<template>
  <div class="m-5">
    <div class="d-flex align-items-center mb-5 justify-content-start">
        <h1 class="me-3 mt-3 mb-3 fw-bold">환율 조회</h1>
    </div>
    <hr>
    <div class="mt-5" style="width: 500px;">
      <select class="form-control mb-2" name="currency" id="currency" v-model="currency" @change="getHistogram">
        <option value="" disabled selected hidden>통화를 선택해주세요</option>
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

      </select>
    </div>

    <!-- 환율 계산기 -->
    <div class="input-group mt-4" v-if="currency && exchangeData">
      <input 
        type="text" 
        class="form-control" 
        v-model="double" 
        placeholder="환산할 금액" 
      />
      <span v-if="currency" class="input-group-text" width="100px">{{ currency }}</span>
      <span class="input-group-text">=</span>
      <input 
        type="text" 
        class="form-control" 
        :value="calculateExchange" 
        readonly
      />
      <span class="input-group-text" width="100px">원</span>
    </div>

    <!-- 히스토그램이 표시될 div -->
    <div v-if="histogramData" class="histogram-container mt-4">
      <img :src="histogramData" alt="환율 히스토그램">
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue';
import { useProductStore } from '@/stores/modules/product';

const store = useProductStore();
const currency = ref('');
const double = ref(1);

// 환율 데이터 가져오기
const exchangeData = computed(() => store.exchange_data);

// 히스토그램 데이터
const histogramData = computed(() => store.histogramData);

// 환율 계산 함수
const calculateExchange = computed(() => {
  if (exchangeData && currency.value) {
    // exchangeData는 문자열로 숫자 형식이므로, 변환 후 계산
    const exchangeRate = parseFloat(exchangeData.replace(/,/g, ''));
    return (exchangeRate * Number(double.value)).toFixed(2);  // 소수점 2자리로 반환
  }
  return 0;
});

// 선택된 통화에 따라 데이터 요청
const getHistogram = () => {
  if (currency.value) {
    store.requestCurrency(currency.value);  // store에서 함수 호출
  }
};

// watch currency 변경 시, 환율 데이터 요청
watch(currency, (newCurrency) => {
  if (newCurrency) {
    store.exchange(newCurrency);  // 환율 데이터 요청
  }
});
</script>

<style scoped>
.histogram-container {
  width: 100%;
  height: auto;
  margin-top: 20px;
  text-align: center;
}
</style>
