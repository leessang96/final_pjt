<template>
  <h1>은행 지도</h1>
  <div class="search-form">
    <select v-model="selectedSido">
      <option disabled value="">시/도 선택</option>
      <option v-for="sido in sidoList" :key="sido">{{ sido }}</option>
    </select>

    <select v-model="selectedSigungu" :disabled="!selectedSido">
      <option disabled value="">시/군/구 선택</option>
      <option v-for="sgg in sigunguList" :key="sgg">{{ sgg }}</option>
    </select>

    <select v-model="selectedBank">
      <option disabled value="">은행 선택</option>
      <option v-for="bank in bankList_json" :key="bank">{{ bank }}</option>
    </select>

    <button @click="searchByRegion">찾기</button>
  </div>

  <div>
    <h2>내 주변 은행 지도</h2>
    <div id="map" style="width: 100%; height: 400px"></div>
  </div>
  <!-- <div>
    <h2>내 주변 은행</h2>
    <ul>
      <li v-for="bank in bankList" :key="bank.id">
        {{ bank.place_name }} - {{ bank.road_address_name }}
      </li>
    </ul>
  </div> -->
</template>

<script setup>
import axios from 'axios'
import { ref, onMounted, nextTick, watch } from 'vue'
import json from '@/assets/data.json'

const bankList = ref([])
let map = null
const markers = []

function clearMarkers() {
  markers.forEach(marker => marker.setMap(null))
  markers.length = 0
}
function waitForKakaoMapsReady() {
  return new Promise((resolve) => {
    const check = setInterval(() => {
      if (window.kakao && window.kakao.maps && typeof window.kakao.maps.load === 'function') {
        clearInterval(check)
        resolve()
      }
    }, 100)
  })
}

async function initializeMap(lat, lng) {
  await nextTick()

  const container = document.getElementById('map')
  if (!container) {
    console.error('map 컨테이너가 없습니다')
    return
  }

  map = new window.kakao.maps.Map(container, {
    center: new window.kakao.maps.LatLng(lat, lng),
    level: 4
  })

  new window.kakao.maps.Marker({
    map,
    position: new window.kakao.maps.LatLng(lat, lng),
    title: '내 위치'
  })

  const res = await axios.get('http://localhost:8000/api/map-banks/nearby-banks/', {
    params: { lat, lng }
  })

  console.log('지도 API 응답', res.data)

  bankList.value = res.data.documents

  bankList.value.forEach(bank => {
    const marker = new window.kakao.maps.Marker({
      map,
      position: new window.kakao.maps.LatLng(bank.y, bank.x),
      title: bank.place_name
    })

    const info = new window.kakao.maps.InfoWindow({
      content: `<div style="padding:5px;font-size:14px;">${bank.place_name}</div>`
    })

    window.kakao.maps.event.addListener(marker, 'click', () => {
      info.open(map, marker)
    })
  })
}

onMounted(async () => {
  navigator.geolocation.getCurrentPosition(
    async (position) => {
      const lat = position.coords.latitude
      const lng = position.coords.longitude

      const script = document.createElement('script')
      script.src = 'https://dapi.kakao.com/v2/maps/sdk.js?appkey=01641d9abf813773e65378b3b3454bfb&autoload=false'
      script.onload = () => {
        window.kakao.maps.load(() => {
          initializeMap(lat, lng)
        })
      }
      document.head.appendChild(script)
    },
    (err) => {
      console.error('위치 정보 실패', err)
    }
  )
})

/// 검색 ///
const sidoList = json.mapInfo.map(region => region.name)
const sigunguList = ref([])
const bankList_json = json.bankInfo

const selectedSido = ref('')
const selectedSigungu = ref('')
const selectedBank = ref('')

// 시/도 선택 시, 시/군/구 자동 갱신
watch(selectedSido, (sido) => {
  const region = json.mapInfo.find(region => region.name === sido)
  sigunguList.value = region ? region.countries : []
})

// 검색 버튼 클릭 시 API 호출
const searchByRegion = async () => {
  const keyword = `${selectedSido.value} ${selectedSigungu.value} ${selectedBank.value}`
  const res = await axios.get('https://dapi.kakao.com/v2/local/search/keyword.json', {
    headers: {
      Authorization: `KakaoAK ${import.meta.env.VITE_KAKAO_REST_API_KEY}`
    },
    params: {
      query: keyword,
      category_group_code: 'BK9'
    }
  })

    const results = res.data.documents
  console.log('검색결과:', results)

  if (results.length === 0) {
    alert('검색 결과가 없습니다')
    return
  }

  const first = results[0]
  const newCenter = new window.kakao.maps.LatLng(first.y, first.x)
  map.setCenter(newCenter)

  clearMarkers()

  results.forEach(result => {
    const marker = new window.kakao.maps.Marker({
      map,
      position: new window.kakao.maps.LatLng(result.y, result.x),
      title: result.place_name
    })

    const info = new window.kakao.maps.InfoWindow({
      content: `<div style="padding:5px;font-size:14px;">${result.place_name}</div>`
    })

    window.kakao.maps.event.addListener(marker, 'click', () => {
      info.open(map, marker)
    })

    markers.push(marker)
  })
}


</script>

<style scoped>
#map {
  width: 100%;
  height: 400px;
  border: 1px solid #ddd;
}
</style>