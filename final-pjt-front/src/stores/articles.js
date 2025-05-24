import { useRouter } from "vue-router";
import { defineStore } from "pinia";
import { ref } from 'vue'
import axios from 'axios'

export const useArticleStore = defineStore('article', () => {
  const articles = ref([])
  const articleDetail = ref(null)
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
    API_URL,
    getArticles,
    getArticleDetail,
    createArticle,
    updateArticle,
    deleteArticle
  }
}, { persist: true })
