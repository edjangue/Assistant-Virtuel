import React, { useState } from 'react';

const UserIdForm = ({ submitUserId }) => {
    const [userIdInput, setUserIdInput] = useState('');

    const handleSubmit = (event) => {
        event.preventDefault();
        submitUserId(userIdInput);
        setUserIdInput('');
    };

    return (
        <form onSubmit={handleSubmit} id="user-id-form">
            <input
                type="text"
                id="user-id"
                value={userIdInput}
                placeholder="Entrez votre ID utilisateur..."
                aria-label="ID utilisateur"
                onChange={(e) => setUserIdInput(e.target.value)}
                required
            />
            <button type="submit" id="submit-id" aria-label="Soumettre votre ID">Soumettre</button>
        </form>
    );
};

export default UserIdForm;
