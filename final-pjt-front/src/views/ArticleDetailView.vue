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

  <!-- 댓글 목록 -->
  <div>
    <h3>댓글</h3>
    <ul v-if="Array.isArray(articleStore.comments) && articleStore.comments.length > 0">
      <li v-for="comment in articleStore.comments" :key="comment.id">
        <p><strong>{{ comment.user }}</strong> ( {{ formatDate(comment.created_at) }})</p>

        <div v-if="editingCommentId === comment.id">
          <textarea v-model="editedContent" rows="2"></textarea>
          <button @click="saveEdit(comment.id)">저장</button>
          <button @click="cancelEdit()">취소</button>
        </div>
        <div v-else>
          <p>{{ comment.content }}</p>
          <div v-if="comment.user === myUsername">
            <button @click="startEdit(comment)">수정</button>
            <button @click="deleteComment(comment.id)">삭제</button>
          </div>
        </div>
      </li>
    </ul>
    <p v-else>댓글이 없습니다.</p>
  </div>

  <!-- 댓글 작성 폼 -->
  <form v-if="accountStore.isLogIn" @submit.prevent="submitComment">
    <textarea v-model="newComment" rows="3" placeholder="댓글을 입력하세요" required></textarea>
    <button class="btn btn-primary">댓글 작성</button>
  </form>

  <!-- 로그인 안 한 경우 안내 -->
   <p v-else class="text-muted">댓글을 작성하려면 로그인이 필요합니다.</p>
</template>

<script setup>
import { onMounted, computed, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useArticleStore } from '@/stores/articles.js'
import { useAccountStore } from '@/stores/accounts'

const articleStore = useArticleStore()
const accountStore = useAccountStore()
const myUsername = computed(() => accountStore.username)

const editingCommentId = ref(null)
const editedContent = ref('')

const startEdit = (comment) => {
  editingCommentId.value = comment.id
  editedContent.value = comment.content
}

const cancelEdit = () => {
  editingCommentId.value = null
  editedContent.value = ''
}

const saveEdit = async (commentId) => {
  await articleStore.updateComment(commentId, editedContent.value)
  cancelEdit()
}

const deleteComment = async (commentId) => {
  if (confirm('정말 삭제하시겠습니까?')){
    await articleStore.deleteComment(commentId)
  }
}

const route = useRoute()
const router = useRouter()
const article = computed(() => articleStore.articleDetail)
const newComment = ref('')

const formatDate = (isoString) => {
  return new Date(isoString).toLocaleString()
}

onMounted(() => {
  articleStore.getArticleDetail(route.params.id)
  articleStore.getComments(route.params.id)
})

const submitComment = async () => {
  if (!newComment.value.trim()) return
  articleStore.createComment(route.params.id, newComment.value)
  newComment.value = ''
}

const onUpdateArticle = () => {
  router.push({ name: 'articleUpdateView', params: { id: route.params.id } })
}

const onDeleteArticle = () => {
  if (confirm('정말로 해당 게시글을 삭제하시겠습니까?')) {
    articleStore.deleteArticle(route.params.id)
  }
}

</script>

<style scoped></style>Z