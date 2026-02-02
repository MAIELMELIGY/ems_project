import axios from "axios";
import { useAuthStore } from "@/stores/auth";

export const http = axios.create({
  baseURL: import.meta.env.VITE_API_URL ?? "http://localhost:8000/api",
  timeout: 15000,
});

http.interceptors.request.use((config) => {
  const auth = useAuthStore();
  if (auth.accessToken) {
    config.headers = config.headers ?? {};
    config.headers.Authorization = `Bearer ${auth.accessToken}`;
  }
  return config;
});

// frontend/src/api/http.ts

http.interceptors.response.use(
  (response) => response,
  async (error) => {
    const auth = useAuthStore();
    const originalRequest = error.config;

    // If 401 error and we haven't tried refreshing yet
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      try {
        // Call your refresh token endpoint
        await auth.refreshAccessToken(); 
        // Update header and retry
        originalRequest.headers.Authorization = `Bearer ${auth.accessToken}`;
        return http(originalRequest);
      } catch (refreshError) {
        
        return Promise.reject(refreshError);
      }
    }

    const msg = error?.response?.data?.detail ?? "Unexpected error";
    return Promise.reject(new Error(msg));
  }
);
