<template>
  <div v-if="store.userInfo" class="mypage-container">
    <h2><strong>{{ store.userInfo.username }}</strong> 님의 프로필 페이지</h2>

    <div class="section-title">기본 정보 수정</div>

    <ul class="info-list">
      <li>
        <span class="label">회원번호</span>
        <span class="value">{{ store.userInfo.id }}</span>
      </li>
      <li>
        <span class="label">ID</span>
        <span class="value">{{ store.userInfo.username }}</span>
      </li>
      <li>
        <span class="label">Email</span>
        <span class="value">{{ store.userInfo.email || '이메일을 설정해주세요' }}</span>
        <button @click="editField('email')" class="edit-btn">수정하기</button>
      </li>
      <li>
        <span class="label">Nickname</span>
        <span v-if="!editing.nickname" class="value">{{ store.userInfo.nickname }}</span>
          <input v-else v-model="form.nickname" type="text" />
        <button @click="editField('nickname')" class="edit-btn">수정하기</button>
      </li>
      <li>
        <span class="label">나이</span>
        <span v-if="!editing.age" class="value">{{ store.userInfo.age }}</span>
          <input v-else v-model="form.age" type="number" />
        <button @click="editField('age')" class="edit-btn">수정하기</button>
      </li>
      <li>
        <span class="label">현재 가진 금액</span>
        <span v-if="!editing.current_amount" class="value">
          {{ typeof form.current_amount === 'number' ? form.current_amount.toLocaleString() : '금액 없음' }}
        </span>
          <input v-else v-model="form.current_amount" type="number" />
        <button @click="editField('current_amount')" class="edit-btn">수정하기</button>
      </li>
      <li>
        <span class="label">연봉</span>
        <span v-if="!editing.salary" class="value">
          {{ typeof form.salary === 'number' ? form.salary.toLocaleString() : '연봉 없음'}}
        </span>
          <input v-else v-model="form.salary" type="number" />
        <button @click="editField('salary')" class="edit-btn">수정하기</button>
      </li>
    </ul>

    <button @click="submitForm" class="submit-btn">모든 변경사항 저장</button>

    <UserProductChart
      v-if="store.userInfo"
      :term-products="store.userInfo.joined_term_products"
      :saving-products="store.userInfo.joined_saving_products"
    />
  </div>

  <div v-else>
    <p>로딩 중입니다...</p>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useAccountStore } from '@/stores/accounts'
import UserProductChart from '@/components/UserProductChart.vue'

const store = useAccountStore()

const form = ref({
  nickname: '',
  age: null,
  salary: null,
  current_amount: null,
})

const editing = ref({
  nickname: false,
  age: false,
  salary: false,
  current_amount: false,
})

const editField = (field) => {
  editing.value[field] = !editing.value[field]
}

onMounted(async () => {
  await store.fetchMyPage()
})

watch(
  () => store.userInfo,
  (newUserInfo) => {
    if (newUserInfo) {
      form.value.nickname = newUserInfo.nickname || ''
      form.value.age = newUserInfo.age ?? null
      form.value.salary = newUserInfo.salary ?? 0
      form.value.current_amount = newUserInfo.current_amount ?? 0
    }
  },
  { immediate: true }  // 새로고침 직후에도 즉시 실행되게 함!
)


const submitForm = async () => {
  await store.updateMyPage(form.value)
  alert('정보가 수정되었습니다!')
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

.mypage-container {
  max-width: 700px;
  margin: 0 auto;
  padding: 2rem;
  font-family: 'Noto Sans KR', sans-serif;
}

.section-title {
  font-size: 1.5rem;
  margin-bottom: 1rem;
  font-weight: bold;
  border-bottom: 2px solid #ddd;
  padding-bottom: 0.5rem;
}

.info-list {
  list-style: none;
  padding: 0;
}

.info-list li {
  display: flex;
  align-items: center;
  margin-bottom: 1rem;
  gap: 1rem;
}

.label {
  width: 150px;
  font-weight: bold;
}

.value {
  flex: 1;
}

input[type="text"],
input[type="number"] {
  flex: 1;
  padding: 0.4rem;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.edit-btn {
  background-color: #00bcd4;
  color: white;
  border: none;
  padding: 0.4rem 0.8rem;
  border-radius: 5px;
  cursor: pointer;
}

.edit-btn:hover {
  background-color: #0097a7;
}

.submit-btn {
  margin-top: 2rem;
  padding: 0.6rem 1.4rem;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}

.submit-btn:hover {
  background-color: #45a049;
}
</style>
