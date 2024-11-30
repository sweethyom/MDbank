<template>
    <div class="container">
      <!-- 첫번째 row -->
      <div class="row row-cols-1 row-cols-lg-2 g-4 mb-4">
        <!-- 광고 배너 캐러셀 -->
        <div class="col col-lg-8">
          <div class="card h-100">
            <div id="mainCarousel" class="carousel slide" data-bs-ride="carousel" data-bs-interval="3000">
              <div class="carousel-inner">
                <div class="carousel-item active">
                  <RouterLink :to="{ name: 'ProductDetailView', params: { id: 26 }}">
                    <img src="/images/banner1.png" class="d-block w-100" alt="banner1">
                  </RouterLink>
                </div>
                <div class="carousel-item">
                  <RouterLink :to="{ name: 'ProductDetailView', params: { id: 27 }}">
                    <img src="/images/banner2.png" class="d-block w-100" alt="banner2">
                  </RouterLink>
                </div>
                <div class="carousel-item">
                    <img src="/images/banner3.png" class="d-block w-100" alt="banner3">
                </div>
              </div>
              <button class="carousel-control-prev" type="button" data-bs-target="#mainCarousel" data-bs-slide="prev">
                <span class="carousel-control-prev-icon" aria-hidden="true"></span>
                <span class="visually-hidden">Previous</span>
              </button>
              <button class="carousel-control-next" type="button" data-bs-target="#mainCarousel" data-bs-slide="next">
                <span class="carousel-control-next-icon" aria-hidden="true"></span>
                <span class="visually-hidden">Next</span>
              </button>
            </div>
          </div>
        </div>
  
        <!-- 잔액 정보 -->
        <div class="col col-lg-4">
          <div class="card h-100">
            <div class="card-body text-center">
              <div v-if="memberStore.profileData">
                <h5 class="card-title mb-4">{{ memberStore.memberName }}님 안녕하세요!</h5>
                <h6 class="card-subtitle mb-3">잔액정보</h6>
                <p v-if="showBalance" class="balance-text mb-4">
                  {{ transferStore.balance ? Number(transferStore.balance?.Ldbl)?.toLocaleString() : '잔액 조회중' }} 원
                </p>
                <div class="button-group">
                  <button class="btn btn-primary me-2" @click="balanceStatus">
                    {{ showBalance ? '잔액 가리기' : '잔액 보기' }}
                  </button>
                  <button class="btn btn-outline-primary" @click="goToTransfer">이체하기</button>
                </div>
              </div>
              <div v-else class="login-prompt">
                <h6 class="mb-3">서비스 이용을 위해 로그인이 필요합니다</h6>
                <RouterLink :to="{name:'LoginView'}" class="btn btn-primary">로그인하기</RouterLink>
              </div>
            </div>
          </div>
        </div>
      </div>
  
<div class="row g-4">
  <div class="col-12 col-lg-6">
    <!-- 자산유형 확인 -->
    <div class="card h-100 asset-type-card">
      <div class="card-body d-flex flex-column">
        <!-- 로그인되지 않은 경우 -->
        <div v-if="!memberStore.profileData" class="login-prompt text-center">
          <h6 class="mb-3">서비스 이용을 위해 로그인이 필요합니다</h6>
          <RouterLink :to="{name:'LoginView'}" class="btn btn-primary">로그인하기</RouterLink>
        </div>

        <!-- 로그인된 경우 -->
        <template v-else>
           <!-- 자산유형이 있는 경우 -->
           <div v-if="memberStore.profileData?.asset_type" class="asset-info">
            <div class="text-center">
              <div class="asset-icon mb-4"> 
                <div class="green-box mx-auto">
                  <img :src="getAssetTypeImage" alt="자산 유형 이미지" class="asset-type-img">
                </div>
              </div>
              <p class="mb-2">{{ memberStore.memberName }}님의 자산관리 유형은</p>
              <h5 class="asset-type mb-3">{{ memberStore.profileData.asset_type.title }}</h5>
              <p>입니다!</p>
            </div>
          </div>

          <!-- 자산유형이 없는 경우 -->
          <div v-else class="asset-info" style="display: flex; flex-direction: column; align-items: center; justify-content: center;">
            <div class="text-center" style="font-size: 25px; font-weight: bold;">
              <p class="mb-3">{{ memberStore.memberName }}님</p>
              <p>자산관리 유형을 분석해보시고, <br>추천 금융 상품을 확인해보세요!</p>
            </div>
          </div>
    

          <button @click="goToRecommend" class="recommend-button mt-auto">
            추천 금융 상품 보러가기
          </button>
        </template>
      </div>
    </div>
  </div>

  <div class="col-12 col-lg-6">
    <!-- 환율 정보 -->
    <div class="card h-100">
      <div class="card-body">
        <div class="d-flex justify-content-between align-items-center mb-3">
          <h5 class="card-title mb-0">환율 정보</h5>
          <RouterLink :to="{name: 'ExchangeView'}" class="btn btn-outline-primary btn-sm">
            더보기
          </RouterLink>
        </div>
        
        <div class="exchange-content d-flex flex-column justify-content-center">
          <!-- 현재 환율 표시 -->
          <div class="exchange-rate mb-4">
            <i class="fas fa-dollar-sign me-2"></i>
            <span class="rate-text">1 USD = {{ exchangeData }} KRW</span>
          </div>

          <!-- 히스토그램 -->
          <div class="histogram-container">
            <div v-if="isLoading" class="loading">
              <i class="fas fa-spinner fa-spin"></i>
            </div>
            <img v-else-if="histogramData" :src="histogramData" alt="USD 환율 히스토그램" class="histogram-image">
          </div>
        </div>
      </div>
    </div>
  </div>
</div>
</div>
</template>
<script setup>
import { onMounted, ref, computed } from 'vue'
import { useTransferStore } from '@/stores/modules/transfer'
import { useRouter } from 'vue-router'
import { useMemberStore } from '@/stores/modules/member';
import { useProductStore } from '@/stores/modules/product';

const memberStore=useMemberStore()
const transferStore = useTransferStore()
const router = useRouter()
const showBalance = ref(false)
const productStore = useProductStore()
const isLoading = ref(false)



// 자산 유형에 따른 이미지 경로 계산
const getAssetTypeImage = computed(() => {
  const assetType = memberStore.profileData?.asset_type?.title
  if (assetType === '느릿느릿 거북이 타입') {
    return '/images/turtle.jpeg'
  } else if (assetType === '플렉스 호랑이 타입') {
    return '/images/tiger.jpeg'
  }
  return '' // 기본 이미지 또는 빈 문자열
})

const goToTransfer = function(){
    router.push({name:'TransferView'})
}

// 추천 상품 페이지로 이동하는 함수 추가
const goToRecommend = function() {
    router.push({ name: 'AssetTypeView' })
}

// 잔액 보기 버튼 클릭시 잔액을 보여주는 함수
const balanceStatus = async () => {
    showBalance.value=!showBalance.value
    if (showBalance. value){
        await fetchBalance ()

    }
}

// 잔액을 서버에서 가져오는 함수
const fetchBalance = async() => {
    await transferStore.balanceSearch()
    
}



onMounted(() => {
    memberStore.getUserInfo()
    // transferStore.balanceSearch()
})

// 환율 데이터와 히스토그램 데이터
const exchangeData = computed(() => productStore.exchange_data)
const histogramData = computed(() => productStore.histogramData)

// 컴포넌트 마운트 시 USD 데이터 로드
onMounted(async () => {
  isLoading.value = true
  try {
    await productStore.exchange('USD')
    await productStore.requestCurrency('USD')
  } finally {
    isLoading.value = false
  }
})
</script>

<style scoped>
.container {
  padding: 20px;
}


.card {
  border: none; /* 테두리 제거 */
  border-radius: 10px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15); /* 그림자 더 진하게 수정 */
  transition: transform 0.2s, box-shadow 0.2s;
  height: 100%;
}

.card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2); /* hover 시 그림자 더 진하게 */
}

/* 캐러셀 높이 고정 */
.carousel {
  border-radius: 10px;
  overflow: hidden;
  height: 400px; /* 고정 높이 설정 */
}

.carousel-item {
  height: 400px;
}

.carousel-item img {
  object-fit: cover;
  height: 100%;
  width: 100%;
}

/* row 높이 고정 */
.row {
  min-height: 400px; /* row의 최소 높이 설정 */
}

/* col 높이 고정 */
.col {
  height: 400px; /* col의 높이 설정 */
}

/* 자산유형 카드 스타일 */
.asset-type-card {
  background: linear-gradient(180deg, #9bc6ff 0%, #ffffff 100%);
  border: none;
  padding: 20px;
  height: 100%;
  display: flex;
  flex-direction: column;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15); /* 그림자 추가 */
}

.recommend-button {
  background-color: #196DDC;
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  width: 100%;
  margin-top: 20px;
  box-shadow: 0 4px 8px rgba(25, 109, 220, 0.2);
}

.recommend-button:hover {
  background-color: #1557b0;
  transform: translateY(-2px);
  box-shadow: 0 6px 12px rgba(25, 109, 220, 0.3);
}

.recommend-button:active {
  transform: translateY(0);
  box-shadow: 0 2px 4px rgba(25, 109, 220, 0.2);
}

.balance-text {
  font-size: 1.5rem;
  font-weight: bold;
  color: #196DDC;
}

.button-group {
  display: flex;
  justify-content: center;
  gap: 10px;
}

.btn {
  padding: 8px 20px;
  border-radius: 5px;
  font-weight: 500;
}

.btn-primary {
  background-color: #196DDC;
  border-color: #196DDC;
}

.btn-primary:hover {
  background-color: #1557b0;
  border-color: #1557b0;
}

.btn-outline-primary {
  color: #196DDC;
  border-color: #196DDC;
}

.btn-outline-primary:hover {
  background-color: #196DDC;
  color: white;
}

.login-prompt {
  padding: 20px;
}

.card-title {
  color: #333;
  font-weight: 600;
}

.card-text {
  color: #666;
}

@media (max-width: 992px) {
  .carousel-item {
    height: 300px;
  }
}


/* 자산유형 카드 스타일 */
.asset-type-card {
  background: linear-gradient(180deg, #9bc6ff 0%, #ffffff 100%);
  border: none;
  padding: 20px;
  height: 100%;
  display: flex;
  flex-direction: column;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15); /* 그림자 추가 */
}


.asset-info {
  display: flex;
  align-items: center;
  gap: 20px;
  flex: 1;
}

.green-box {
  width: 120px;
  height: 160px;
  background-color: #ffffff;
  border-radius: 10px;
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15),
              0 12px 24px rgba(0, 0, 0, 0.15); /* 그림자 더 진하게 */
  transition: box-shadow 0.3s ease;
  overflow: hidden;
}

.green-box:hover {
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2),
              0 16px 32px rgba(0, 0, 0, 0.2); /* hover 시 그림자 더 진하게 */
}


.asset-type-img {
  width: 100%;
  height: 100%;
  object-fit: cover; /* 이미지 비율 유지하면서 박스에 맞춤 */
}

.green-box {
  width: 120px;
  height: 160px;
  background-color: #ffffff;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1),
              0 8px 16px rgba(0, 0, 0, 0.1);
  transition: box-shadow 0.3s ease;
  overflow: hidden; /* 이미지가 박스를 벗어나지 않도록 */
}


.green-box:hover {
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15), /* 호버 시 더 강한 그림자 */
              0 12px 24px rgba(0, 0, 0, 0.15);
}

/* 환율 카드 스타일 */
.card-body {
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.exchange-content {
  height: calc(100% - 50px);
}

.histogram-container {
  flex-grow: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  background: #f8f9fa;
  border-radius: 10px;
  overflow: hidden;
  min-height: 200px;
}

.histogram-image {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.loading {
  color: #196DDC;
  font-size: 1.5rem;
}

.exchange-rate {
  background: #f8f9fa;
  padding: 1rem;
  border-radius: 10px;
  text-align: center;
}

.rate-text {
  font-size: 1.2rem;
  font-weight: 600;
  color: #196DDC;
}

</style>

