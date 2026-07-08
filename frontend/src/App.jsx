import "./theme.css";
import "./index.css";
import { useState, useEffect } from "react";
import api from "./api";
import Admin from "./AdminDashboard";
import Login from "./login"; 

const App = () => {

  const [loggedIn, setLoggedIn]= useState(
    !!localStorage.getItem("token")
  )
  
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

return <Admin />;

};

export default App;