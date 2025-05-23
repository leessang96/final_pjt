<template>
  <h1>회원가입 페이지</h1>
  <form @submit.prevent="onSignUp">
    <label for="username">id : </label>
    <input type="text" id="username" class="my-3 ms-2" placeholder="아이디 혹은 이메일 입력" v-model="username">
    <br>
    <label for="pwd">pwd : </label>
    <input type="password" id="pwd" class="mb-3 ms-2" placeholder="비밀번호 입력" v-model="password1">
    <br>
    <label for="checkPwd">checkPwd : </label>
    <input type="password" id="checkPwd" class="mb-3 ms-2" placeholder="비밀번호 확인" v-model="password2">
    <br>
    <label for="age">age : </label>
    <input type="number" id="age" class="mb-3 ms-2" placeholder="나이 입력" v-model="age" required>
    <br>
    <label for="email">email : </label>
    <input type="email" id="email" class="mb-3 ms-2" placeholder="이메일 입력" v-model="email" required>
    <br>
    <label for="sub-product">sub-product</label>
    <input type="text" id="sub-product" class="mb-3 ms-2" placeholder="가입한 상품 목록" v-model="sub_product">
    <br>
    <input type="submit" value="signup">
  </form>
</template>

<script setup>
  import { ref } from 'vue'
  import { useAccountStore } from '@/stores/accounts.js'

  const accountStore = useAccountStore()

  const username = ref('')
  const password1 = ref('')
  const password2 = ref('')
  const age = ref('')
  const email = ref('')
  const sub_product = ref('')

  const onSignUp = () => {
    const userInfo = {
      username: username.value,
      password1: password1.value,
      password2: password2.value,
      age: age.value,
      email: email.value,
      sub_product: sub_product.value
    }
    accountStore.signUp(userInfo)
  }
</script>

<style scoped>

</style>