import React from 'react';

const Message = ({ message, className }) => {
    return (
        <div className={`message ${className}`}>
            {message}
        </div>
    );
};

export default Message;
