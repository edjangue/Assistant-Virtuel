import React, { useState } from 'react';
import UserIdForm from './UserIdForm';
import Message from './Message';
import LoadingIndicator from './LoadingIndicator'; // Import the loading indicator component

const ChatContainer = () => {
    const [userId, setUserId] = useState('');
    const [messages, setMessages] = useState([]);
    const [showOptions, setShowOptions] = useState(false);
    const [loading, setLoading] = useState(false); // New state variable for loading indicator

    const submitUserId = (id) => {
        setUserId(id);
        appendMessage('Bienvenue dans le chatbot agro-alimentaire ! Posez-moi vos questions.', 'bot-message');
        setShowOptions(true);


    };
    

    const appendMessage = (message, className) => {
        setMessages((prevMessages) => [...prevMessages, { message, className }]);
    };

    // Send the selected intent to the backend
    const handleOptionClick = async (intent) => {
        setShowOptions(false);
        setLoading(true); // Show loading indicator

        try {
            const response = await fetch('http://127.0.0.1:5000/webhook', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ user_id: userId, intent_click: intent })
            });

            const data = await response.json();
            appendMessage(data.message, 'bot-message');
        } catch (error) {
            appendMessage('Erreur de connexion. Veuillez réessayer.', 'bot-message');
        }

        setLoading(false); // Hide loading indicator
    };

    const sendMessage = async (message) => {
        appendMessage(message, 'user-message');
        // Clear the input field after the message is sent
        document.getElementById('user-input').value = '';
        setLoading(true); // Show loading indicator

        try {
            const response = await fetch('http://127.0.0.1:5000/webhook', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ user_id: userId, message })
            });

            const data = await response.json();
            appendMessage(data.message, 'bot-message');
        } catch (error) {
            appendMessage('Erreur de connexion. Veuillez réessayer.', 'bot-message');
        }

        setLoading(false); // Hide loading indicator
    };


    return (
        <section id="chat-container">
            <header>
                {!userId && <UserIdForm submitUserId={submitUserId} />}
            </header>
            <main id="messages">
                {messages.map((msg, index) => (
                    <Message key={index} message={msg.message} className={msg.className} />
                ))}
                {loading && <LoadingIndicator />} {/* Show loading indicator when loading */}
            </main>
            {userId && (
                <footer>
                    {showOptions && (
                        <div>
                            <button onClick={() => handleOptionClick('TRACEABILITY')}>Traçabilité des produits</button>
                            <button onClick={() => handleOptionClick('RECOMMENDATION')}>Recommandations de produits</button>
                            <button onClick={() => handleOptionClick('NUTRITION_ADVICE')}>Conseils nutritionnels</button>
                        </div>
                    )}
                    <input
                        type="text"
                        id="user-input"
                        placeholder="Posez votre question ici..."
                        aria-label="Votre message"
                        onKeyPress={(e) => { if (e.key === 'Enter') sendMessage(e.target.value); }}
                    />
                    <button id="send-button" onClick={() => sendMessage(document.getElementById('user-input').value)}>Envoyer</button>
                </footer>
            )}
        </section>
    );
};

export default ChatContainer;
