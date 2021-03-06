import React from 'react';
import styled from 'styled-components';
import { IInputFieldProps } from '../../../interfaces/common';
import { smMax } from '../../../utils/media';
import withError from './WithError';

const StyledInputField = styled.div`
  position: relative;
  width: 100%;
  height: 60px;
  display: flex;
  align-items: center;
  overflow: hidden;

  @media (max-width: ${smMax}) {
    width: 100%;
  }

  background: #ffffff;
  box-shadow: 4px 4px 10px rgba(56, 57, 88, 0.4);
  border-radius: 15px;
`;

const StyledInput = styled.input`
  margin: 0 20px;

  outline: none;
  border: none;
  width: 100%;
  height: 100%;

  font-size: 18px;
  line-height: 22px;
`;

const InputFieldNoError: React.FC<IInputFieldProps> = ({ type, placeholder, value, onChange }) => {
  return (
    <>
      <StyledInputField>
        <StyledInput type={type} placeholder={placeholder} value={value} onChange={onChange} />
      </StyledInputField>
    </>
  );
};

const InputField = withError(InputFieldNoError);

export default InputField;
