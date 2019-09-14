"""
Schemas are Cerberus rules used for validation of user input
and serializing results to return to users.
"""

# Conversion
to_boolean = lambda v: v.lower() in ["true", "1"]

# Common rules
is_integer = {"type": "integer", "coerce": int, "nullable": False, "empty": False}
is_unsigned_integer_with_max = {
    "type": "integer",
    "coerce": int,
    "nullable": False,
    "empty": False,
    "min": 0,
    "max": 100,
}
is_unsigned_integer = {
    "type": "integer",
    "coerce": int,
    "nullable": False,
    "empty": False,
    "min": 0,
}
is_nullable_integer = {"type": "integer", "coerce": int}
is_required_integer = {
    "type": "integer",
    "coerce": int,
    "nullable": False,
    "empty": False,
    "required": True,
}
is_required_unsigned_integer = {
    "type": "integer",
    "coerce": int,
    "nullable": False,
    "empty": False,
    "required": True,
    "min": 0,
}
is_boolean = {
    "type": "boolean",
    "coerce": to_boolean,
    "nullable": False,
    "empty": False,
}
is_string = {
    "type": "string",
    "empty": False,
    "nullable": False,
}
is_required_string = {
    "type": "string",
    "empty": False,
    "nullable": False,
    "required": True,
}
is_string_list = {"type": "list", "schema": is_string}
is_required_string_list = {
    "type": "list",
    "required": True,
    "schema": is_string,
}
is_unsigned_integer_list = {
	"type": "list",
	"schema": is_unsigned_integer,
}


# Schemas

QUERY_PARAM_READ_SCHEMA = {
    "many": is_boolean,
    "last_id": is_unsigned_integer,
    "limit": is_unsigned_integer_with_max,
}

QUIZ_QUESTION_READ_SCHEMA = {
    "id": is_unsigned_integer,
    "quiz_id": is_unsigned_integer,
    "text": {"type": "string"},
    "animation_id": is_unsigned_integer,
    "options": {"readonly": True},
	"correct_option": is_unsigned_integer,	# Check correct answer in backend ?
    "created_at": is_unsigned_integer,
    "updated_at": is_unsigned_integer,
    **QUERY_PARAM_READ_SCHEMA,
}

QUIZ_QUESTION_WRITE_SCHEMA = {
    "id": {"readonly": True},
    "quiz_id": is_required_unsigned_integer,
    "text": is_required_string,
    "animation_id": is_unsigned_integer,
    "options": is_required_string_list,
    "correct_option": is_required_unsigned_integer,
    "created_at": {"readonly": True},
    "updated_at": {"readonly": True},
}

QUIZ_ATTEMPT_READ_SCHEMA = {
    "id": is_unsigned_integer,
    "quiz_id": is_unsigned_integer,
    "user_id": is_unsigned_integer,
    "score": is_integer,
    "created_at": is_unsigned_integer,
    "updated_at": is_unsigned_integer,
    **QUERY_PARAM_READ_SCHEMA,
}

QUIZ_ATTEMPT_WRITE_SCHEMA = {
    "id": {"readonly": True},
    "quiz_id": is_required_unsigned_integer,
    "user_id": is_required_unsigned_integer,
    "score": {"readonly": True},
    "created_at": {"readonly": True},
    "updated_at": {"readonly": True},
}

QUIZ_ANSWER_READ_SCHEMA = {
    "id": is_unsigned_integer,
    "quiz_id": is_unsigned_integer,
    "attempt_id": is_unsigned_integer,
    "user_id": is_unsigned_integer,
    "selected_option": is_unsigned_integer,
    "created_at": is_unsigned_integer,
    "updated_at": is_unsigned_integer,
    **QUERY_PARAM_READ_SCHEMA,
}

QUIZ_ANSWER_WRITE_SCHEMA = {
    "id": {"readonly": True},
    "quiz_id": is_required_unsigned_integer,
    "attempt_id": is_required_unsigned_integer,
    "user_id": is_required_unsigned_integer,
    "selected_option": is_required_integer,
    "created_at": {"readonly": True},
    "updated_at": {"readonly": True},
    "many": is_boolean,
    "last_id": is_unsigned_integer,
    "limit": is_unsigned_integer_with_max,
}


QUIZ_READ_SCHEMA = {
    "id": is_unsigned_integer,
    "title": is_string,
    "creator_id": is_unsigned_integer,
    "category_id": is_unsigned_integer,
    "type_id": is_unsigned_integer,
    "animation_id": is_unsigned_integer,
    "questions_order": is_unsigned_integer_list,
	"questions": {	# A list of dicts
		"type": "list",
		"schema": {
			"type": "dict",
			"schema": QUIZ_QUESTION_READ_SCHEMA,
		},
	},
    "created_at": is_unsigned_integer,
    "updated_at": is_unsigned_integer,
    **QUERY_PARAM_READ_SCHEMA,
}

QUIZ_WRITE_SCHEMA = {
    "id": {"readonly": True},
    "title": is_string,
    "creator_id": is_required_unsigned_integer,
    "category_id": is_unsigned_integer,
    "type_id": is_unsigned_integer,
    "animation_id": is_unsigned_integer,
    "questions_order": is_unsigned_integer_list,
	"questions": {	# A list of dicts
		"type": "list",
        "required": True,
		"schema": {
			"type": "dict",
            "required": True,
			"schema": {
                **QUIZ_QUESTION_WRITE_SCHEMA,
                "quiz_id": is_unsigned_integer,
            },
		},
	},
    "created_at": {"readonly": True},
    "updated_at": {"readonly": True},
}

USER_READ_SCHEMA = {
    "id": is_integer,
    "full_name": {"type": "string"},
    "email": {"type": "string"},
    "password": {"readonly": True},
    "disabled": is_boolean,
    "created_at": is_unsigned_integer,
    "updated_at": is_unsigned_integer,
    **QUERY_PARAM_READ_SCHEMA,
}

USER_WRITE_SCHEMA = {
    "id": {"readonly": True},
    "full_name": is_required_string,
    "display_name": {"type": "string"},
    "email": is_required_string,
    "password": {**is_required_string, "minlength": 8, "maxlength": 128},
    "disabled": {"readonly": True},
    "created_at": {"readonly": True},
    "updated_at": {"readonly": True},
}

USER_LOGIN_SCHEMA = {
    "email": is_required_string,
    "password": {**is_required_string, "minlength": 8, "maxlength": 128},
}

"""
The format for keys in `schemas` is
<tablename>_read or <tablename>_write

Please strictly follow this format
as several utils function get the schema by
adding '_read' after model.__tablename__
"""
schemas = {
    "quiz_read": QUIZ_READ_SCHEMA,
    "quiz_write": QUIZ_WRITE_SCHEMA,
    "quiz_question_read": QUIZ_QUESTION_READ_SCHEMA,
    "quiz_question_write": QUIZ_QUESTION_WRITE_SCHEMA,
    "quiz_attempt_read": QUIZ_ATTEMPT_READ_SCHEMA,
    "quiz_attempt_write": QUIZ_ATTEMPT_WRITE_SCHEMA,
    "quiz_answer_read": QUIZ_ANSWER_READ_SCHEMA,
    "quiz_answer_write": QUIZ_ANSWER_WRITE_SCHEMA,
    "user_read": USER_READ_SCHEMA,
    "user_write": USER_WRITE_SCHEMA,
    "user_login": USER_LOGIN_SCHEMA,
}