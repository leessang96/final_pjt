<template>
  <div v-if="article">
    <h1>{{ article.id }}번째 글</h1>
    <p>제목 : {{ article.title }}</p>
    <p>내용 : {{ article.content }}</p>
    <p>생성시간 : {{ article.created_at }}</p>
    <p>내용 : {{ article.updated_at }}</p>

  </div>
</template>

<script setup>
  import { onMounted, ref } from 'vue'
  import { useRoute } from 'vue-router'
  import {useArticleStore} from '@/stores/articles.js'
  import axios from 'axios'

  const articleStore = useArticleStore()
  const route = useRoute()
  const article = ref(null)
  const token = localStorage.getItem('token')

  onMounted(() => {
    axios({
      method: 'get',
      url: `${articleStore.API_URL}/api/v1/articles/${route.params.id}/`,
      headers: {
        Authorization: `Token ${token}`
      }      
    })
      .then((res) => {
        article.value = res.data
      })
      .catch(err => console.log(err))

  })
</script>

<style scoped>

</style>