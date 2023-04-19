import React, { useState } from "react";

export const Searchbar = () => {
  const [formInput, setFormInput] = useState("");

  // handleSubmit(event) {
  //     event.preventDefault();
  //     setFormInput(formInput);
  // }
  console.log("before formInput: ", formInput);

  const handleInputChange = (event) => {
    console.log("Hi Rui asked a really question");
    const { value } = event.target;
    setFormInput(value);
    console.log("after setting formInput: ", formInput);
  };

  return (
    <div>
      <form>
        <label>
          Search Result:
          <input
            type="text"
            value={formInput}
            onChange={handleInputChange}
          ></input>
        </label>
        <input type="submit" value="Submit" />
      </form>
      <p>{formInput}</p>
    </div>
  );
};
