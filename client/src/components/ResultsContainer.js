import PathContainer from "./PathContainer";
import "./ResultsContainer.css";

const ResultsContainer = ({ results }) => {
  const paths = results.map((path) => <PathContainer data={path} />);

  return (
    <div>
      <h2>All results</h2>
      <p>{paths}</p>
    </div>
  );
};

export default ResultsContainer;
