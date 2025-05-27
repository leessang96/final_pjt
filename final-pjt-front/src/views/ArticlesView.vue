<template>
  <h1>게시판</h1>
  <RouterLink :to="{ name: 'articleCreate'}" class="create-button">글 작성하기</RouterLink>
  <ArticleList/>
</template>

<script setup>
  import { RouterLink } from 'vue-router'
  import { onMounted } from 'vue'
  import { useArticleStore } from '@/stores/articles.js'
  import ArticleList from '@/components/ArticleList.vue'
  const articleStore = useArticleStore()

  onMounted(() => {
    articleStore.getArticles()
  })
</script>

<style scoped>
 .create-button {
  display: inline-block;
  padding: 0.5rem 1.2rem;
  background-color: #FFCB05;
  color: #222 !important;
  border-radius: 0.5rem;
  font-weight: 600;
  text-decoration: none !important;
  transition: background-color 0.2s ease;
  box-shadow: 0 2px 6px rgba(0,0,0,0.1);
  }


  .create-button:hover {
    background-color: #e5b800;
  }

</style>