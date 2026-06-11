import axios from "axios";


const sessionId = "user123";
const api = axios.create({
    baseURL: "http://localhost:8000"
});


export default api;
