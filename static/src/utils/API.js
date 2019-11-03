import axios from "axios";

export const BASE_URL = "http://10.60.163.239:5000";

export default axios.create({
  baseURL: BASE_URL,
  responseType: "json"
});
