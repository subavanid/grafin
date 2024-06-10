import axios from "axios";

const Axios = axios.create({
    // baseURL: "http://192.168.1.15:8000",
    baseURL: "http://127.0.0.1:8000"
    // baseURL: "http://localhost:4000",

});


export default Axios