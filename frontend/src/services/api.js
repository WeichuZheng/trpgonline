import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Lazy router reference to avoid circular imports
let router = null
export function setRouter(r) {
  router = r
}

// Request interceptor - add auth token, fix FormData Content-Type
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    // Let browser set Content-Type with boundary for FormData
    if (config.data instanceof FormData) {
      delete config.headers['Content-Type']
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor - handle errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response) {
      const { status, data } = error.response

      if (status === 401) {
        localStorage.removeItem('token')
        if (router && !window.location.pathname.includes('/login')) {
          router.push({ name: 'login', query: { redirect: window.location.pathname } })
        } else if (!window.location.pathname.includes('/login')) {
          window.location.href = '/login'
        }
      }

      // FastAPI validation errors return detail as array of objects
      let message = '请求失败'
      if (data?.detail) {
        if (typeof data.detail === 'string') {
          message = data.detail
        } else if (Array.isArray(data.detail)) {
          message = data.detail.map(e => {
            const field = e.loc?.slice(1).join('.') || ''
            const msg = e.msg || String(e)
            return field ? `${field}: ${msg}` : msg
          }).join('; ')
        } else {
          message = String(data.detail)
        }
      } else if (data?.message) {
        message = String(data.message)
      } else if (data?.error) {
        message = String(data.error)
      }
      return Promise.reject(new Error(message))
    }

    if (error.request) {
      return Promise.reject(new Error('网络连接失败，请检查网络'))
    }

    return Promise.reject(error)
  }
)

export default api
