import React, { useState, useEffect } from 'react';
import { Player, ControlBar } from 'video-react';
import '../node_modules/video-react/dist/video-react.css';
import { BASE_URL } from './utils/API';
import Request from 'axios-request-handler';

const VideoPlayer = ({ filepath }) => {
    return (
        <Player playsInline src={`${BASE_URL}/video/${filepath}`}>
            <ControlBar />
        </Player>
    );
};

export default VideoPlayer;
