import "./InputContainer.css";
import { useState } from "react";
const axios = require("axios");

function InputContainer() {
  const [data, setData] = useState("NoData");
  const [start, setStart] = useState("");
  const [destination, setDestination] = useState("");

  const switchStr = "<=>";

  const clickHandler = async (event) => {
    event.preventDefault();
    const response = await axios.post("/post", {
      start: start,
      destination: destination,
    });
    setData(response.data);
    console.log(response.data);
  };

  const switchInputs = (event) => {
    event.preventDefault();
    console.log(`Start: ${start}, Destination: ${destination}`);
    let temp = start;
    setStart(destination);
    setDestination(temp);
  };

  return (
    <div className="search-information">
      <form className="search-form" id="search-form" name="search-form">
        <div className="user-input">
          <input
            className="search-input"
            name="start"
            id="start"
            value={start}
            onChange={(event) => setStart(event.target.value)}
            placeholder="Start"
          />
          <button
            className="input-button"
            id="switch-inputs"
            onClick={switchInputs}
          >
            {switchStr}
          </button>
          <input
            className="search-input"
            name="destination"
            id="destination"
            value={destination}
            onChange={(event) => setDestination(event.target.value)}
            placeholder="Destination"
          />
        </div>

        <button
          className="input-button"
          id="search-button"
          onClick={clickHandler}
        >
          START SEARCH
        </button>
      </form>
      <p>{data}</p>
    </div>
  );
}

export default InputContainer;
