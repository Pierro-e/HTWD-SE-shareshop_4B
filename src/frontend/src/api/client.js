import axios from "axios";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

if (!API_BASE_URL) {
  console.warn("VITE_API_BASE_URL is not defined");
}

export const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
});
