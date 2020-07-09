import request from '@/utils/request'

export function login(data) {
  return request({
    url: '/token-auth/',
    method: 'post',
    data
  })
}

export function refresh() {
  return request.post('/token-refresh/')
}

export function getInfo() {
  return request({
    url: `/me/`,
    method: 'get'
  })
}

export function verify() {
  return request({
    url: '/token-verify/',
    method: 'post'
  })
}
