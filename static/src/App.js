import React, { useState } from "react";
import "./App.css";
import SearchContainer from "./SearchContainer";
import API from "./utils/API";
import VideosContainer from "./VideosContainer";

const App = () => {
  const [jobs, setJobs] = useState([]);
  const startJobs = e => {
    const search = e.target.value;
    API.get(`/submit/${search}`).then(res => setJobs(res.data.job_ids || []));
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
          <SearchContainer startJobs={startJobs} />
          <VideosContainer jobs={jobs} />
          <a id="git" href="https://github.com/skylers27/Sound-Repo-Thing">
            Source Code
          </a>
        </div>
      </div>
    </div>
  );
};

export default App;
