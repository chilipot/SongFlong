import React, { useState, useEffect, useContext } from "react";
import "./App.css";
import SearchContainer from "./SearchContainer";
import VideoPlayer from "./VideoPlayer";
import { BASE_URL } from "./utils/API";

const App = () => {
  const [jobIds, setJobIds] = useState([]);
  const search = song => {
    const url = `${BASE_URL}/submit/${encodeURI(song)}`;

    console.log(url);
    fetch(url)
      .then(res => res.json())
      .then(json => setJobIds(json.job_ids));
  };

  return (
    <div className="wrapper">
      <div className="header">
        <div className="container jumbotron">
          <img
            src="https://hackumass.com/assets/img/logo.png"
            alt="hackumass"
            id="hum"
          />
          <h1>Song Flong</h1>
          <h3>Can a music video still work with a different song?</h3>
          <SearchContainer search={search} />
          {jobIds.map(id => (
            <VideoPlayer id={id} key={id} />
          ))}
          <a id="git" href="https://github.com/skylers27/Sound-Repo-Thing">
            Source Code
          </a>
        </div>
      </div>
    </div>
  );
};

export default App;
