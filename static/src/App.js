import React, { useState } from 'react';
import './App.css';
import API from './utils/API';
import SearchContainer from './SearchContainer';
import VideoContainer from './VideoContainer';
import LoadingBar from './utils/LoadingBar';

const App = () => {
    // Primary: Music Video
    // Secondaries: Audios to overlay
    const [primary, setPrimary] = useState();
    const [secondaries, setSecondaries] = useState([]);
    const [loading, setLoading] = useState(false);
    const [jobIds, setJobIds] = useState([]);

    const setPrimaryAndFindSecondaries = inPrimary => {
        setPrimary(inPrimary);
        setLoading(true);
        API.post('/related', inPrimary).then(res => {
            const inSecondaries = res.data.results;
            setSecondaries(inSecondaries);
            console.log(inSecondaries);
            API.post('/submit/', {
                primary: inPrimary,
                secondary: inSecondaries.slice(0, 5)
            }).then(res => {
                setJobIds(res.data.job_ids);
                setLoading(false);
            });
        });
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
                    <SearchContainer
                        setPrimary={setPrimaryAndFindSecondaries}
                    />
                    <LoadingBar status={loading} />
                </div>
            </div>
            <div className="videos container">
                {jobIds.map((id, index) => (
                    <VideoContainer id={id} index={index} />
                ))}
            </div>
            <div className="footer">
                <a id="git" href="https://github.com/chilipot/SongFlong">
                    Source Code
                </a>
            </div>
        </div>
    );
};

export default App;
