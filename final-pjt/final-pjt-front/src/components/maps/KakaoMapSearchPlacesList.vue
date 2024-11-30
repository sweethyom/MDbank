<template>
  <div class="places-container">
    <!-- 검색 결과 목록 -->
    <div v-if="isSearched" class="places-list">
      <!-- 검색 결과가 없을 때 -->
      <div v-if="places.length === 0" class="no-results">
        <i class="fas fa-search me-2"></i>
        <p>검색 결과가 없습니다.</p>
      </div>
      
      <!-- 검색 결과가 있을 때 -->
      <div v-else class="results-list">
        <div 
          v-for="(place, index) in places" 
          :key="place.id || index" 
          @click="setCenter(place)" 
          class="place-item"
        >
          <div class="place-content">
            <h4 class="place-name">
              <i class="fas fa-building me-2"></i>
              {{ place.place_name }}
            </h4>
            <div class="place-info">
              <p class="info-row">
                <i class="fas fa-map-marker-alt me-2"></i>
                {{ place.address_name }}
              </p>
              <p class="info-row">
                <i class="fas fa-phone me-2"></i>
                {{ place.phone || '연락처 없음' }}
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 초기 상태 -->
    <div v-else class="initial-state">
      <i class="fas fa-map-marked-alt mb-3"></i>
      <p>지역과 은행을 선택하고 검색해 주세요.</p>
    </div>
  </div>
</template>

<style scoped>
.places-container {
  max-height: 400px;
  overflow-y: auto;
  scrollbar-width: thin;
  scrollbar-color: #196DDC #f0f0f0;
}

/* 스크롤바 스타일링 */
.places-container::-webkit-scrollbar {
  width: 6px;
}

.places-container::-webkit-scrollbar-track {
  background: #f0f0f0;
  border-radius: 3px;
}

.places-container::-webkit-scrollbar-thumb {
  background: #196DDC;
  border-radius: 3px;
}

.places-list {
  margin-top: 1rem;
}

.no-results {
  text-align: center;
  padding: 2rem;
  color: #666;
}

.no-results i {
  font-size: 2rem;
  color: #196DDC;
  margin-bottom: 1rem;
}

.place-item {
  padding: 1rem;
  border-radius: 10px;
  background: #f8f9fa;
  margin-bottom: 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.place-item:hover {
  background: #fff;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  transform: translateY(-2px);
}

.place-content {
  padding: 0.5rem;
}

.place-name {
  font-size: 1.1rem;
  font-weight: 600;
  color: #196DDC;
  margin-bottom: 0.5rem;
}

.place-info {
  color: #666;
}

.info-row {
  display: flex;
  align-items: center;
  margin: 0.3rem 0;
  font-size: 0.9rem;
}

.info-row i {
  color: #196DDC;
  width: 20px;
}

.initial-state {
  text-align: center;
  padding: 3rem 1rem;
  color: #666;
}

.initial-state i {
  font-size: 3rem;
  color: #196DDC;
  margin-bottom: 1rem;
}

/* 반응형 디자인 */
@media (max-width: 768px) {
  .places-container {
    max-height: 300px;
  }

  .place-item {
    padding: 0.8rem;
  }

  .place-name {
    font-size: 1rem;
  }

  .info-row {
    font-size: 0.8rem;
  }
}
</style>

<script setup>
import { useMapStore } from '@/stores/modules/kakaomap';
import { computed, watch } from 'vue';

const store = useMapStore();

// 상태를 computed로 래핑하여 템플릿에 반응형으로 연결
const places = computed(() => store.places);
const isSearched = computed(() => store.isSearched);

const setCenter = (place) => {
  console.log("선택된 장소:", place);
  store.setCenter(place);
};

// 디버깅용: 상태 변화를 관찰
watch(() => places.value, (newPlaces) => {
  console.log("places.value 변경됨:", newPlaces);
});
watch(() => isSearched.value, (newStatus) => {
  console.log("isSearched 변경됨:", newStatus);
});
</script>