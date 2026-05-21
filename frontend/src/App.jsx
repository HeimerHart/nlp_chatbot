const App=()=>{
  return(
    <div className="Container">
      <div className="chatbotpopup">
        <div className="chat-header">
          <div className="header-info">
            <h2 className="logo-txt">ChatBot</h2>

            {/*chat body*/}
            <div className="chatbody">
              <div className="botmessage">
                <p className="messagetext">
                  Good Day!<br/>
                  How can I help you
                </p>

              </div>

              <div className="usermessage">
                nigga nigga nigga
              </div>

            </div>




            {/*chat footer */}
            <div className="chatfooter">
              <form action="#" className="chatform">
                <input type="text" placeholder="Message: " className="messageinput" required />
                <button className="materials-symbols-rounded"><span class="material-symbols-outlined">
                    send
                  </span>
                  </button>
                  
                                  

              </form>
            </div>
          </div>
        </div>
      </div>
    </div>





  );
};
export default App