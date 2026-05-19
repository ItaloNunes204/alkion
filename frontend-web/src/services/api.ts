import axios from 'axios'

const api = axios.create({
  baseURL: 'http://localhost:5000',
  headers: {
    'Content-Type': 'application/json',
    'X-Client-Type': 'web',
  },
})

export default api