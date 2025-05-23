import { useRouter } from "vue-router";
import { defineStore } from "pinia";
import { ref } from 'vue'
import axios from 'axios'

export const useArticleStore = defineStore('article', () => {
  const articles = ref([])
  const token = localStorage.getItem('token')
  const API_URL = 'http://127.0.0.1:8000'
  const router = useRouter()

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
        router.push({name: 'articles'})
      }) 
      .catch(err => console.log(err))
  }
  

  return{
    articles, API_URL, getArticles, createArticle
  }
}, { persist: true })
