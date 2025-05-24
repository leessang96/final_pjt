<template>
  <div v-if="article && article.id">
    <h1>{{ article.id }}번째 글</h1>
    <p>제목 : {{ article.title }}</p>
    <p>내용 : {{ article.content }}</p>
    <p>생성시간 : {{ article.created_at }}</p>
    <p>내용 : {{ article.updated_at }}</p>

    <button class="btn btn-warning" @click="onUpdateArticle">수정하기</button>
    <button class="btn btn-danger" @click="onDeleteArticle">삭제하기</button>
  </div>


  <hr>


</template>

<script setup>
import { onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useArticleStore } from '@/stores/articles.js'

const articleStore = useArticleStore()
const route = useRoute()
const router = useRouter()
const article = computed(() => articleStore.articleDetail)

onMounted(() => {
  articleStore.getArticleDetail(route.params.id)
})

const onUpdateArticle = () => {
  router.push({ name: 'articleUpdateView', params: { id: route.params.id } })
}

const onDeleteArticle = () => {
  if (confirm('정말로 해당 게시글을 삭제하시겠습니까?')) {
    articleStore.deleteArticle(route.params.id)
  }
}

</script>

<style scoped></style>