import React, { useState, useEffect } from 'react';
import { Player, ControlBar } from 'video-react';
import '../node_modules/video-react/dist/video-react.css';
import { BASE_URL } from './utils/API';
import Request from 'axios-request-handler';

const VideoPlayer = ({ filepath }) => {
    // const [video, setVideo] = useState('');
    // useEffect(() => {
    //     const url = `${BASE_URL}/results/${id}`;
    //     const jobResult = new Request(url);
    //     jobResult.poll(1000).get(res => {
    //         if (res.status === 400) {
    //             throw 'Unable To Retrieve Video Src';
    //         } else if (res.status === 200) {
    //             setVideo(res.data);
    //             return false;
    //         }
    //         return true;
    //     });
    // }, [id]);

    return (
        <Player playsInline src={`${BASE_URL}/video/${filepath}`}>
            <ControlBar />
        </Player>
    );
};

export default VideoPlayer;
