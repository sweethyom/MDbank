<template>
  <div class="search-container">
    <form @submit.prevent="search">
      <h2 class="search-title">
        <i class="fas fa-search me-2"></i>주변은행 검색
      </h2>
      
      <!-- 지역 선택 -->
      <div class="form-group">
        <select 
          id="city" 
          class="search-select" 
          v-model="keyword1"
        >
          <option value="" disabled selected>지역을 선택해주세요</option>
          <optgroup label="특별시/광역시">
            <option value="서울">서울특별시</option>
            <option value="부산">부산광역시</option>
            <option value="대구">대구광역시</option>
            <option value="인천">인천광역시</option>
            <option value="광주">광주광역시</option>
            <option value="대전">대전광역시</option>
            <option value="울산">울산광역시</option>
          </optgroup>
          <optgroup label="도">
            <option value="경기도">경기도</option>
            <option value="강원도">강원도</option>
            <option value="충청북도">충청북도</option>
            <option value="충청남도">충청남도</option>
            <option value="경상북도">경상북도</option>
            <option value="경상남도">경상남도</option>
            <option value="전라북도">전라북도</option>
            <option value="전라남도">전라남도</option>
          </optgroup>
        </select>
      </div>

      <!-- 상세 주소 입력 -->
      <div class="form-group">
        <input
          type="text"
          id="keyword2" 
          class="search-input"
          v-model="keyword2"
          placeholder="시/군/구 또는 은행명을 입력하세요"
        />
      </div>

      <!-- 검색 버튼 -->
      <button type="submit" class="search-button">
        <i class="fas fa-search me-2"></i>검색하기
      </button>
    </form>

    <div class="search-divider"></div>
    
    <!-- 검색 결과 목록 -->
    <KakaoMapSearchPlacesList />
  </div>
</template>

<style scoped>
.search-container {
  background: white;
  border-radius: 15px;
  padding: 1.5rem;
}

.search-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: #333;
  margin-bottom: 1.5rem;
}

.search-title i {
  color: #196DDC;
}

.form-group {
  margin-bottom: 1rem;
}

.search-select {
  width: 100%;
  padding: 0.8rem;
  border: 2px solid #e0e0e0;
  border-radius: 10px;
  font-size: 1rem;
  color: #333;
  background-color: #fff;
  transition: all 0.3s ease;
  cursor: pointer;
}

.search-select:focus {
  border-color: #196DDC;
  box-shadow: 0 0 0 3px rgba(25, 109, 220, 0.1);
  outline: none;
}

.search-input {
  width: 100%;
  padding: 0.8rem;
  border: 2px solid #e0e0e0;
  border-radius: 10px;
  font-size: 1rem;
  transition: all 0.3s ease;
}

.search-input:focus {
  border-color: #196DDC;
  box-shadow: 0 0 0 3px rgba(25, 109, 220, 0.1);
  outline: none;
}

.search-button {
  width: 100%;
  padding: 0.8rem;
  background: #196DDC;
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.search-button:hover {
  background: #1557B0;
  transform: translateY(-2px);
}

.search-button:active {
  transform: translateY(0);
}

.search-divider {
  height: 1px;
  background: #e0e0e0;
  margin: 1.5rem 0;
}

/* 옵션 그룹 스타일링 */
optgroup {
  font-weight: 600;
  color: #196DDC;
}

option {
  color: #333;
  padding: 0.5rem;
}

/* 반응형 디자인 */
@media (max-width: 768px) {
  .search-container {
    padding: 1rem;
  }

  .search-title {
    font-size: 1.2rem;
  }

  .search-select,
  .search-input,
  .search-button {
    padding: 0.6rem;
    font-size: 0.9rem;
  }
}
</style>
  
  <script setup>
  import { ref } from 'vue';
  import { useMapStore } from '@/stores/modules/kakaomap';
  import KakaoMapSearchPlacesList from './KakaoMapSearchPlacesList.vue';
  
  const store = useMapStore();
  const keyword1 = ref('');
  const keyword2 = ref('');
  
  // 검색어를 조합해서 searchPlaces 호출
  const search = () => {
    // 검색어 조합 (빈 문자열 처리)
    const searchQuery = `${keyword1.value} ${keyword2.value}`.trim();
    if (!searchQuery) {
      alert('검색어를 입력해주세요.');
      return;
    }
    store.searchPlaces(searchQuery); // 장소 검색
  };
  </script>

  