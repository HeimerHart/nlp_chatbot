import axios from "axios";


const sessionId = "user123";
const api = axios.create({
    baseURL: "http://localhost:8000"
});

const [message, setMessage] = useState("");

const [messages, setMessages] = useState([]);

const [loading, setLoading] = useState(false);

const [error, setError] = useState("");

export default api;
