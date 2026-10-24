import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Attach access token from memory (not localStorage)
api.interceptors.request.use(config => {
  const userStr = sessionStorage.getItem('axiom_lens_user')
  if (userStr) {
    // In real app, store token separately and attach here
    // config.headers.Authorization = `Bearer ${token}`
  }
  return config
})
