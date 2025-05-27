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

<style>

input, select, textarea {
  width: 100%;
  padding: 0.6rem;
  border-radius: 0.5rem;
  border: 1px solid #ccc;
  margin-top: 0.5rem;
  margin-bottom: 1rem;
  box-shadow: 0 1px 2px rgba(0,0,0,0.1);
}

button {
  background-color: #FFD700;
  border: none;
  padding: 0.6rem 1.2rem;
  border-radius: 0.5rem;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

button:hover {
  background-color: #e6c200;
}

.modal-overlay {
  position: fixed;
  top: 0; left: 0;
  width: 100%; height: 100%;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-card {
  background: white;
  padding: 2rem;
  border-radius: 1rem;
  width: 90%;
  max-width: 500px;
  box-shadow: 0 4px 10px rgba(0,0,0,0.3);
}


</style>