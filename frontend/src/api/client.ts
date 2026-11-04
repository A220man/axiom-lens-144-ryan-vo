import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Attach access token from sessionStorage
api.interceptors.request.use(config => {
  const tokenStr = sessionStorage.getItem('axiom_lens_token')
  if (tokenStr) {
    const token = JSON.parse(tokenStr)
    config.headers.Authorization = `Bearer ${token.access_token}`
  }
  return config
})

// Handle 401 responses
api.interceptors.response.use(
  response => response,
  error => {
    if (error.response?.status === 401) {
      // Clear session and redirect to login
      sessionStorage.removeItem('axiom_lens_user')
      sessionStorage.removeItem('axiom_lens_token')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)
