<template>
  <h1>회원가입 페이지</h1>
  <form @submit.prevent="onSignUp">
    <label for="username">ID (username):</label>
    <input type="text" id="username" class="my-3 ms-2" placeholder="아이디 입력" v-model="username" required />
    <br />

    <label for="nickname">Nickname:</label>
    <input type="text" id="nickname" class="my-3 ms-2" placeholder="닉네임 입력" v-model="nickname" required />
    <br />

    <label for="pwd">Password:</label>
    <input type="password" id="pwd" class="mb-3 ms-2" placeholder="비밀번호 입력" v-model="password1" required />
    <br />

    <label for="checkPwd">Confirm Password:</label>
    <input type="password" id="checkPwd" class="mb-3 ms-2" placeholder="비밀번호 확인" v-model="password2" required />
    <br />

    <label for="age">Age:</label>
    <input type="number" id="age" class="mb-3 ms-2" placeholder="나이 입력" v-model="age" required />
    <br />

    <label for="email">Email:</label>
    <input type="email" id="email" class="mb-3 ms-2" placeholder="이메일 입력" v-model="email" required />
    <br />

    <label for="salary">Salary (연봉):</label>
    <input type="number" id="salary" class="mb-3 ms-2" placeholder="연봉 입력" v-model="salary" required />
    <br />

    <label for="current_amount">Current Amount (자산):</label>
    <input type="number" id="current_amount" class="mb-3 ms-2" placeholder="현재 자산 입력" v-model="current_amount" required />
    <br />

    <label for="sub-product">Sub Product:</label>
    <input type="text" id="sub-product" class="mb-3 ms-2" placeholder="가입한 상품 목록" v-model="sub_product" />
    <br />

    <label for="profile_image">Profile Image:</label>
    <input type="file" id="profile_image" class="mb-3 ms-2" @change="onFileChange" />
    <br />

    <input type="submit" value="회원가입" />
  </form>
</template>

<script setup>
import { ref } from 'vue'
import { useAccountStore } from '@/stores/accounts.js'

const accountStore = useAccountStore()

const username = ref('')
const nickname = ref('')
const password1 = ref('')
const password2 = ref('')
const age = ref('')
const email = ref('')
const salary = ref('')
const current_amount = ref('')
const sub_product = ref('')
const profile_image = ref(null)

const onFileChange = (event) => {
  const file = event.target.files[0]
  if (file) {
    profile_image.value = file
  }
}

const onSignUp = () => {
  const formData = new FormData()
  formData.append('username', username.value)
  formData.append('nickname', nickname.value)
  formData.append('password1', password1.value)
  formData.append('password2', password2.value)
  formData.append('age', age.value)
  formData.append('email', email.value)
  formData.append('salary', salary.value)
  formData.append('current_amount', current_amount.value)
  formData.append('sub_product', sub_product.value)

  if (profile_image.value) {
    formData.append('profile_image', profile_image.value)
  }

  accountStore.signUp(formData)
}
</script>

<style scoped>
/* 원하는 스타일을 여기에 추가하세요 */
</style>
