import { ref, computed } from 'vue'
import { defineStore } from "pinia";
import { useRouter } from 'vue-router';
import axios from 'axios';

export const useAccountStore = defineStore('account', () => {
  // const ACCOUNT_API_URL = 'http://127.0.0.1:8000/api/v1/accounts'
  const token = ref(localStorage.getItem('token'))
  const username = ref(localStorage.getItem('username') || '')
  const router = useRouter()

  const isLogIn = computed(() => !!token.value)

  const userInfo = ref(null)  

  const BASE_URL = 'http://127.0.0.1:8000'
  const ACCOUNT_API_URL = `${BASE_URL}/api/v1/accounts`
  const AUTH_API_URL = `${BASE_URL}/accounts`

  const logIn = ({username: inputUsername, password}) => {
    axios({
      method: 'POST',
      url: `${ACCOUNT_API_URL}/login/`,
      data: {
        username: inputUsername, 
        password
      }
    })
      .then(async res => {
        token.value = res.data.key
        // username.value = inputUsername
        localStorage.setItem('token', res.data.key)

        // const userRes = await axios.get(`${ACCOUNT_API_URL}/user/`,{
        const userRes = await axios.get(`${AUTH_API_URL}/user/`, {
          headers: {
            Authorization: `Token ${res.data.key}`
          }
        })
        username.value = userRes.data.username
        localStorage.setItem('username', userRes.data.username)
        router.push({ name: 'home'})
      })
      .catch(err => console.log(err))
  }

  const signUp = (formData) => {
    axios({
      method: 'POST',
      url: `${ACCOUNT_API_URL}/signup/`,
      data: formData,
      headers: {
        'Content-Type': 'multipart/form-data',
      }
    })
      .then(res => {
        console.log('회원가입 성공!')
        router.push({ name: 'logIn'})
      })
      .catch(err => console.log(err))
  }

  const logOut = () => {
    token.value = null
    username.value = ''
    localStorage.removeItem('token')
    localStorage.removeItem('username')
  }

  const fetchMyPage = () => {
    axios({
      method: 'GET',
      url: `${ACCOUNT_API_URL}/mypage/`,
      headers: {
        Authorization: `Token ${token.value}`
      }
    })
      .then(res => {
        userInfo.value = res.data
      })
      .catch(err => {
        console.error('마이페이지 불러오기 실패:', err)
      })
  }

  const updateMyPage = (formData) => {
    axios({
      method: 'POST',
      url: `${ACCOUNT_API_URL}/mypage/`,
      data: formData,
      headers: {
        Authorization: `Token ${token.value}`
      }
    })
      .then(res => {
        userInfo.value = res.data
      })
      .catch(err => {
        console.error('마이페이지 수정 실패:', err)
      })
    }
  return {
    logIn, signUp, logOut, token, username, isLogIn, userInfo, fetchMyPage, updateMyPage
  }
})