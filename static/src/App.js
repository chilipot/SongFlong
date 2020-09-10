import React, { useState, useEffect, useContext } from 'react';
import './App.css';
import SearchContainer from './SearchContainer';
import VideoContainer from './VideoContainer';

const App = () => {
    const [jobIds, setJobIds] = useState([]);

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
                    <SearchContainer setJobIds={setJobIds} />
                </div>
            </div>
            <div className="videos container">
                {jobIds.map((id, index) => (
                    <VideoContainer id={id} index={index} />
                ))}
            </div>
            <div className="footer">
                <a
                    id="git"
                    href="https://github.com/skylers27/Sound-Repo-Thing"
                >
                    Source Code
                </a>
            </div>
        </div>
    );
};

export default App;
