import React from 'react';

import '../App.css';

const LoadingBar = ({ status }) =>
    status && (
        <div className="lds-facebook">
            <div />
            <div />
            <div />
            <div />
            <div />
            <div />
            <div />
            <div />
        </div>
    );

export default LoadingBar;
