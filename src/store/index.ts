import { createStore, Store } from 'vuex'
import { InjectionKey } from 'vue'

// 声明store实例
let store: Store<RootState>

// 定义User类型
interface User {
  id: string
  username: string
  role: string
  email: string
}

// 定义state类型
interface AuthState {
  user: User | null
  token: string | null
  refreshToken: string | null
  loading: boolean
  error: string | null
}

// 定义根state类型
interface RootState {
  auth: AuthState
}

// 定义store类型
export const key: InjectionKey<Store<RootState>> = Symbol()

import axios from 'axios'
import router from '../router'
import config from '../config'

// 创建模块化的store
const authModule = {
  namespaced: true,
  state: () => ({
    user: null,
    token: localStorage.getItem('token') || null,
    refreshToken: localStorage.getItem('refreshToken') || null,
    loading: false,
    error: null
  }),
  mutations: {
    SET_USER(state, user) {
      state.user = user
    },
    SET_TOKEN(state, { token, refreshToken }) {
      state.token = token
      state.refreshToken = refreshToken
      localStorage.setItem('token', token)
      localStorage.setItem('refreshToken', refreshToken)
    },
    SET_LOADING(state, loading) {
      state.loading = loading
    },
    SET_ERROR(state, error) {
      state.error = error
    },
    CLEAR_AUTH(state) {
      state.user = null
      state.token = null
      state.refreshToken = null
      localStorage.removeItem('token')
      localStorage.removeItem('refreshToken')
    }
  },
  actions: {
    async login({ commit }, credentials) {
      commit('SET_LOADING', true)
      try {
        const response = await apiClient.post('/login', credentials)
        commit('SET_TOKEN', {
          token: response.data.token,
          refreshToken: response.data.refreshToken
        })
        commit('SET_USER', response.data.user)
        router.push('/')
      } catch (error) {
        commit('SET_ERROR', error.response?.data?.message || 'Login failed')
        throw error
      } finally {
        commit('SET_LOADING', false)
      }
    },
    async logout({ commit }) {
      commit('CLEAR_AUTH')
      router.push('/login')
    },
    async register({ commit }, userData) {
      commit('SET_LOADING', true)
      try {
        await apiClient.post('/register', userData)
        router.push('/login')
      } catch (error) {
        commit('SET_ERROR', error.response?.data?.message || 'Registration failed')
        throw error
      } finally {
        commit('SET_LOADING', false)
      }
    },
    async fetchCurrentUser({ commit, state }) {
      if (!state.token) return
      
      commit('SET_LOADING', true)
      try {
        const response = await apiClient.get('/current_user')
        commit('SET_USER', response.data)
      } catch (error) {
        commit('CLEAR_AUTH')
        throw error
      } finally {
        commit('SET_LOADING', false)
      }
    }
  },
  getters: {
    isAuthenticated: state => !!state.token,
    currentUser: state => state.user,
    userRole: state => state.user?.role,
    isLoading: state => state.loading,
    error: state => state.error
  }
}

// 创建axios实例
const apiClient = axios.create({
  baseURL: config.apiEndpoints.baseUrl,
  timeout: 10000
})

// 请求拦截器
apiClient.interceptors.request.use(
  config => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

// 响应拦截器
apiClient.interceptors.response.use(
  response => response,
  async error => {
    const originalRequest = error.config
    
    // Token过期处理
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true
      
      try {
        const refreshToken = localStorage.getItem('refreshToken')
        const response = await axios.post(`${config.apiEndpoints.baseUrl}/refresh`, {
          refreshToken
        })
        
        localStorage.setItem('token', response.data.token)
        apiClient.defaults.headers.common['Authorization'] = `Bearer ${response.data.token}`
        return apiClient(originalRequest)
      } catch (refreshError) {
        // 使用模块化的commit方式
        store.commit('auth/CLEAR_AUTH')
        router.push('/login')
        return Promise.reject(refreshError)
      }
    }
    
    // 统一错误处理
    if (error.response) {
      const errorMessage = error.response.data?.message || 
        error.response.statusText || 
        '请求失败，请稍后重试'
      store.commit('auth/SET_ERROR', errorMessage)
    }
    
    return Promise.reject(error)
  }
)

store = createStore<RootState>({
  modules: {
    auth: authModule
  }
})

export default store
