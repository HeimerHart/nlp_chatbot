import { useState, useEffect, useRef, useMemo } from "react";
import api, { getSessionId } from "./api";
import ChatbotIcon from "./components/Chatboticon";
import OrderStatusCard from "./components/OrderStatusCard";
import RefundTimelineCard from "./components/RefundTimelineCard";
import "./index.css";
import "./theme.css";

const newConversationId = () =>
  typeof crypto !== "undefined" && crypto.randomUUID
    ? crypto.randomUUID()
    : `conv-${Date.now()}-${Math.random().toString(36).slice(2)}`;

const formatThreadTime = (timestamp) => {
  if (!timestamp) return "";
  const date = new Date(timestamp);
  if (Number.isNaN(date.getTime())) return "";
  return date.toLocaleString(undefined, {
    month: "short",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
};

const CARD_COMPONENTS = {
  order_status: OrderStatusCard,
  refund_timeline: RefundTimelineCard,
};

const renderCard = (card) => {
  if (!card) return null;
  const Card = CARD_COMPONENTS[card.type];
  if (!Card) return null;
  return <Card data={card} />;
};

const GREETING_MESSAGE = {
  sender: "bot",
  text: "Good day. What can I help you with?",
};

const ChatBot = () => {
  const sessionId = useMemo(() => getSessionId(), []);
  const [context, setContext] = useState([]);
  const [threads, setThreads] = useState([]);
  const [conversationId, setConversationId] = useState(null);
  const [message, setMessage] = useState("");
  const [historyOpen, setHistoryOpen] = useState(false);

  const [messages, setMessages] = useState([GREETING_MESSAGE]);

  const [loading, setLoading] = useState(false);
  const bodyRef = useRef(null);

  const loadThreads = async () => {
    try {
      const response = await api.get(`/api/conversations/threads/${sessionId}`);
      setThreads(response.data);
    } catch (error) {
      console.log(error);
    }
  };

  useEffect(() => {
    loadThreads();
  }, []);

  useEffect(() => {
    if (bodyRef.current) {
      bodyRef.current.scrollTop = bodyRef.current.scrollHeight;
    }
  }, [messages, loading]);

  const startNewChat = () => {
    setConversationId(null);
    setContext([]);
    setMessages([GREETING_MESSAGE]);
    setHistoryOpen(false);
  };

  const openThread = async (threadId) => {
    setHistoryOpen(false);
    try {
      const response = await api.get(`/api/conversations/${sessionId}/thread/${threadId}`);
      const restored = response.data.flatMap((chat) => [
        { sender: "user", text: chat.user_message },
        {
          sender: "bot",
          text: chat.bot_response,
          quickReplies: chat.quick_replies || [],
          card: chat.card || null,
        },
      ]);
      setConversationId(threadId);
      setContext(
        response.data.flatMap((chat) => [chat.user_message, chat.bot_response]).slice(-5)
      );
      setMessages(restored.length > 0 ? restored : [GREETING_MESSAGE]);
    } catch (error) {
      console.log(error);
    }
  };

  const sendMessage = async (text) => {
    const outgoing = (text ?? message).trim();
    if (!outgoing) return;

    const activeConversationId = conversationId || newConversationId();
    if (!conversationId) {
      setConversationId(activeConversationId);
    }

    const userMessage = { sender: "user", text: outgoing };
    setMessages((prev) => [...prev, userMessage]);
    setLoading(true);
    setMessage("");

    try {
      const response = await api.post("/api/chat", {
        session_id: sessionId,
        message: outgoing,
        context: context,
        conversation_id: activeConversationId,
      });

      const botMessage = {
        sender: "bot",
        text: response.data.response,
        quickReplies: response.data.quick_replies || [],
        card: response.data.card || null,
      };

      setMessages((prev) => [...prev, botMessage]);
      setContext((prev) => [...prev, outgoing, response.data.response].slice(-5));

      loadThreads();
    } catch (error) {
      console.log(error);
      setMessages((prev) => [
        ...prev,
        {
          sender: "bot",
          text: "Something went wrong on our end. Please try again in a moment.",
        },
      ]);
    }

    setLoading(false);
  };

  const logout = () => {
    localStorage.removeItem("token");
    window.location.reload();
  };

  const isEmptyState = messages.length === 1;

  return (
    <div className="stage">
      <div className={`app-shell ${historyOpen ? "history-open" : ""}`}>
        <aside className="history-rail">
          <div className="history-rail-head">
            <span className="eyebrow">Conversations</span>
            <button
              className="icon-btn history-close"
              onClick={() => setHistoryOpen(false)}
              aria-label="Close history"
            >
              <span className="material-symbols-outlined">close</span>
            </button>
          </div>

          <button className="new-chat-btn" onClick={startNewChat}>
            <span className="material-symbols-outlined">add</span>
            New chat
          </button>

          <div className="history-list">
            {threads.length === 0 && (
              <p className="history-empty">No conversations yet.</p>
            )}
            {threads.map((thread) => (
              <button
                key={thread.conversation_id}
                className={`thread-item ${thread.conversation_id === conversationId ? "active" : ""}`}
                onClick={() => openThread(thread.conversation_id)}
              >
                <p className="thread-item-title">{thread.title}</p>
                <span className="thread-item-meta">
                  {formatThreadTime(thread.last_message_at)}
                </span>
              </button>
            ))}
          </div>
        </aside>

        <main className="chat-panel">
          <header className="chat-header">
            <div className="chat-header-info">
              <button
                className="icon-btn history-toggle"
                onClick={() => setHistoryOpen(true)}
                aria-label="Open history"
              >
                <span className="material-symbols-outlined">history</span>
              </button>
              <span className="bot-mark">
                <ChatbotIcon size={20} />
              </span>
              <div>
                <h1 className="chat-title">ChatBot</h1>
                <p className="chat-subtitle">Signed in as {sessionId}</p>
              </div>
            </div>
            <button className="text-btn" onClick={logout}>
              Log out
            </button>
          </header>

          <div className="chat-body" ref={bodyRef}>
            {isEmptyState && (
              <div className="hero">
                <span className="hero-mark">
                  <ChatbotIcon size={30} />
                </span>
                <h2 className="hero-title">
                  Good day. <em>How can we help?</em>
                </h2>
                <p className="hero-subtitle">
                  Ask about an order, a refund, or anything else — I'm listening.
                </p>
              </div>
            )}

            {!isEmptyState &&
              messages.map((msg, index) => (
                <div
                  className={`message ${msg.sender === "bot" ? "bot-message" : "user-message"}`}
                  key={index}
                >
                  {msg.sender === "bot" && (
                    <span className="message-avatar">
                      <ChatbotIcon size={16} />
                    </span>
                  )}
                  <div className="message-column">
                    <p className="message-text">{msg.text}</p>

                    {msg.card && renderCard(msg.card)}

                    {msg.quickReplies && msg.quickReplies.length > 0 && (
                      <div className="suggestions">
                        {msg.quickReplies.map((suggestion, i) => (
                          <button key={i} onClick={() => sendMessage(suggestion)}>
                            {suggestion}
                          </button>
                        ))}
                      </div>
                    )}
                  </div>
                </div>
              ))}

            {loading && (
              <div className="message bot-message">
                <span className="message-avatar">
                  <ChatbotIcon size={16} />
                </span>
                <div className="message-column">
                  <p className="message-text typing">
                    <span />
                    <span />
                    <span />
                  </p>
                </div>
              </div>
            )}
          </div>

          <div className="chat-footer">
            <form
              className="chat-form"
              onSubmit={(e) => {
                e.preventDefault();
                sendMessage();
              }}
            >
              <input
                aria-label="Message"
                type="text"
                placeholder="Message"
                className="message-input"
                value={message}
                onChange={(e) => setMessage(e.target.value)}
              />
              <button aria-label="Send message" type="submit" className="send-btn">
                <span className="material-symbols-outlined">arrow_upward</span>
              </button>
            </form>
          </div>
        </main>
      </div>

      {historyOpen && (
        <div className="scrim" onClick={() => setHistoryOpen(false)} aria-hidden="true" />
      )}
    </div>
  );
};

export default ChatBot;
