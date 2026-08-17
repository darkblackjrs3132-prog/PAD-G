import axios from "axios";
export const api = axios.create({baseURL: import.meta.env.VITE_API_URL || "http://localhost:8000/api", timeout:15000});
export const buildParams = f => Object.fromEntries(Object.entries(f).filter(([,v])=>v));
