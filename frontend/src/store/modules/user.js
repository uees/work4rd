import { login, logout, getInfo } from '@/api/user'
import { getToken, setToken, removeToken } from '@/utils/auth'
import { resetRouter } from '@/router'

const getDefaultState = () => {
  return {
    url: '',
    username: '',
    nickname: '',
    avatar: '',
    first_name: '',
    last_name: '',
    email: '',
    groups: [],
    last_login: '',
    date_joined: '',
    updated_at: '',
    is_superuser: false,
    is_staff: false,
    is_active: false,
    token: getToken()
  }
}

const state = getDefaultState()

const mutations = {
  RESET_STATE: (state) => {
    Object.assign(state, getDefaultState())
  },
  SET_USER: (state, userInfo) => {
    Object.assign(state, {}, userInfo)
  },
  SET_TOKEN: (state, token) => {
    state.token = token
  }
}

const actions = {
  async login({ commit }, userInfo) {
    const { username, password } = userInfo
    const response = await login({ username: username.trim(), password: password })
    const { data } = response
    commit('SET_TOKEN', data.token)
    setToken(data.token)

    return data.token
  },

  // get user info
  async getInfo({ commit, state }) {
    const response = await getInfo()
    const { data } = response
    if (!data) {
      return reject('Verification failed, please Login again.')
    }

    commit('SET_USER', data)

    return data
  },

  // user logout
  async logout({ commit }) {
    removeToken() // must remove  token  first
    resetRouter()
    commit('RESET_STATE')
  },

  // remove token
  resetToken({ commit }) {
    return new Promise(resolve => {
      removeToken() // must remove  token  first
      commit('RESET_STATE')
      resolve()
    })
  }
}

export default {
  namespaced: true,
  state,
  mutations,
  actions
}

