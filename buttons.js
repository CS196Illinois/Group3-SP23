import React from 'react';


function Button(props) {
  return (
    <button onClick={props.onClick}>
      {props.label}
    </button>
  );
}

export default Button;

/* props is an object that will have two properties:
1. an onClick function that is called when the user clicks on the button
        * this should take the user to a new page
2. a label function that contains the writing to be displayed on the button
        * this should display the name of the course found by the search function

--> the search function output should be inputted into the props object
    * the name of the course should set the label
    * the course, if found, should be inputted into the onClick function to redirect the site to display the page of the course
*/