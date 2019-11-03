import React from "react";
import "./App.css";

const SearchContainer = ({ startJobs = () => null }) => {
  return (
    <div>
      <input
        placeholder="Youtube Search..."
        type="text"
        onKeyPress={e => {
          if (e.key === "Enter") {
            startJobs(e);
          }
        }}
      />
    </div>
  );
};

export default SearchContainer;
