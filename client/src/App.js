import React, { useState } from "react";

function App() {
  return (
    <div>
      <div>
        <label>
          Start
          <input type="text" name="Start" />
        </label>
        <label>
          Destination
          <input type="text" name="Destination" />
        </label>
        <input type="submit" value="Submit" />
      </div>
    </div>
  );
}

export default App;
