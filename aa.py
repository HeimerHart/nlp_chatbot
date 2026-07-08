import "./theme.css";
import "./index.css";
import { useState, useEffect } from "react";
import api from "./api";

const App = () => {
  
  const isAdmin = () => {
  const token = localStorage.getItem("token");
  if (!token) return false;

  const payload = JSON.parse(atob(token.split(".")[1]));
  return payload.role === "admin";
};

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

    if (!message.trim()) {
      return;
    }

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
        message: message,
        context: context
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

    <div className="container">

      <div className="sidebar">

        <h3>History</h3>

        {history.slice(-10).map((chat, index) => (

          <div
            key={index}
            style={{
              marginBottom: "10px",
              padding: "8px",
              background: "#ffffff20",
              borderRadius: "8px"
            }}
          >

            <p>{chat.user_message}</p>

          </div>

        ))}

      </div>

      <div className="chatbotpopup">

        <div className="chat-header">

          <div className="header-info">

            <h2 className="logo-txt">
              ChatBot
            </h2>

          </div>

        </div>

        <div className="chatbody">

          {messages.map((msg, index) => (

            <div
              key={index}
              className={
                msg.sender === "bot"
                  ? "message botmessage"
                  : "message usermessage"
              }
            >

              {msg.sender === "bot" && (

                <div className="boticon">
                  🤖
                </div>

              )}

              <div>

                <p className="messagetext">
                  {msg.text}
                </p>

                {msg.suggestions && (

                  <div className="suggestions">

                    {msg.suggestions.map((suggestion, i) => (

                      <button
                        key={i}
                        onClick={() => setMessage(suggestion)}
                      >
                        {suggestion}
                      </button>

                    ))}

                  </div>

                )}

              </div>

            </div>

          ))}

          {loading && (

            <div className="message botmessage">

              <div className="boticon">
                🤖
              </div>

              <p className="messagetext">
                Typing...
              </p>

            </div>

          )}

        </div>

        <div className="chat-footer">

          <form
            className="chat-form"
            onSubmit={(e) => e.preventDefault()}
          >

            <input
              type="text"
              placeholder="Message..."
              className="message-input"
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              required
            />

            <button
              type="button"
              className="materials-symbols-rounded"
              onClick={sendMessage}
            >

              <span className="material-symbols-outlined">
                send
              </span>

            </button>

          </form>

        </div>

      </div>

    </div>

  );

};

export default App;