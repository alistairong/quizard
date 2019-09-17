import React from 'react';
import { BeigeBackground } from '../common/BeigeBackground';
import { BodyAfterNavBarWithPadding } from '../common/BodyAfterNavBarWithPadding';
import HomeContent from './HomeContent';
import HomeHeader from './HomeHeader';
import HomeNavBar from './HomeNavBar';

const Home: React.FC = (props) => {
  return (
    <BeigeBackground>
      <HomeNavBar />
      <BodyAfterNavBarWithPadding>
        <HomeHeader />
        <HomeContent>{props.children}</HomeContent>
      </BodyAfterNavBarWithPadding>
    </BeigeBackground>
  );
};

export default Home;
