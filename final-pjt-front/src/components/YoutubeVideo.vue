<template>
    <div class="card h-100">
        <RouterLink :to="{ name: 'videoDetail', params: { 'id': video.id.videoId } }">
            <img :src="video.snippet.thumbnails.medium.url" class="card-img-top" :alt="video.snippet.title">
        </RouterLink>
        <div class="card-body">
            <p class="card-text">{{ video.snippet.title }}</p>
        </div>
    </div>
</template>

<script setup>
import { RouterLink, RouterView } from 'vue-router';
const props = defineProps({
    video: Object
})


</script>

<style scoped>
.card-text {
    font-size: 0.95rem;
    font-weight: 500;
}
</style>
