<template>
  <div class="map-container">
    <!-- 헤더 섹션 -->
    <div class="section-header">
      <h2 class="section-title">
        <i class="fas fa-map-marker-alt me-2"></i>주변지점찾기
      </h2>
      <div class="divider"></div>
    </div>

    <!-- 맵 콘텐츠 -->
    <div class="map-content">
      <!-- 지도 영역 -->
      <div class="map-wrapper">
        <div 
          ref="mapContainer" 
          :key="route.fullPath" 
          id="mapContainer" 
          class="map-area">
        </div>
      </div>
      
      <!-- 검색 영역 -->
      <div class="search-wrapper">
        <KakaoMapSearch />
      </div>
    </div>
  </div>
</template>

<style scoped>
.map-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.section-header {
  margin-bottom: 2rem;
}

.section-title {
  font-size: 2rem;
  font-weight: 700;
  color: #333;
  margin-bottom: 1rem;
}

.section-title i {
  color: #196DDC;
}

.divider {
  height: 3px;
  background: linear-gradient(to right, #196DDC, #FCC800);
  border-radius: 2px;
  margin: 1rem 0;
}

.map-content {
  display: flex;
  gap: 2rem;
  margin-top: 2rem;
}

.map-wrapper {
  flex: 1;
  position: relative;
}

.map-area {
  height: 70vh;
  border-radius: 15px;
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  border: 1px solid #e0e0e0;
  transition: all 0.3s ease;
}

.map-area:hover {
  box-shadow: 0 6px 25px rgba(0, 0, 0, 0.15);
  transform: translateY(-5px);
}

.search-wrapper {
  width: 450px;
  background: white;
  padding: 1.5rem;
  border-radius: 15px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  border: 1px solid #e0e0e0;
}

/* 반응형 디자인 */
@media (max-width: 992px) {
  .map-content {
    flex-direction: column;
  }

  .search-wrapper {
    width: 100%;
    margin-top: 1rem;
  }

  .map-area {
    height: 50vh;
  }
}

@media (max-width: 768px) {
  .map-container {
    padding: 1rem;
  }

  .section-title {
    font-size: 1.5rem;
  }

  .map-area {
    height: 40vh;
  }
}
</style>
<script setup>
import { useMapStore } from '@/stores/modules/kakaomap';
import { ref, onMounted, nextTick, watch, onBeforeMount, onActivated } from 'vue';
import { useRoute } from 'vue-router';  // vue-router에서 useRoute 가져오기
import KakaoMapSearch from '@/components/maps/KakaoMapSearch.vue';

const store = useMapStore();
const mapContainer = ref(null);
const route = useRoute();  // 라우트 객체 사용

// 지도 로드 전 mapContainer가 null이 아닌지 체크
onMounted(() => {
  nextTick(() => {
    if (mapContainer.value) {
      store.loadKakaoMap(mapContainer.value);
    } else {
      console.error('mapContainer가 존재하지 않습니다.');
    }
  });
});


// 라우트가 변경될 때마다 지도를 새로 로드
// watch(route, () => {
//   nextTick(() => {
//     if (mapContainer.value) {
//       store.loadKakaoMap(mapContainer.value);
//       console.log('지도 리로드');
//     }
//   });
// });

onActivated(() => {
  nextTick(() => {
    if (mapContainer.value) {
      store.loadKakaoMap(mapContainer.value);
    }
  });
});
</script>
