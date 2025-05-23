<template>
  <h1>게시판</h1>
  <RouterLink :to="{ name: 'articleCreate'}">[CREATE]</RouterLink>
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

</style>