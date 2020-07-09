import axios from 'axios'
import { Message } from 'element-ui'
import store from '@/store'

// create an axios instance
const service = axios.create({
  baseURL: process.env.VUE_APP_BASE_API, // url = base url + request url
  // withCredentials: true, // send cookies when cross-domain requests
  timeout: 10000 // request timeout
})

// request interceptor
service.interceptors.request.use(
  config => {
    // do something before request is sent
    config.headers['X-Requested-With'] = 'XMLHttpRequest'
    const token = store.getters.token
    if (token) {
      config.headers['Authorization'] = 'Bearer ' + token
    }
    return config
  },
  error => {
    // do something with request error
    if (process.env.NODE_ENV === 'development') {
      console.log(error) // for debug
    }
    return Promise.reject(error)
  }
)

// response interceptor
service.interceptors.response.use(
  /**
   * If you want to get http information such as headers or status
   * Please return  response => response
  */
  response => response,
  async error => {
    if (process.env.NODE_ENV === 'development') {
      console.log('err' + error) // for debug
    }

    let message = error.message

    if (error.response) {
      const res = error.response.data
      if (res.status) {
        if (res.data && res.data.message) {
          message = `${res.status}: ${res.data.message}`
        } else {
          message = res.status
        }
      }

      if (error.response.status === 401) {
        await store.dispatch('user/resetToken')
        location.reload()
      }
    }

    Message({
      message: message,
      type: 'error',
      duration: 5 * 1000
    })

    return Promise.reject(error)
  }
)

export default service
