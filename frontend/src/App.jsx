import "./theme.css";
import "./index.css";
import { useState } from "react";
import Admin from "./AdminDashboard";
import Login from "./Login";
import ChatBot from "./chatbot";


const App = () => {

    const [loggedIn, setLoggedIn] = useState(
        !!localStorage.getItem("token")
    );

    const getRole = () => {

        const token = localStorage.getItem("token");

        if (!token) return null;

        const payload = JSON.parse(
            atob(token.split(".")[1])
        );

        return payload.role;
    };

    if (!loggedIn) {
        return <Login setLoggedIn={setLoggedIn} />;
    }

    if (getRole() === "admin") {
        return <Admin />;
    }

    return <Login />;

};

export default App;