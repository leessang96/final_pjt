<template>
  <div>
    <ArticleListItem
      v-for="article in articleStore.articles"
      :key="article.id"
      :article="article"
    />

  </div>
</template>

<script setup>
  import { useArticleStore } from '@/stores/articles.js'
  import ArticleListItem from '@/components/ArticleListItem.vue'

  const articleStore = useArticleStore()
</script>

<style scoped>

</style>