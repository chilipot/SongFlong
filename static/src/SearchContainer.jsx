import React, { useState } from 'react';
import './App.css';
import API from './utils/API';
import LoadingBar from './utils/LoadingBar';

const SearchBar = ({ setLoading, setResults }) => {
    const [query, setQuery] = useState('');
    const search = () => {
        setLoading(true);
        API.get('/search', { params: { query: query } }).then(res => {
            setResults(res.data.results);
            setLoading(false);
        });
    };
    return (
        <input
            placeholder="Music Video Search..."
            type="text"
            onKeyPress={e => {
                if (e.key === 'Enter' && query.length >= 3) {
                    search();
                }
            }}
            onChange={e => setQuery(e.target.value)}
        />
    );
};

const SearchContainer = ({ setPrimary }) => {
    const [results, setResults] = useState([]);
    const [loading, setLoading] = useState(false);

    const setResultsComplex = inResults => {
        setResults(inResults);
        console.log('results');
        console.log(results);
        console.log(inResults);
        // TODO: Implement Choosing
        setPrimary(inResults[0]);
    };

    return (
        <div className="searchbar">
            <SearchBar setLoading={setLoading} setResults={setResultsComplex} />
            <LoadingBar status={loading} />
        </div>
    );
};

export default SearchContainer;
