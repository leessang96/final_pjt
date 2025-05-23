<template>
  <h1>게시글 작성</h1>
  <form @submit.prevent="onCreateArticle">
    <label for="title">제목 : </label>
    <input type="text" class="ms-2 my-2" id="title" v-model.trim="title">
    
    <br>

    <label for="content">내용 : </label>
    <textarea class="ms-2" id="content" v-model.trim="content"></textarea>

    <br>

    <button>글 쓰기</button>

  </form>
</template>

<script setup>
  import { ref } from 'vue'
  import { useArticleStore } from '@/stores/articles.js'

  const articleStore = useArticleStore()

  const title = ref('')
  const content = ref('')

  const onCreateArticle = () => {
    articleStore.createArticle(title.value, content.value)
  }
</script>

<style scoped>

</style>