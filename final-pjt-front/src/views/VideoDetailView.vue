<template>
    <div class="container mt-4">
        <h3>{{ video?.snippet.title }}</h3>
        <p class="text-muted">업로드 날짜: {{ formattedDate }}</p>

        <iframe width="100%" height="400" :src="'https://www.youtube.com/embed/' + id" frameborder="0"
            allowfullscreen></iframe>

        <p class="mt-3" v-html="video?.snippet.description?.replace(/\n/g, '<br>')"></p>

        <!-- <RouterLink to="/" class="btn btn-secondary mt-3">돌아가기</RouterLink> -->
        <div class="d-flex">
            <button @click="saveVideo" class="btn btn-primary"> 동영상 저장 </button>
            <button @click="saveChannel" class="btn btn-warning">채널 저장</button>
        </div>
    </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'

const route = useRoute()
const id = route.params.id
const video = ref(null)

const formattedDate = ref('')

onMounted(async () => {
    const apiKey = import.meta.env.VITE_YT_API_KEY
    const url = 'https://www.googleapis.com/youtube/v3/videos'

    const params = {
        key: apiKey,
        part: 'snippet',
        id: id
    }

    try {
        const res = await axios.get(url, { params })
        video.value = res.data.items[0]
        const date = new Date(video.value.snippet.publishedAt)
        formattedDate.value = date.toISOString().split('T')[0]
    } catch (error) {
        console.error('상세정보 요청 실패:', error)
    }
})

const saveVideo = () => {
    const stored = JSON.parse(localStorage.getItem('savedVideos')) || []

    // 중복 방지
    const exists = stored.some(v => v.id === video.value.id)
    if (exists) {
        alert('이미 저장된 영상입니다.')
        return
    }
    const newVideo = {
        id: video.value.id,
        title: video.value.snippet.title,
        description: video.value.snippet.description,
        thumbnail: video.value.snippet.thumbnails.medium.url,
        publishedAt: video.value.snippet.publishedAt,
    }

    stored.push(newVideo)
    localStorage.setItem('savedVideos', JSON.stringify(stored))
    alert('영상이 저장되었습니다.')
}

const saveChannel = () => {
    const stored = JSON.parse(localStorage.getItem('savedChannels')) || []

    // 중복 방지
    const exists = stored.some(v => v === video.value.snippet.channelTitle)
    if (exists) {
        alert('이미 저장된 채널입니다.')
        return
    }

    const newChannel = video.value.snippet.channelTitle

    stored.push(newChannel)
    localStorage.setItem('savedChannels', JSON.stringify(stored))
    alert('채널이 저장되었습니다.')
}
// 저장할 영상 객체 구성

</script>
