import { ref } from 'vue'
import { defineStore } from "pinia";
import axios from 'axios';

export const useAccountStore = defineStore('account', () => {
  const ACCOUNT_API_URL = 'http://127.0.0.1:8000/accounts'
  const token = ref('')

  const logIn = ({username, password}) => {
    axios({
      method: 'POST',
      url: `${ACCOUNT_API_URL}/login/`,
      data: {
        username, password
      }
    })
      .then(res => {
        token.value = res.data.key
      })
      .catch(err => console.log(err))
  }

  const signUp = ({username, password1, password2, age, email, sub_product}) => {
    axios({
      method: 'POST',
      url: `${ACCOUNT_API_URL}/signup/`,
      data: {
        username,
        password1, 
        password2,
        age,
        email,
        sub_product
      }
    })
      .then(res => {
        console.log('회원가입 성공!')
      })
      .catch(err => console.log(err))
  }

  return {
    logIn, signUp
  }
})