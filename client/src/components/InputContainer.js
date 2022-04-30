import "./InputContainer.css";
import { useState } from "react";
import ResultsContainer from "./ResultsContainer";
const axios = require("axios");

function InputContainer() {
  const [data, setData] = useState([]);
  const [start, setStart] = useState("");
  const [destination, setDestination] = useState("");
  const [results, setResults] = useState(false);

  const [searchButton, setSearchButton] = useState("Go!");

  const switchStr = "<=>";

  const clickHandler = async (event) => {
    event.preventDefault();
    setSearchButton("Loading...");
    const response = await axios.post("/post", {
      start: start,
      destination: destination,
    });
    setResults(true);
    setData(response.data);
    setSearchButton("Go!");
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
          {searchButton}
        </button>
      </form>
      <div>{results ? <ResultsContainer results={data} /> : ""}</div>
    </div>
  );
}

export default InputContainer;
