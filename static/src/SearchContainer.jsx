import React, { useState } from 'react';
import './App.css';
import { BASE_URL } from './utils/API';

const Loading = status => {
    console.log(status);
    if (status.status) {
        return (
            <div className="lds-facebook">
                <div></div>
                <div></div>
                <div></div>
                <div></div>
                <div></div>
                <div></div>
                <div></div>
                <div></div>
            </div>
        );
    } else {
        return <div></div>;
    }
};

const SearchContainer = ({ setJobIds }) => {
    const [status, setStatus] = useState({ value: false });
    const search = song => {
        setStatus({ value: true });
        setJobIds([]);
        const url = `${BASE_URL}/submit/${encodeURI(song)}`;
        console.log(url);
        fetch(url)
            .then(res => res.json())
            .then(json => setJobIds(json.job_ids))
            .then(() => setStatus({ value: false }));
    };
    return (
        <div className="searchbar">
            <input
                placeholder="Youtube Search..."
                type="text"
                onKeyPress={e => {
                    if (e.key === 'Enter') {
                        search(e.target.value);
                    }
                }}
            />
            <Loading status={status.value} />
        </div>
    );
};

export default SearchContainer;
