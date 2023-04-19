import React from 'react';
import myImage from './images/myImage.jpg';
import './images/size.css';

export const Graph = () => {
    return (
      <div>
        <img src={myImage} alt="My Image" className="my-image"/>
      </div>
    );
}