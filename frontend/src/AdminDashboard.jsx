import { useEffect, useState } from "react";
import api from "./api";
import AnalyticsDashboard from "./AnalyticsDashboard";
import ChatbotIcon from "./components/Chatboticon";
import "./theme.css";
import "./AdminDashboard.css";

const formatTime = (timestamp) => {
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

function Admin() {
  const [users, setUsers] = useState([]);
  const [intents, setIntents] = useState([]);
  const [conversations, setConversations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [loadError, setLoadError] = useState("");
  const [search, setSearch] = useState("");
  const [openSessions, setOpenSessions] = useState({});

  const loadData = async () => {
    setLoading(true);
    setLoadError("");

    try {
      const [userResponse, intentResponse, conversationResponse] = await Promise.all([
        api.get("/api/admin/users"),
        api.get("/api/admin/intents"),
        api.get("/api/admin/conversations"),
      ]);

      setUsers(userResponse.data);
      setIntents(intentResponse.data);
      setConversations(conversationResponse.data);
    } catch (error) {
      console.log(error);
      setLoadError(
        error?.response?.status === 403
          ? "You don't have permission to view admin data."
          : "Couldn't load admin data. Check your connection and try again."
      );
    }

    setLoading(false);
  };

  useEffect(() => {
    loadData();
  }, []);

  const logout = () => {
    localStorage.removeItem("token");
    window.location.reload();
  };

  const sessions = conversations.reduce((acc, chat) => {
    const key = chat.session_id || "unknown";
    if (!acc[key]) acc[key] = [];
    acc[key].push(chat);
    return acc;
  }, {});

  const sessionEntries = Object.entries(sessions)
    .filter(([sessionId, chats]) => {
      if (!search.trim()) return true;
      const query = search.toLowerCase();
      return (
        sessionId.toLowerCase().includes(query) ||
        chats.some(
          (chat) =>
            chat.user_message?.toLowerCase().includes(query) ||
            chat.bot_response?.toLowerCase().includes(query)
        )
      );
    })
    .sort((a, b) => {
      const lastA = a[1][a[1].length - 1]?.timestamp || "";
      const lastB = b[1][b[1].length - 1]?.timestamp || "";
      return lastB.localeCompare(lastA);
    });

  const toggleSession = (sessionId) => {
    setOpenSessions((prev) => ({ ...prev, [sessionId]: !prev[sessionId] }));
  };

  return (
    <div className="admin-stage">
      <header className="admin-header">
        <div className="admin-header-info">
          <span className="admin-mark">
            <ChatbotIcon size={16} />
          </span>
          <div>
            <h1 className="admin-title">ChatBot</h1>
            <span className="eyebrow">Admin</span>
          </div>
        </div>
        <div className="admin-header-actions">
          <button className="icon-btn" onClick={loadData} aria-label="Refresh">
            <span className="material-symbols-outlined">refresh</span>
          </button>
          <button className="text-btn" onClick={logout}>
            Log out
          </button>
        </div>
      </header>

      <main className="admin-body">
        {loadError && (
          <div className="admin-alert">
            <span>{loadError}</span>
            <button className="text-btn" onClick={loadData}>
              Retry
            </button>
          </div>
        )}

        <section className="admin-section">
          <div className="admin-section-head">
            <h2>Overview</h2>
          </div>
          <AnalyticsDashboard />
        </section>

        <div className="admin-grid">
          <section className="admin-section">
            <div className="admin-section-head">
              <h2>Users</h2>
              <span className="pill-count">{users.length}</span>
            </div>
            <div className="admin-card admin-card-scroll-sm">
              {loading && <p className="admin-empty">Loading…</p>}
              {!loading && users.length === 0 && (
                <p className="admin-empty">No users yet.</p>
              )}
              {users.map((user, index) => (
                <div className="admin-row" key={index}>
                  <span>{user.email}</span>
                  <span className={`role-tag ${user.role === "admin" ? "role-admin" : ""}`}>
                    {user.role}
                  </span>
                </div>
              ))}
            </div>
          </section>

          <section className="admin-section">
            <div className="admin-section-head">
              <h2>Intents</h2>
              <span className="pill-count">{intents.length}</span>
            </div>
            <div className="admin-card admin-card-scroll-sm">
              {loading && <p className="admin-empty">Loading…</p>}
              {!loading && intents.length === 0 && (
                <p className="admin-empty">No intents configured.</p>
              )}
              <div className="chip-row">
                {intents.map((intent, index) => (
                  <span className="chip" key={index}>
                    {intent.name}
                  </span>
                ))}
              </div>
            </div>
          </section>
        </div>

        <section className="admin-section">
          <div className="admin-section-head admin-section-head-row">
            <h2>Conversation logs</h2>
            <span className="pill-count">{conversations.length}</span>
          </div>
          <input
            className="admin-search"
            type="text"
            placeholder="Search by session or message…"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
          <div className="admin-card admin-card-scroll">
            {loading && <p className="admin-empty">Loading…</p>}
            {!loading && sessionEntries.length === 0 && (
              <p className="admin-empty">No conversations yet.</p>
            )}
            {sessionEntries.map(([sessionId, chats]) => {
              const isOpen = !!openSessions[sessionId];
              const lastChat = chats[chats.length - 1];
              return (
                <div className="session-group" key={sessionId}>
                  <button
                    className="session-summary"
                    onClick={() => toggleSession(sessionId)}
                  >
                    <span className="session-summary-main">
                      <span className="log-session">{sessionId}</span>
                      <span className="session-preview">{lastChat?.user_message}</span>
                    </span>
                    <span className="session-summary-meta">
                      <span className="pill-count">{chats.length}</span>
                      <span className="session-time">{formatTime(lastChat?.timestamp)}</span>
                      <span className="material-symbols-outlined">
                        {isOpen ? "expand_less" : "expand_more"}
                      </span>
                    </span>
                  </button>

                  {isOpen && (
                    <div className="session-thread">
                      {chats.map((chat, index) => (
                        <div className="log-entry" key={index}>
                          <span className="log-time">{formatTime(chat.timestamp)}</span>
                          <p className="log-line">
                            <strong>User</strong> {chat.user_message}
                          </p>
                          <p className="log-line">
                            <strong>Bot</strong> {chat.bot_response}
                          </p>
                          {chat.intent && (
                            <span className="chip chip-small">{chat.intent}</span>
                          )}
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        </section>
      </main>
    </div>
  );
}

export default Admin;
