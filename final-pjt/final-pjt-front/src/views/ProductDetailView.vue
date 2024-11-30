<template>
        <div class="product-detail-container">
      <!-- 헤더 섹션 -->
      <div class="header-section">
        <div class="d-flex align-items-center justify-content-between mb-4">
          <div>
            <h1 class="product-title fw-bold">{{ product.fin_prdt_nm }}</h1>
            <p class="product-description text-secondary mt-3">
              {{ product.description }}
            </p>
          </div>
          <RouterLink :to="{name: 'ProductView'}" class="btn btn-secondary btn-lg fw-bold back-button">
            <i class="fas fa-arrow-left me-2"></i>뒤로가기
          </RouterLink>
        </div>
      </div>
      <hr class="divider">
      <div class="circle-container mt-5">
    <div class="circle circle1 opacity-75" style="background-color:#FCC800;">
        <div class="circle-content">
            <h3 class="circle-value">{{ product?.rates?.intr_rate2 }}%</h3>
            <p class="circle-label">최고금리</p>
        </div>
    </div>
    <div class="circle circle2 opacity-75" style="background-color:#196DDC;">
        <div class="circle-content">
            <h3 class="circle-value">{{ product.join_member }}</h3>
            <p class="circle-label">대상</p>
        </div>
    </div>
    <div class="circle circle3 opacity-75" style="background-color:#FCC800; font-size: 16px; color:black;">
        <div class="circle-content">
          <h3 class="circle-value">{{ product.join_way }}</h3>
          <p class="circle-label">가입방법</p>
        </div>
    </div>
    <div class="circle circle4 opacity-75" style="background-color:#196DDC; font-size: 16px; color:black;">
    <div class="circle-content">
        <h3 v-if="product.period" class="circle-value">
            {{ isNaN(product.period.save_trm) ? 
                product.period.save_trm : 
                `${product.period.save_trm}개월` }}
        </h3>
        <p class="circle-label">기간</p>
    </div>
</div>
</div>

        <div class="d-flex justify-content-center mt-5">
            <button type="button" class="btn btn-outline-primary btn-lg fw-bold">부모님 조르기</button>
        </div>

        <div v-if="product" class="product-details-section">
    <!-- 상세 정보 카드 -->
    <div class="info-card">
        <h3 class="section-title">상품 상세 정보</h3>
        <div class="info-grid">
            <div class="info-item">
                <div class="info-label">
                    <i class="fas fa-info-circle"></i>
                    <span>상품 설명</span>
                </div>
                <p class="info-content">{{ product.description || '정보 없음' }}</p>
            </div>
            
            <div class="info-item">
                <div class="info-label">
                    <i class="fas fa-percentage"></i>
                    <span>만기 후 이자율</span>
                </div>
                <p class="info-content">{{ product.mtrt_int || '정보 없음' }}</p>
            </div>

            <div class="info-item">
                <div class="info-label">
                    <i class="fas fa-file-contract"></i>
                    <span>특별 우대 조건</span>
                </div>
                <p class="info-content">{{ product.cpcl_cnd || '정보 없음' }}</p>
            </div>

            <div class="info-item">
                <div class="info-label">
                    <i class="fas fa-users"></i>
                    <span>가입 대상</span>
                </div>
                <p class="info-content">{{ product.join_member || '정보 없음' }}</p>
            </div>

            <div class="info-item">
                <div class="info-label">
                    <i class="fas fa-clipboard-list"></i>
                    <span>상품 내용</span>
                </div>
                <p class="info-content">{{ product.etc_note || '정보 없음' }}</p>
            </div>
        </div>
    </div>

    <!-- 예금자 보호 정보 카드 -->
    <div class="protection-card">
        <div class="protection-header">
            <i class="fas fa-shield-alt"></i>
            <h4>예금자 보호</h4>
        </div>
        <div class="protection-content">
            <img src="../../public/images/kdic_logo_new.png" alt="kdic_logo" class="kdic-logo">
            <p class="protection-text">
                이 예금은 예금자보호법에 따라 원금과 소정의 이자를 합하여 1인당 "5천만원까지" (본 은행의 여타 보호상품과 합산) 보호됩니다.
            </p>
        </div>
    </div>
</div>
      </div>
</template>

<script setup>
import { useProductStore } from '@/stores/modules/product';
import { onMounted, ref } from 'vue';
import { useRoute } from 'vue-router';

const product = ref({})
const route = useRoute()
const store = useProductStore()
onMounted(async () => {
    const productId = Number(route.params.id);  // ID를 숫자로 변환
    console.log('요청한 Product ID:', productId);

    try {
        await store.productList();  // 데이터를 로드
        console.log('로딩된 상품 목록:', store.products);

        // 상품 찾기
        const foundProduct = store.products.find(item => item.id === productId);
        if (foundProduct) {
            product.value = foundProduct;
            console.log('찾은 상품:', product.value);
        } else {
            console.error('상품을 찾을 수 없습니다.');
        }
    } catch (error) {
        console.error('데이터 로드 중 오류:', error);
    }
});

</script>

<style scoped>
.product-detail-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
  background-color: #fff;
}

.header-section {
  margin-bottom: 2rem;
  padding: 1rem 0;
}

.product-title {
  font-size: 2.5rem;
  color: #333;
  margin: 0;
  line-height: 1.2;
}

.product-description {
  font-size: 1.1rem;
  max-width: 800px;
  margin-bottom: 0;
}

.back-button {
  transition: all 0.3s ease;
  background-color: #f8f9fa;
  color: #333;
  border: none;
  padding: 0.8rem 1.5rem;
}

.back-button:hover {
  background-color: #e9ecef;
  transform: translateX(-5px);
}

.divider {
  border: none;
  height: 2px;
  background: linear-gradient(to right, #196DDC, #FCC800);
  margin: 2rem 0;
  opacity: 0.2;
}

.circle-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: nowrap;
  margin: 3rem 0;
  padding: 0 2rem;
  gap: 1rem;
}

.circle {
  flex: 0 0 auto;
  width: 250px;
  height: 250px;
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
  color: #000;  /* 검정색으로 변경 */
  transition: transform 0.3s ease;
  box-shadow: 0 4px 15px rgba(0,0,0,0.1);
  margin: 0 10px;
  font-weight: 500;  /* 기본 폰트 두께 증가 */
}

.circle:hover {
  transform: translateY(-5px);
}

.circle-value {
  font-size: 2rem;  /* 크기 증가 */
  font-weight: 700;  /* 더 진하게 */
  margin: 0.5rem 0;
  color: #000;  /* 확실한 검정색 */
  text-shadow: 1px 1px 1px rgba(255,255,255,0.5);  /* 가독성을 위한 텍스트 그림자 */
}

.circle-label {
  font-size: 1.2rem;  /* 크기 증가 */
  font-weight: 600;  /* 진하게 */
  margin: 0.5rem 0;
  color: #000;  /* 확실한 검정색 */
}

.circle-content {
  text-align: center;
  padding: 1rem;
}

.circle-content i {
  font-size: 2rem;
  margin-bottom: 0.5rem;
}

.circle-content h3 {
  font-size: 1.5rem;
  margin: 0.5rem 0;
}

.info-card {
  background: white;
  border-radius: 15px;
  padding: 2rem;
  box-shadow: 0 4px 15px rgba(0,0,0,0.05);
  margin-bottom: 2rem;
}

.section-title {
  color: #333;
  border-bottom: 2px solid #196DDC;
  padding-bottom: 0.5rem;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  margin-top: 1.5rem;
}

.info-item {
  background: #f8f9fa;
  padding: 1.5rem;
  border-radius: 10px;
  transition: transform 0.2s ease;
}

.info-item:hover {
  transform: translateY(-3px);
  box-shadow: 0 4px 10px rgba(0,0,0,0.1);
}

.info-label {
  display: flex;
  align-items: center;
  margin-bottom: 0.8rem;
  color: #196DDC;
  font-weight: bold;
}

.info-label i {
  margin-right: 0.5rem;
  font-size: 1.2rem;
}

.info-content {
  color: #666;
  line-height: 1.6;
  margin: 0;
}

.protection-card {
  background: white;
  border-radius: 15px;
  padding: 2rem;
  box-shadow: 0 4px 15px rgba(0,0,0,0.05);
}

.protection-header {
  display: flex;
  align-items: center;
  margin-bottom: 1.5rem;
  color: #196DDC;
}

.protection-header i {
  font-size: 1.5rem;
  margin-right: 1rem;
}

.protection-content {
  display: flex;
  align-items: center;
  background: #f8f9fa;
  padding: 1.5rem;
  border-radius: 10px;
}

.kdic-logo {
  height: 50px;
  margin-right: 1.5rem;
}

.protection-text {
  margin: 0;
  color: #666;
  line-height: 1.6;
  flex: 1;
}

@media (max-width: 1200px) {
  .circle-container {
    overflow-x: auto;
    padding-bottom: 1rem;
  }
  
  .circle {
    width: 220px;
    height: 220px;
  }
}

@media (max-width: 768px) {
  .header-section > div {
    flex-direction: column;
    gap: 1rem;
  }

  .product-title {
    font-size: 2rem;
  }

  .back-button {
    align-self: flex-start;
  }

  .circle {
    width: 200px;
    height: 200px;
  }

  .product-details-section {
    padding: 0 1rem;
  }

  .info-grid {
    grid-template-columns: 1fr;
  }

  .protection-content {
    flex-direction: column;
    text-align: center;
  }

  .kdic-logo {
    margin: 0 0 1rem 0;
  }
}
</style>