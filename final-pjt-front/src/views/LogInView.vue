<template>
  <h1>로그인 페이지</h1>
  <form @submit.prevent="onLogIn">
    <input type="text" class="mb-2" v-model="username" placeholder="아이디"> <br>
    <input type="password" class="mb-2" v-model="password" placeholder="비밀번호"><br>
    <button>로그인</button>
  </form>

  <hr>

  <button @click="onSignUp">회원가입</button>
</template>

<script setup>
  import { ref } from 'vue'
  import { useRouter } from 'vue-router'
  import { useAccountStore } from '@/stores/accounts.js'
  
  const accountStore = useAccountStore()
  const router = useRouter()

  const username = ref('')
  const password = ref('')

  const onLogIn = () => {
    const userInfo = {
      username: username.value,
      password: password.value
    }
    accountStore.logIn(userInfo)
  }

  const onSignUp = () => {  
    router.push({ name: 'signUp'})
  }
</script>

<style scoped>

</style>