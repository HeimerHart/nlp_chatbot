import { useEffect, useState } from "react";
import api from "./api";
import AnalyticsDashboard from "./AnalyticsDashboard";

function Admin() {

    const [users, setUsers] = useState([]);
    const [intents, setIntents] = useState([]);
    const [conversations, setConversations] = useState([]);

    useEffect(() => {
        loadData();
    }, []);

    const loadData = async () => {

        const token = localStorage.getItem("token");

        console.log(token);

        const config = {
            headers: {
                Authorization: `Bearer ${token}`
            }
        };

        const userResponse = await api.get(
            "/api/admin/users",
            config
        );

        const intentResponse = await api.get(
            "/api/admin/intents",
            config
        );

        const conversationResponse = await api.get(
            "/api/admin/conversations",
            config
        );

        setUsers(userResponse.data);
        setIntents(intentResponse.data);
        setConversations(conversationResponse.data);
    };

    return (

        <div style={{padding:"20px"}}>

            <h1>Admin Dashboard</h1>

            <hr/>

            <h2>Users</h2>

            {users.map((user,index)=>(

                <div key={index}>
                    {user.email} - {user.role}
                </div>

            ))}

            <hr/>

            <h2>Intents</h2>

            {intents.map((intent,index)=>(

                <div key={index}>
                    {intent.name}
                </div>

            ))}

            <hr/>

            <h2>Conversation Logs</h2>

            {conversations.map((chat,index)=>(

                <div key={index}>

                    <b>{chat.session_id}</b>

                    <br/>

                    {chat.user_message}

                    <br/>

                    {chat.bot_response}

                    <hr/>

                </div>

            ))}

            <hr />

<AnalyticsDashboard />

        </div>

    );

}

export default Admin;