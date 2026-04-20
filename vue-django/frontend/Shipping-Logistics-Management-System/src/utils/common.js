
// common.js
import axios from 'axios'

export const api = axios.create({
  baseURL: 'http://127.0.0.1:8000',
  withCredentials: true
})

export const fixAvatar = (u) => { 
  u.avatar = 'http://127.0.0.1:8000/' + u.avatar
  return u
}