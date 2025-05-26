import { useRouter } from "vue-router";
import { defineStore } from "pinia";
import { ref } from 'vue'
import axios from 'axios'

export const useArticleStore = defineStore('article', () => {
  const articles = ref([])
  const articleDetail = ref(null)
  const comments = ref([])
  const token = localStorage.getItem('token')
  const API_URL = 'http://127.0.0.1:8000'
  const router = useRouter()

  // 게시글 전체 리스트
  const getArticles = () => {
    axios({
      method: 'get',
      url: `${API_URL}/api/v1/articles/`,
      headers: {
        Authorization: `Token ${token}`
      }
    })
      .then(res => {
        articles.value = res.data
      })
      .catch(err => console.log(err))
  }

  // 게시글 디테일 get
  const getArticleDetail = (articleId) => {
    axios({
      method: 'get',
      url: `${API_URL}/api/v1/articles/${articleId}/`,
      headers: {
        Authorization: `Token ${token}`
      }
    })
      .then((res) => {
        articleDetail.value = { ...res.data }
      })
      .catch(err => console.log(err))
  }

  
  const getComments = (articleId) => {
    axios({
      method: 'get',
      url: `${API_URL}/api/v1/articles/${articleId}/comments/`,
      headers: {
        Authorization: `Token ${token}`
      }
    })
      .then((res) => {
        comments.value = res.data
      })
      .catch(err => console.log('댓글 불러오기 실패 :', err))
  }

  const createComment = (articleId, content) => {
    axios({
      method: 'post',
      url: `${API_URL}/api/v1/articles/${articleId}/comments/`,
      data: {content},
      headers: {
        Authorization: `Token ${token}`
      }
    })
      .then((res) => {
        comments.value.push(res.data)
        console.log(comments.value)
      })
      .catch(err => {
        console.log('댓글 작성 실패 : ', err)
        console.log('응답 내용:', err.response?.data)  // 디버깅용
      })
        
  }

  const updateComment = (commentId, newContent) => {
    axios({
      method: 'put',
      url: `${API_URL}/api/v1/articles/comments/${commentId}/`,
      data: {
        content: newContent
      },
      headers: {
        Authorization: `Token ${token}`
      }
    })
      .then((res) => {
        const idx = comments.value.findIndex(c => c.id === commentId)
        if(idx !== -1) comments.value[idx] = res.data
      })
      .catch(err => console.log('댓글 수정 실패: ', err))
  }


  const deleteComment = (commentId) => {
    axios({
      method: 'delete',
      url: `${API_URL}/api/v1/articles/comments/${commentId}/`,
      headers: {
        Authorization: `Token ${token}`
      }
    })
      .then((res) => {
        comments.value = comments.value.filter(c => c.id !== commentId)
      })
      .catch(err => console.log('댓글 삭제 실패: ', err))
  }


  // 게시글 생성 post
  const createArticle = (title, content) => {
    axios({
      method: 'POST',
      url: `${API_URL}/api/v1/articles/`,
      headers: {
        Authorization: `Token ${token}`
      },
      data: {
        title, content
      }
    })
      .then(() => {
        router.push({ name: 'articles' })
      })
      .catch(err => console.log(err))
  }

  // 게시글 수정
  const updateArticle = (articleId, title, content) => {
    axios({
      method: 'put',
      url: `${API_URL}/api/v1/articles/${articleId}/`,
      headers: {
        Authorization: `Token ${token}`
      },
      data: {
        title, content
      }
    })
      .then(() => {
        alert('게시글이 수정되었습니다.')
        router.push({ name: 'articleDetailView', params: { id: articleId } })
      })
      .catch(err => console.log(err))
  }

  // 게시글 삭제
  const deleteArticle = (articleId) => {
    axios({
      method: 'DELETE',
      url: `${API_URL}/api/v1/articles/${articleId}`,
      headers: {
        Authorization: `Token ${token}`
      }
    })
      .then(() => {
        alert('게시글이 삭제되었습니다.')
        router.push({ name: 'articles' })
      })
      .catch((err) => {
        alert('삭제 중 오류가 발생했습니다')
        console.log(err)
      })
  }


  return {
    articles,
    articleDetail,
    comments,
    API_URL,
    getArticles,
    getArticleDetail,
    getComments,
    createComment,
    updateComment,
    deleteComment,
    createArticle,
    updateArticle,
    deleteArticle
  }
}, { persist: true })
