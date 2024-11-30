<template>
  <div class="exchange-container">
    <!-- 헤더 섹션 -->
    <div class="header-section">
      <h1 class="page-title">
        <i class="fas fa-exchange-alt me-3"></i>환율 조회
      </h1>
      <RouterLink :to="{name: 'HomeView'}" class="home-button">
        <i class="fas fa-home me-2"></i>홈으로
      </RouterLink>
    </div>
    
    <div class="content-divider"></div>

    <!-- 메인 콘텐츠 -->
    <div class="content-section">
      <!-- 히스토그램 섹션 -->
      <div class="histogram-section">
        <div v-if="isLoading" class="loading">
          <i class="fas fa-spinner fa-spin me-2"></i>로딩 중...
        </div>
        <img v-else-if="histogramData" :src="histogramData" alt="환율 히스토그램" class="histogram-image">
      </div>

      <!-- 환율 계산기 섹션 -->
      <div class="calculator-section">
        <!-- 통화 선택 -->
        <select 
          class="currency-select" 
          v-model="currency" 
          @change="get_Histogram"
        >
          <option value="" disabled selected>통화를 선택해주세요</option>
          <optgroup label="주요 통화">
            <option value="USD">미국 달러 (USD)</option>
            <option value="EUR">유로 (EUR)</option>
            <option value="JPY(100)">일본 엔 (JPY)</option>
            <option value="CNH">중국 위안화 (CNH)</option>
          </optgroup>
          <optgroup label="기타 통화">
            <option value="GBP">영국 파운드 (GBP)</option>
            <option value="AUD">호주 달러 (AUD)</option>
            <option value="AED">아랍에미리트 디르함</option>
            <option value="BHD">바레인 디나르</option>
            <option value="BND">브루나이 달러</option>
            <option value="CAD">캐나다 달러</option>
            <option value="CHF">스위스 프랑</option>
            <option value="CNH">중국 위안화</option>
            <option value="DKK">덴마아크 크로네</option>
            <option value="ESP(100)">스페인 페세타</option>
            <option value="HKD">홍콩 달러</option>
            <option value="IDR(100)">인도네시아 루피아</option>
            <option value="KRW">한국 원</option>
            <option value="KWD">쿠웨이트 디나르</option>
            <option value="MYR">말레이지아 링기트</option>
            <option value="NLG">네델란드 길더</option>
            <option value="NOK">노르웨이 크로네</option>
            <option value="NZD">뉴질랜드 달러</option>
            <option value="SAR">사우디 리얄</option>
            <option value="SEK">스웨덴 크로나</option>
            <option value="SGD">싱가포르 달러</option>
            <option value="THB">태국 바트</option>
          </optgroup>
        </select>

        <!-- 환율 계산기 -->
        <div class="calculator-input">
          <div class="input-group">
            <input 
              type="number" 
              class="amount-input" 
              v-model="double"
              min="0"
            >
            <span class="currency-label">{{ currency || '통화' }}</span>
            <span class="equals-sign">=</span>
            <input 
              type="text" 
              class="result-input" 
              :value="exchangeData && currency ? (parseFloat(exchangeData.replace(/,/g, '')) * Number(double)).toLocaleString() : '0'" 
              readonly
            >
            <span class="currency-label">KRW</span>
          </div>
        </div>

        <!-- 로딩 및 결과 표시 -->
        <div class="status-section">
          <div v-if="isLoading" class="loading">
            <i class="fas fa-spinner fa-spin me-2"></i>로딩 중...
          </div>
          <div v-else class="exchange-rate">
            <i class="fas fa-info-circle me-2"></i>
            현재 환율: 1 {{ currency }} = {{ exchangeData }} KRW
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.exchange-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.header-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.page-title {
  font-size: 2.5rem;
  font-weight: 700;
  color: #333;
}

.home-button {
  padding: 0.8rem 1.5rem;
  background: #196DDC;
  color: white;
  border-radius: 10px;
  text-decoration: none;
  transition: all 0.3s ease;
}

.home-button:hover {
  background: #1557B0;
  transform: translateY(-2px);
}

.content-divider {
  height: 3px;
  background: linear-gradient(to right, #196DDC, #FCC800);
  border-radius: 2px;
  margin-bottom: 2rem;
}

.content-section {
  display: flex;
  gap: 2rem;
  margin-top: 2rem;
}

.histogram-section {
  flex: 1;
  background: white;
  border-radius: 15px;
  padding: 1rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.histogram-image {
  width: 100%;
  height: auto;
  border-radius: 10px;
}

.calculator-section {
  width: 500px;
  background: white;
  border-radius: 15px;
  padding: 2rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.currency-select {
  width: 100%;
  padding: 1rem;
  border: 2px solid #e0e0e0;
  border-radius: 10px;
  font-size: 1rem;
  margin-bottom: 1.5rem;
  transition: all 0.3s ease;
}

.currency-select:focus {
  border-color: #196DDC;
  box-shadow: 0 0 0 3px rgba(25, 109, 220, 0.1);
}

.calculator-input {
  margin-bottom: 1.5rem;
}

.input-group {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.amount-input,
.result-input {
  flex: 1;
  padding: 1rem;
  border: 2px solid #e0e0e0;
  border-radius: 10px;
  font-size: 1rem;
  transition: all 0.3s ease;
}

.amount-input:focus {
  border-color: #196DDC;
  box-shadow: 0 0 0 3px rgba(25, 109, 220, 0.1);
}

.currency-label {
  padding: 0.5rem 1rem;
  background: #f8f9fa;
  border-radius: 8px;
  font-weight: 600;
}

.equals-sign {
  font-size: 1.5rem;
  font-weight: 600;
  color: #196DDC;
}

.status-section {
  text-align: center;
  color: #666;
}

.loading,
.exchange-rate {
  padding: 1rem;
  border-radius: 10px;
  background: #f8f9fa;
}

.loading {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 200px;
  background: #f8f9fa;
  border-radius: 10px;
  color: #196DDC;
  font-size: 1.2rem;
}

.fa-spin {
  margin-right: 8px;
}

/* 반응형 디자인 */
@media (max-width: 992px) {
  .content-section {
    flex-direction: column;
  }

  .calculator-section {
    width: 100%;
  }
}

@media (max-width: 768px) {
  .exchange-container {
    padding: 1rem;
  }

  .page-title {
    font-size: 2rem;
  }

  .calculator-section {
    padding: 1rem;
  }
}
</style>
    
    <script setup>
    import { useProductStore } from '@/stores/modules/product';
    import { computed, ref, watch } from 'vue';
    
    const isLoading = ref(false)
    const store = useProductStore()
    const currency = ref("")
    const double = ref(1)
    
  // 스토어 변수 매핑
    const exchangeData = computed(() => store.exchange_data);
    const histogramData = computed(() => store.histogramData);
    console.log('exchangeData:', exchangeData)
    
    // watch(currency, (newCurrency) => {
    //   if (newCurrency) {
    //     console.log('newCurrency:', newCurrency)
    //     store.exchange(newCurrency); // Trigger the store's exchange function
    //   }
    // });
    

    
    const get_Histogram = () => {
  isLoading.value = true
  Promise.all([
    store.exchange(currency.value),
    store.requestCurrency(currency.value)
  ])
    .catch(error => {
      console.error('Error:', error)
    })
    .finally(() => {
      setTimeout(() => {  // 로딩 상태를 조금 더 오래 유지
        isLoading.value = false
      }, 100)
    })
}
    
</script>