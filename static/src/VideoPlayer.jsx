import React, { useState, useEffect } from 'react';
import { Player, ControlBar, BigPlayButton } from 'video-react';
import '../node_modules/video-react/dist/video-react.css';
import { BASE_URL } from './utils/API';

const VideoPlayer = ({ filepath }) => {
    return (
        <Player playsInline src={`${BASE_URL}/video/${filepath}`}>
            <ControlBar />
            <BigPlayButton position="center" />
        </Player>
    );
};

export default VideoPlayer;
