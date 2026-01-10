import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL

// Create Axios instance
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Global response interceptor
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      console.warn('Unauthorized! You might want to redirect to login here.')
      // window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export default apiClient
