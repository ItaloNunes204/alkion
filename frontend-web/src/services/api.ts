import axios from "axios";

const api = axios.create({
    baseURL: "http://localhost:5000",
    headers: {
        "Content-Type": "application/json",
        "X-Client-Type": "web",
    },
});

api.interceptors.request.use((config) => {
    const token = localStorage.getItem("access_token");
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
});

api.interceptors.response.use(
    (response) => response,
    async (error) => {
        if (error.response?.status === 401) {
            const refresh = localStorage.getItem("refresh_token");
            if (refresh) {
                try {
                    const res = await axios.post(
                        "http://localhost:5000/api/v1/auth/refresh",
                        {},
                        {
                            headers: { Authorization: `Bearer ${refresh}` },
                        },
                    );
                    localStorage.setItem("access_token", res.data.access_token);
                    error.config.headers.Authorization = `Bearer ${res.data.access_token}`;
                    return axios(error.config);
                } catch {
                    localStorage.clear();
                    window.location.href = "/plans";
                }
            }
        }
        return Promise.reject(error);
    },
);

export default api;
