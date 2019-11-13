import React from 'react';
import './App.css';

const SearchContainer = ({ search }) => {
    return (
        <div>
            <input
                placeholder="Youtube Search..."
                type="text"
                onKeyPress={e => {
                    if (e.key === 'Enter') {
                        search(e.target.value);
                    }
                }}
            />
        </div>
    );
};

export default SearchContainer;
