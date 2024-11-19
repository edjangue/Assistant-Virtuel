import React from 'react';
import './LoadingIndicator.css'; // Import CSS for styling

const LoadingIndicator = () => {
    return (
        <div className="loading-indicator">
            <span className="dot">.</span>
            <span className="dot">.</span>
            <span className="dot">.</span>
        </div>
    );
};

export default LoadingIndicator;
