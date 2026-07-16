import { useState, useEffect } from "react";
import api from "./api";
import "./index.css";

const ChatBot = () => {

    const [context, setContext] = useState([]);
    const [history, setHistory] = useState([]);
    const [message, setMessage] = useState("");

    const [messages, setMessages] = useState([
        {
            sender: "bot",
            text: "Good Day!\n"
        }
    ]);

    const [loading, setLoading] = useState(false);

    const loadHistory = async () => {

        const response = await api.get(
            "/api/conversations/user123"
        );

        setHistory(response.data);

    };

    useEffect(() => {
        loadHistory();
    }, []);

    const sendMessage = async () => {

        if (!message.trim()) return;

        const userMessage = {
            sender: "user",
            text: message
        };

        setMessages(prev => [
            ...prev,
            userMessage
        ]);

        setLoading(true);

        const response = await api.post(
            "/api/chat",
            {
                session_id: "user123",
                message,
                context
            }
        );

        setLoading(false);

        const botMessage = {
            sender: "bot",
            text: response.data.response,
            suggestions: [
                "Tell me more",
                "Help",
                "Thanks"
            ]
        };

        setMessages(prev => [
            ...prev,
            botMessage
        ]);

        setHistory(prev => [
            ...prev,
            {
                user_message: message,
                bot_response: response.data.response
            }
        ]);

        setContext(prev => [
            ...prev,
            message,
            response.data.response
        ].slice(-5));

        setMessage("");

    };

    return (
        <div>

            <h2>ChatBot</h2>

            {messages.map((msg, index) => (

                <div key={index}>
                    <b>{msg.sender}:</b> {msg.text}
                </div>

            ))}

            {loading && <p>Typing...</p>}

            <input
                value={message}
                onChange={(e) => setMessage(e.target.value)}
                placeholder="Type a message..."
            />

            <button onClick={sendMessage}>
                Send
            </button>

        </div>
    );

};

export default ChatBot;