import React from "react";
import "./App.css";

const SearchContainer = (props) => {
  return (
    <div>
      <input
        placeholder="Youtube Search..."
        type="text"
        onKeyPress={e => {
          if (e.key === "Enter") {
            props.search(e.target.value);
          }
        }}
      />
    </div>
  );
};

export default SearchContainer;
