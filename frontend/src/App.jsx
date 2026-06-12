import "./theme.css";
import './index.css'
import { useState } from "react";
import api from "./api";





const App=()=>{
  const [message, setMessage] = useState("");

  const [messages, setMessages] = useState([
  {
    sender: "bot",
    text: "Good Day!\n"
  }
]);


const [loading, setLoading] = useState(false);






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
    message: message
  }
);

const botMessage = {
  sender: "bot",
  text: response.data.response
};






setMessages(prev => [
  ...prev,
  botMessage
]);
setLoading(false);







  setMessage("");
};








  return(
    <div className="container">
      <div className="chatbotpopup">
        {/*chat header */}
        <div className="chat-header">
          <div className="header-info">

            <h2 className="logo-txt">ChatBot</h2>
            </div>
            </div>




      
            {/*chat body*/}
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

      <p className="messagetext">
        {msg.text}
      </p>









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




            {/*chat footer */}
            <div className="chat-footer">
              <form action="#" className="chat-form">

                <input type="text" placeholder="Message: " className="message-input" value={message} onChange={(e) => setMessage(e.target.value)} required />


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
export default App