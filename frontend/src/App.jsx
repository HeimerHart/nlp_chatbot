import "./theme.css";
import './index.css'
const App=()=>{
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
              
              <div className="message botmessage">


                <div className="boticon">
    🤖
  </div>


                <p className="messagetext">
                  Good Day!<br/>
                  How can I help you
                </p>

              </div>

              <div className="message usermessage">
                <p className="messagetext">Hi there</p>
              </div>
            </div>




            {/*chat footer */}
            <div className="chat-footer">
              <form action="#" className="chat-form">
                <input type="text" placeholder="Message: " className="message-input" required />
                <button className="materials-symbols-rounded"><span className="material-symbols-outlined">
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