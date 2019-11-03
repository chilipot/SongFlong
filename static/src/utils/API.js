import axios from "axios";

export default axios.create({
  baseURL: "http://10.60.163.239:5000",
  responseType: "json"
});
