<template>
  <h1>회원가입 페이지</h1>
  <form @submit.prevent="onSignUp">
    <div class="form-group">
      <label for="username">ID (username):</label>
      <input type="text" id="username" class="my-3 ms-2" placeholder="아이디 입력" v-model="username" required />
    </div>

    <div class="form-group">
      <label for="nickname">Nickname:</label>
      <input type="text" id="nickname" class="my-3 ms-2" placeholder="닉네임 입력" v-model="nickname" required />
    </div>

    <div class="form-group">
      <label for="pwd">Password:</label>
      <input type="password" id="pwd" class="mb-3 ms-2" placeholder="비밀번호 입력" v-model="password1" required />
    </div>

    <div class="form-group">
      <label for="checkPwd">Confirm Password:</label>
      <input type="password" id="checkPwd" class="mb-3 ms-2" placeholder="비밀번호 확인" v-model="password2" required />
    </div>

    <div class="form-group">
      <label for="age">Age:</label>
      <input type="number" id="age" class="mb-3 ms-2" placeholder="나이 입력" v-model="age" required />
    </div>

    <div class="form-group">
      <label for="email">Email:</label>
      <input type="email" id="email" class="mb-3 ms-2" placeholder="이메일 입력" v-model="email" required />
    </div>

    <div class="form-group">
      <label for="salary">Salary (연봉):</label>
      <input type="number" id="salary" class="mb-3 ms-2" placeholder="연봉 입력" v-model="salary" required />
    </div>

    <div class="form-group">
      <label for="current_amount">Current Amount (자산):</label>
      <input type="number" id="current_amount" class="mb-3 ms-2" placeholder="현재 자산 입력" v-model="current_amount" required />
    </div>

    <div class="form-group">
      <label for="profile_image">Profile Image:</label>
      <input type="file" id="profile_image" class="mb-3 ms-2" @change="onFileChange" />
    </div>

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

  if (profile_image.value) {
    formData.append('profile_image', profile_image.value)
  }

  accountStore.signUp(formData)
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

/* 원하는 스타일을 여기에 추가하세요 */
</style>
