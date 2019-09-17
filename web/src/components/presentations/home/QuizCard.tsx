import React from 'react';
import { ChevronRight, Users } from 'react-feather';
import styled from 'styled-components';
import { IQuizCardProps } from '../../../interfaces/home/index';
import { QuizCardContents } from './QuizCardContents';
import { QuizDateCreatedDiv } from './QuizDateCreatedDiv';

const StyledQuizCard = styled.div`
  position: relative;
  max-width: 1065px;
  max-height: 206px;

  padding: 20px calc(20px + 2%) 40px calc(20px + 2%);

  background: #ffffff;
  border-radius: 15px;
  box-shadow: 4px 4px 10px rgba(56, 57, 88, 0.25);
`;

const QuizTitle = styled.div`
  font-size: 32px;
`;

const QuizDescription = styled.div`
  font-weight: 300;
`;

const MiscDetails = styled.div`
  font-weight: 300;
  font-size: 18px;
  margin-top: 15px;
`;

const QuizCard: React.FC<IQuizCardProps> = ({
  title,
  description,
  numAttempted,
  dateCreated,
  children
}) => {
  return (
    <StyledQuizCard>
      <QuizDateCreatedDiv> Created {dateCreated} days ago</QuizDateCreatedDiv>
      <QuizCardContents>
        <div>
          <QuizTitle>{title}</QuizTitle>
          <QuizDescription>{description}</QuizDescription>
          <MiscDetails>
            <Users /> {numAttempted} people attended
          </MiscDetails>
          {children}
        </div>
        <div>
          <ChevronRight />
        </div>
      </QuizCardContents>
    </StyledQuizCard>
  );
};

export default QuizCard;
