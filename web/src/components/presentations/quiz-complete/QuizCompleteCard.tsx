import React from 'react';
import { Link } from 'react-router-dom';
import styled from 'styled-components';
import { IQuizCompleteCardProps } from '../../../interfaces/quiz-complete';
import { ReactComponent as Owl } from '../../../svg/owl.svg';
import QuizRedoButtonContainer from '../../containers/quiz-complete/QuizRedoButtonContainer';
import BigDarkButton from '../common/buttons/BigDarkButton';
import WholeScreenCard from '../common/WholeScreenCard';

const StyledOwl = styled(Owl)`
  height: 170px;
`;

const QuizCompleteCard: React.FC<IQuizCompleteCardProps> = ({ score, maxScore, quizName }) => {
  return (
    <>
      <StyledOwl />
      <h3>
        You have scored {score}/{maxScore} for {quizName}!
      </h3>
      <p style={{ fontWeight: 300 }}>
        Your quiz results have been saved and you can review your quiz answers
        anytime.
      </p>
      <QuizRedoButtonContainer />
      <BigDarkButton>Review Quiz Results</BigDarkButton>
      <Link to="/">
        <div style={{ fontSize: '18px', textDecoration: 'underline' }}>
          Back to Home
        </div>
      </Link>
    </>
  );
};

export default QuizCompleteCard;
