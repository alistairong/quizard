# Response's type:
# <aiohttp.client_reqrep.ClientResponse>
# Client: aiohttp
# https://docs.aiohttp.org/en/stable/client_quickstart.html#json-request

from quizard_backend.models import User
from quizard_backend.tests import get_fake_user, profile_created_from_origin
from quizard_backend.utils.query import get_one
from quizard_backend.utils.crypto import hash_password

## GET ##


async def test_get_one_user(client, users):
    # Default: returns the first user
    res = await client.get("/users")
    assert res.status == 200

    body = await res.json()
    assert "data" in body
    assert isinstance(body["data"], dict)
    assert profile_created_from_origin(users[0], body["data"])

    # Get one user with id
    res = await client.get("/users?id=3")
    assert res.status == 200

    body = await res.json()
    assert "data" in body
    assert isinstance(body["data"], dict)
    assert profile_created_from_origin(users[2], body["data"])

    # A random-order user will be returned
    res = await client.get("/users")
    assert res.status == 200

    body = await res.json()
    assert "data" in body
    assert isinstance(body["data"], dict)
    assert any(profile_created_from_origin(user, body["data"]) for user in users)

    # User doesnt exist
    res = await client.get("/users?id=9999")
    assert res.status == 404

    # Invalid id
    res = await client.get("/users?id=true")
    assert res.status == 400

    res = await client.get("/users?id=")
    assert res.status == 400

    # Non-exist args
    res = await client.get("/users?end_timestamp=true")
    assert res.status == 400

    res = await client.get("/users?end_timestamp=")
    assert res.status == 400

async def test_get_all_users(client, users):
    res = await client.get("/users?many=trUe")
    assert res.status == 200

    body = await res.json()
    assert "data" in body
    assert isinstance(body["data"], list)
    assert len(body["data"]) == 15  # Default offset for User is 15
    assert all(
        profile_created_from_origin(origin, created)
        for origin, created in zip(users, body["data"])
    )

    # GET request will have its body ignored.
    res = await client.get("/users?many=True", json={"id": 3})
    assert res.status == 200

    body = await res.json()
    assert "data" in body
    assert isinstance(body["data"], list)
    assert len(body["data"]) == 15  # Default offset for User is 15

    # Get one user by id with many=True
    res = await client.get("/users?id=3&many=true")
    assert res.status == 200

    body = await res.json()
    assert "data" in body
    assert isinstance(body["data"], list)
    assert len(body["data"]) == 1
    assert profile_created_from_origin(users[2], body["data"][0])

    ## LIMIT ##
    # No users
    res = await client.get("/users?many=true&limit=0")
    assert res.status == 200

    body = await res.json()
    assert "data" in body
    assert isinstance(body["data"], list)
    assert not body["data"]

    # 10 users
    res = await client.get("/users?many=true&limit=10")
    assert res.status == 200

    body = await res.json()
    assert "data" in body
    assert isinstance(body["data"], list)
    assert len(body["data"]) == 10
    assert all(
        profile_created_from_origin(origin, created)
        for origin, created in zip(users[:10], body["data"])
    )

    # -1 users
    res = await client.get("/users?many=true&limit=-1")
    assert res.status == 400


async def test_get_users_with_last_id(client, users):
    # Use last_id in query parameter.
    res = await client.get("/users?last_id=3&many=true")
    assert res.status == 200

    body = await res.json()
    assert "data" in body
    assert isinstance(body["data"], list)
    assert len(body["data"]) == 15  # Default offset for User is 15

    # Check if all profiles match from id 4 to 19
    assert all(
        profile_created_from_origin(origin, created)
        for origin, created in zip(users[3:20], body["data"])
    )

    ## Get user and ignore pagination
    # Although last_id is provided,
    # it is ignored if many=False (default)
    res = await client.get("/users?last_id=3")
    assert res.status == 200

    body = await res.json()
    assert "data" in body
    assert isinstance(body["data"], dict)
    assert body["data"]["id"] == 1

    # Invalid last_id
    res = await client.get("/users?last_id=true")
    assert res.status == 400

    res = await client.get("/users?last_id=")
    assert res.status == 400


## CREATE ##


async def test_create_user(client, users):
    new_user = get_fake_user()

    res = await client.post(
        "/users", json=new_user
    )
    assert res.status == 200

    body = await res.json()
    assert "data" in body
    assert isinstance(body["data"], dict)

    all_users = await User.query.gino.all()
    assert len(all_users) == len(users) + 1
    assert profile_created_from_origin(new_user, all_users[-1].to_dict())
    assert all(
        profile_created_from_origin(origin, created.to_dict())
        for origin, created in zip(users, all_users)
    )

    # Ignore param args
    # POST request will have its query parameter (args) ignored.
    new_user = get_fake_user()
    res = await client.post(
        "/users", json=new_user
    )
    assert res.status == 200

    body = await res.json()
    assert "data" in body
    assert isinstance(body["data"], dict)

    all_users = await User.query.gino.all()
    assert len(all_users) == len(users) + 2
    assert profile_created_from_origin(new_user, all_users[-1].to_dict())
    assert all(
        profile_created_from_origin(origin, created.to_dict())
        for origin, created in zip(users, all_users)
    )

async def test_create_user_with_invalid_args(client, users):
    res = await client.post("/users", json={})
    assert res.status == 400

    res = await client.post(
        "/users", json={"id": 4}
    )
    assert res.status == 400

    res = await client.post(
        "/users", json={"full_name": ""}
    )
    assert res.status == 400

    res = await client.post(
        "/users",
        json={"full_name": ""},
    )
    assert res.status == 400

    res = await client.post(
        "/users",
        json={"full_name": "Josh", "password": ""},
    )
    assert res.status == 400

    res = await client.post(
        "/users", json={"email": ""}
    )
    assert res.status == 400

    res = await client.post(
        "/users", json={"location": 2}
    )
    assert res.status == 400

    res = await client.post(
        "/users", json={"created_at": 2}
    )
    assert res.status == 400

    res = await client.post(
        "/users", json={"updated_at": 2}
    )
    assert res.status == 400

    # Invalid or weak password
    res = await client.post(
        "/users",
        json={"full_name": "Josh", "password": "mmmw"}
    )
    assert res.status == 400

    res = await client.post(
        "/users",
        json={"full_name": "Josh", "password": "qweon@qweqweklasl"}
    )
    assert res.status == 400

    # Assert no new users are created
    all_users = await User.query.gino.all()
    assert len(all_users) == len(users)


## UPDATE ##

async def test_update_one_user(client, users, token_user):
    new_changes = {
        "full_name": "this name surely doesnt exist",
        "password": "strong_password_123",
    }

    # Without token
    res = await client.put("/users?id=5", json=new_changes)
    assert res.status == 401

    # Another user
    res = await client.put(
        "/users?id=10", json=new_changes, headers={"Authorization": token_user}
    )
    assert res.status == 401

    # With id
    res = await client.put(
        "/users?id=1", json=new_changes, headers={"Authorization": token_user}
    )
    assert res.status == 200

    body = await res.json()
    assert "data" in body
    assert isinstance(body["data"], dict)
    updated_user = await get_one(User, id=1)

    ## Assert the new password has been updated
    assert profile_created_from_origin(
        {**body["data"], "password": hash_password(new_changes["password"])},
        updated_user.to_dict(),
        ignore=["updated_at"],
    )

    # With full_name and email
    # Update is invalid without id
    new_changes = {"full_name": "another new name for my friend"}
    res = await client.put(
        "/users?full_name={}&email={}".format(users[6]["full_name"], users[6]["email"]),
        json=new_changes,
        headers={"Authorization": token_user},
    )
    assert res.status == 401

    # User doesnt exist
    res = await client.put(
        "/users?id=9999",
        json=new_changes,
        headers={"Authorization": token_user},
    )
    assert res.status == 404

    # Update to a weak password
    new_changes = {"password": "mmmk"}
    res = await client.put(
        "/users?id=1", json=new_changes, headers={"Authorization": token_user}
    )
    assert res.status == 400


## DELETE ##


# async def test_delete_user(client, users, token_admin, token_mod, token_user):
#     # As admin
#     res = await client.delete("/users?id=7", headers={"Authorization": token_admin})
#     assert res.status == 200
#
#     body = await res.json()
#     assert "data" in body
#     assert body["data"] is None
#
#     all_users = await User.query.gino.all()
#     assert len(all_users) == len(users)
#     disabled_users_count = 0
#     for user in all_users:
#         if user.to_dict()["disabled"]:
#             disabled_users_count += 1
#     assert disabled_users_count == 1
#
#     # Without token
#     res = await client.delete("/users?id=7")
#     assert res.status == 401
#
#     # As mod
#     res = await client.delete("/users?id=7", headers={"Authorization": token_mod})
#     assert res.status == 401
#
#     # As user
#     res = await client.delete("/users?id=7", headers={"Authorization": token_user})
#     assert res.status == 401
#
#     # No new users are "deleted"
#     all_users = await User.query.gino.all()
#     assert len(all_users) == len(users)
#     disabled_users_count = 0
#     for user in all_users:
#         if user.to_dict()["disabled"]:
#             disabled_users_count += 1
#     assert disabled_users_count == 1


# async def test_delete_user_self(client, users, token_user):
#     # User can only "delete" himself/herself
#     res = await client.delete("/users?id=23", headers={"Authorization": token_user})
#     assert res.status == 200
#
#     # No new users are "deleted"
#     all_users = await User.query.gino.all()
#     assert len(all_users) == len(users)
#
#     deleted_user = await User.get(id=23)
#     assert deleted_user["disabled"]
#
#     # Ensure only 1 user is "deleted"
#     disabled_users_count = 0
#     for user in all_users:
#         if user.to_dict()["disabled"]:
#             disabled_users_count += 1
#     assert disabled_users_count == 1