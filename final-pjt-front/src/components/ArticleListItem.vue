<template>
  <div class="my-3">
    <h5>{{ article.id }}번째 글</h5>
    <p>제목 : {{ article.title }}</p>
    <p>내용 : {{ article.content }}</p>
    <RouterLink :to="{ name: 'articleDetailView', params: { id: article.id }}">
      [상세 보기]
    </RouterLink>
  </div>
  
  <hr>

</template>

<script setup>
  import { RouterLink } from 'vue-router'

  defineProps({
    article: Object
  })
</script>

<style scoped>

</style>