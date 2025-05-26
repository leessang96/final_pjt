import { ref, computed } from 'vue'
import { defineStore } from "pinia";
import { useRouter } from 'vue-router';
import axios from 'axios';

export const useAccountStore = defineStore('account', () => {
  const ACCOUNT_API_URL = 'http://127.0.0.1:8000/accounts'
  const token = ref(localStorage.getItem('token'))
  const username = ref(localStorage.getItem('username') || '')
  const router = useRouter()

  const isLogIn = computed(() => !!token.value)

  const userInfo = ref(null)  

  const logIn = ({username: inputUsername, password}) => {
    axios({
      method: 'POST',
      url: `${ACCOUNT_API_URL}/login/`,
      data: {
        username: inputUsername, 
        password
      }
    })
      .then(res => {
        token.value = res.data.key
        username.value = inputUsername
        localStorage.setItem('token', res.data.key)
        localStorage.setItem('username', inputUsername)
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