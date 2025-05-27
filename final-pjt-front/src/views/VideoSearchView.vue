<template>
    <!-- input -->
    <div class="container mt-2">
        <h1>비디오 검색</h1>
    </div>
    <div class="container mt-2 d-flex">
        <input class="form-control me-2" v-model="query" @keyup.enter="search" placeholder="검색어 입력 후 Enter">
        <button class="btn btn-success" type="submit" @click="search">Search</button>
    </div>

    <div class="container video-list mt-4">
        <div class="row g-3"> <!-- g-3: 카드 간 간격 -->
            <div class="col-md-4" v-for="video in videos" :key="video.id.videoId">
                <YoutubeVideo :video="video" />
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import YoutubeVideo from '@/components/YoutubeVideo.vue'

const query = ref('')
const videos = ref([])

const search = async () => {
    const apiKey = import.meta.env.VITE_YT_API_KEY
    const url = 'https://www.googleapis.com/youtube/v3/search'

    const params = {
        key: apiKey,
        part: 'snippet',
        q: query.value,
        type: 'video',
        maxResults: 10,
        regeionCode: 'kr'
    }

    try {
        const res = await axios.get(url, { params })
        videos.value = res.data.items
    } catch (err) {
        console.error('YouTube API 오류:', err)
    }
}
</script>

<style scoped>
.video-list {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
}
</style>
