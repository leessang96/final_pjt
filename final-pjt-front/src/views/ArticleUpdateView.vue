<template>
    <h1>게시글 수정</h1>
    <form @submit.prevent="onUpdateArticle">
        <label for="updateTitle">제목 : </label>
        <input type="text" class="ms-2 mb-3" id="updateTitle" v-model="title"> <br>
        <label for="updateContent" class="mb-3">내용 : </label>
        <textarea id="updateContent" class="ms-2" v-model="content"></textarea> <br>
        <button class="btn btn-warning">수정하기</button>
    </form>
</template>

<script setup>
import { onMounted, ref, computed, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useArticleStore } from '@/stores/articles.js'
const route = useRoute()
const articleStore = useArticleStore()

const title = ref('')
const content = ref('')
const article = computed(() => articleStore.articleDetail)

onMounted(() => {
    articleStore.getArticleDetail(route.params.id)
})

watch(article, (newArticle) => {
    if (newArticle) {
        title.value = newArticle.title || ''
        content.value = newArticle.content || ''
    }
})

const onUpdateArticle = () => {
    articleStore.updateArticle(route.params.id, title.value, content.value)
}

</script>

<style scoped></style>