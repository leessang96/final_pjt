<template>
  <h1>은행 지도</h1>
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
import { ref, onMounted, nextTick } from 'vue'

const bankList = ref([])

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

  const map = new window.kakao.maps.Map(container, {
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
</script>

<style scoped>
#map {
  width: 100%;
  height: 400px;
  border: 1px solid #ddd;
}
</style>