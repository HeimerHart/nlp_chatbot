import { useState, useEffect } from "react";
import api from "./api";
import "./index.css";
import "./theme.css";


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

    try {

      const response = await api.get(
        "/api/conversations/user123"
      );

      setHistory(response.data);

    } catch(error){

      console.log(error);

    }

  };



  useEffect(() => {

    loadHistory();

  }, []);






  const sendMessage = async () => {


    if (!message.trim()) {
      return;
    }



    const userMessage = {

      sender:"user",
      text:message

    };



    setMessages(prev => [

      ...prev,
      userMessage

    ]);



    setLoading(true);



    try {


      const response = await api.post(

        "/api/chat",

        {
          session_id:"user123",
          message:message,
          context:context
        }

      );



      const botMessage = {

        sender:"bot",

        text:response.data.response,


        suggestions:[

          "Tell me more",
          "Help",
          "Thanks"

        ]

      };



      setMessages(prev => [

        ...prev,
        botMessage

      ]);




      setContext(prev => [

        ...prev,
        message,
        response.data.response

      ].slice(-5));




      setHistory(prev => [

        ...prev,

        {

          user_message:message,

          bot_response:response.data.response

        }

      ]);



    }

    catch(error){

      console.log(error);

    }



    setLoading(false);

    setMessage("");

  };



const logout = () => {
    localStorage.removeItem("token");
    window.location.reload();
};


return (

<div className="container">
    <div className="sidebar">
    <h3>History</h3>


    {history.slice(-10).map((chat,index)=>(


        <div key={index}

            style={{

            marginBottom:"10px",

            padding:"8px",

            background:"#ffffff20",

            borderRadius:"8px"

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

        <button
        className="logout-btn"
        onClick={logout}
    >
        Logout
    </button>






<div className="chatbody">

{messages.map((msg,index)=>(
    <div key={index} className={msg.sender==="bot"? "message botmessage":"message usermessage"}>

        {msg.sender==="bot" && (

            <div className="boticon">

            🤖

            </div>

)}

<p className="messagetext"> {msg.text}</p>

{msg.suggestions && (


<div className="suggestions">


{msg.suggestions.map((suggestion,i)=>(


<button

key={i}

onClick={()=>setMessage(suggestion)}

>

{suggestion}

</button>


))}



</div>


)}




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






            <form className="chat-form" onSubmit={(e)=>{e.preventDefault();sendMessage();}}>
            <input aria-label="Chat message" type="text" placeholder="Message:" className="message-input" 
            value={message} onChange={(e)=>setMessage(e.target.value
                
            )}/>
            <button aria-label="Chat message" type="submit" className="materials-symbols-rounded">
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

export default ChatBot;