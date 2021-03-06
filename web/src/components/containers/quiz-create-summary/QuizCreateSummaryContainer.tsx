import React from 'react';
import { connect } from 'react-redux';
import { Dispatch } from 'redux';
import { getQuestionsByQuizId, getQuizById, getQuizStatisticsByQuizId } from '../../../api';
import { IQuizCreateSummaryContainerProps } from '../../../interfaces/quiz-create-summary';
import { IQuiz } from '../../../interfaces/quiz-create-summary';
import { AppState } from '../../../store/store';
import { getUser } from '../../../utils/auth';
import { history } from '../../../utils/history';
import Loading from '../../presentations/common/Loading';
import QuizCreateSummary from '../../presentations/quiz-summaries/QuizCreateSummary';
import { setLoadingComplete } from '../loading/redux/actions';
import { setQuizCreateSummary } from './redux/actions';

const getQuizLink = (quizId: string) => {
  return `${window.location.origin}/quiz/${quizId}`;
};

class QuizCreateSummaryContainer extends React.Component<IQuizCreateSummaryContainerProps> {
  public async componentDidMount() {
    this.props.setLoadingComplete(false);

    const userId = getUser().id;
    const { match: { params: { id: quizId = '' } = {} } = {} , ...props } = this.props;
    const quiz = (await getQuizById(quizId)).data;
    const questions = (await getQuestionsByQuizId(quizId)).data;

    if (quiz === undefined || quiz.creator_id !== userId) {
      history.push('/');
    } else {
      const summary = (await getQuizStatisticsByQuizId(quizId)).data;

      props.setQuiz({
        name: quiz.title,
        description: quiz.description || 'No description',
        numAttempts: quiz.num_attempts,
        questions: questions.map((qn: any, idx: number) => {
          const qnSummary = summary[idx];

          return {
            questionNumber: idx + 1,
            text: qn.text,
            options: qn.options.map((opt: string, optIdx: number) => {
              return {
                option: opt,
                percentage: qnSummary.stats.percentage[optIdx]
              };
            }),
            correctOption: qnSummary.correct_option
          };
        })
      });
    }

    this.props.setLoadingComplete(true);
  }

  public render() {
    const {
      match: { params: { id: quizId = '' } = {} } = {},
      name,
      description,
      numAttempts,
      questions
    } = this.props;

    if (!this.props.hasLoaded) {
      return <Loading />;
    }

    return (
      <QuizCreateSummary
        name={name}
        description={description}
        numAttempts={numAttempts}
        questions={questions}
        sharableLink={getQuizLink(quizId)}
      />
    );
  }
}

const mapStateToProps = (state: AppState) => ({
  name: state.quizCreateSummary.name,
  description: state.quizCreateSummary.description,
  numAttempts: state.quizCreateSummary.numAttempts,
  questions: state.quizCreateSummary.questions,
  hasLoaded: state.loading.hasLoaded
});

const mapDispatchToProps = (dispatch: Dispatch) => {
  return {
    setQuiz: (quiz: IQuiz) => {
      dispatch(setQuizCreateSummary(quiz));
    },
    setLoadingComplete: (hasLoaded: boolean) =>
      dispatch(setLoadingComplete(hasLoaded))
  };
};

export default connect(
  mapStateToProps,
  mapDispatchToProps
)(QuizCreateSummaryContainer);
