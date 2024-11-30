<template>
    <div class="container">
      <div class="carousel-wrapper">
      <ProductCarousel />
      </div>
    <div class="content-section">
      <!-- 네비게이션 탭 -->
      <div class="tab-container">
        <ul class="custom-tabs">
          <li class="tab-item">
            <a class="tab-link" 
               :class="{ active: selectedType === 4 }"
               @click="selectTab(4)">
               <i class="fas fa-list-ul me-2"></i>전체
            </a>
          </li>
          <li class="tab-item">
            <a class="tab-link" 
               :class="{ active: selectedType === 3 }"
               @click="selectTab(3)">
               <i class="fas fa-wallet me-2"></i>입출금
            </a>
          </li>
          <li class="tab-item">
            <a class="tab-link" 
               :class="{ active: selectedType === 1 }"
               @click="selectTab(1)">
               <i class="fas fa-piggy-bank me-2"></i>예금
            </a>
          </li>
          <li class="tab-item">
            <a class="tab-link" 
               :class="{ active: selectedType === 2 }"
               @click="selectTab(2)">
               <i class="fas fa-coins me-2"></i>적금
            </a>
          </li>
        </ul>
      </div>

      <!-- 정렬 버튼 -->
      <div class="sort-buttons">
        <button class="sort-btn" :class="{ active: sortBy === 'intr_rate2' }" @click="sortFunction('intr_rate2')">
          <i class="fas fa-percentage me-2"></i>금리순
        </button>
        <button class="sort-btn" :class="{ active: sortBy === '' }" @click="sortFunction('')">
          <i class="fas fa-font me-2"></i>상품명순
        </button>
      </div>
    </div>

    <!-- 상품 리스트 -->
    <ProductList :products="sortedProducts" />
    
  </div>
</template>

<style scoped>
.product-view-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;  /* 좌우 패딩 줄임 */
}

.carousel-wrapper {
  width: 100%;
  margin: 0 auto;
  /* 캐러셀의 여백 조정 */
  margin-bottom: 2rem;
}

.content-section {
  margin: 2rem 0;
  width: 100%;  /* 전체 너비 사용 */
}

/* 탭 스타일링 */
.tab-container {
  margin-bottom: 1.5rem;
  border-bottom: 2px solid #e9ecef;
}

.custom-tabs {
  display: flex;
  list-style: none;
  padding: 0;
  margin: 0;
  gap: 0.5rem;
}

.tab-item {
  margin-bottom: -2px;
}

.tab-link {
  display: inline-block;
  padding: 1rem 1.5rem;
  color: #666;
  text-decoration: none;
  font-weight: 600;
  border-bottom: 2px solid transparent;
  transition: all 0.3s ease;
  cursor: pointer;
}

.tab-link:hover {
  color: #196DDC;
}

.tab-link.active {
  color: #196DDC;
  border-bottom: 2px solid #196DDC;
}

/* 정렬 버튼 스타일링 */
.sort-buttons {
  display: flex;
  justify-content: flex-end;
  gap: 0.5rem;
  margin: 1rem 0;
}

.sort-btn {
  padding: 0.5rem 1rem;
  border: 1px solid #196DDC;
  background-color: white;
  color: #196DDC;
  border-radius: 20px;
  font-weight: 600;
  transition: all 0.3s ease;
  cursor: pointer;
}

.sort-btn:hover {
  background-color: #f8f9fa;
  transform: translateY(-2px);
}

.sort-btn.active {
  background-color: #196DDC;
  color: white;
}

/* 반응형 디자인 */
@media (max-width: 768px) {
  .custom-tabs {
    flex-wrap: wrap;
  }

  .tab-link {
    padding: 0.8rem 1rem;
  }

  .sort-buttons {
    flex-wrap: wrap;
  }

  .sort-btn {
    width: 100%;
    margin: 0.25rem 0;
  }
}
</style>

<script setup>
import { computed, onMounted, ref } from 'vue';
import ProductList from '@/components/products/ProductList.vue';
import { useProductStore } from '@/stores/modules/product';
import ProductCarousel from '@/components/products/ProductCarousel.vue';


const sortBy = ref('')

const store =useProductStore()

onMounted(()=>{ 
  store.productList()
})

const sortFunction = (order) => {
sortBy.value = order; // 정렬 기준을 설정
}

const sortedProducts = computed(() => {
// const products = [...store.products]; // 배열 복사
  const filtered= selectedType.value === 4
  ? store.products
  : store.products.filter(product => product.type === selectedType.value)
if (sortBy.value === 'intr_rate2') {
  console.log('Sorting by:', sortBy.value)  // 이 부분을 통해 sortBy.value가 바뀌는지 확인
  return filtered.sort((a, b) => b.rates.intr_rate2 - a.rates.intr_rate2)  // 금리순 정렬
} else {
  return filtered.sort((a, b) => a.fin_prdt_nm.localeCompare(b.fin_prdt_nm))  // 이름순 정렬
}
})

//  1: 예금, 2: 적금, 3: 입출금
const selectedType=ref(1)

const selectTab = (type)=>{
  selectedType.value=type;
}

</script>