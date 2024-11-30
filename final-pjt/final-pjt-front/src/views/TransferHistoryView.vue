<template>
  <div class="transfer-container">
    <!-- 헤더 섹션 통일 -->
    <div class="page-header">
      <div class="d-flex justify-content-between align-items-center">
        <h1 class="page-title mb-4 mt-5">이체내역</h1>
        <RouterLink :to="{name: 'HomeView'}" class="btn btn-home">
          <i class="fas fa-home me-2"></i>홈으로
        </RouterLink>
      </div>
      <hr class="custom-hr">
    </div>
    <!-- 조회 폼 -->
    <div class="search-container">
      <form @submit.prevent="transferHistory" class="search-form">
        <!-- 정렬 옵션 -->
        <div class="filter-section">
          <div class="filter-group">
            <div class="form-check custom-radio">
              <input class="form-check-input" type="radio" name="sortType" id="recent" value="recent" v-model="sortType">
              <label class="form-check-label" for="recent">최신순</label>
            </div>
            <div class="form-check custom-radio">
              <input class="form-check-input" type="radio" name="sortType" id="old" value="old" v-model="sortType">
              <label class="form-check-label" for="old">과거순</label>
            </div>
          </div>

          <!-- 거래 유형 필터 -->
          <div class="filter-group">
            <div class="form-check custom-radio">
              <input class="form-check-input" type="radio" name="transactionType" id="all" value="all" v-model="transactionType">
              <label class="form-check-label" for="all">전체</label>
            </div>
            <div class="form-check custom-radio">
              <input class="form-check-input" type="radio" name="transactionType" id="withdraw" value="withdraw" v-model="transactionType">
              <label class="form-check-label" for="withdraw">입금</label>
            </div>
            <div class="form-check custom-radio">
              <input class="form-check-input" type="radio" name="transactionType" id="deposit" value="deposit" v-model="transactionType">
              <label class="form-check-label" for="deposit">출금</label>
            </div>
          </div>
        </div>

        <!-- 날짜 선택 -->
        <div class="date-range">
          <input type="date" id="insymd" v-model="formattedInsymd" class="form-control date-input" :max="maxDate">
          <span class="date-separator">~</span>
          <input type="date" id="ineymd" v-model="formattedIneymd" class="form-control date-input" :max="maxDate">
        </div>

        <!-- 검색창 -->
        <div class="search-field">
          <input type="text" class="form-control search-input" placeholder="받는 분 검색" v-model="searchQuery">
          <button type="submit" class="btn btn-search">
            <i class="fas fa-search me-2"></i>조회
          </button>
        </div>
      </form>
    </div>

    <hr class="custom-hr">

    <!-- 거래내역 리스트 -->
    <div class="transaction-list">
      <transferHistoryItem v-for="item in sortedAndFilteredHistory" :key="item.id" :item="item"/>
    </div>
  </div>
</template>

<style scoped>
.transfer-history-container {
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.header-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.transfer-title {
  color: #196DDC;
  font-weight: 600;
}

.custom-hr {
  border-color: #e0e0e0;
  margin: 2rem 0;
}

.btn-home {
  background-color: #196DDC;
  color: white;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.btn-home:hover {
  background-color: #1557b0;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(25, 109, 220, 0.2);
}

.search-container {
  background: white;
  border-radius: 16px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
  padding: 2rem;
  margin-bottom: 2rem;
}

.search-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.filter-section {
  display: flex;
  gap: 2rem;
  flex-wrap: wrap;
}

.filter-group {
  display: flex;
  gap: 1.5rem;
  align-items: center;
}

.custom-radio .form-check-input:checked {
  background-color: #196DDC;
  border-color: #196DDC;
}

.date-range {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.date-input {
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 0.75rem;
  background-color: #f8f9fa;
  cursor: pointer;
  transition: border-color 0.3s ease;
}

.date-input:focus {
  border-color: #196DDC;
  box-shadow: 0 0 0 2px rgba(25, 109, 220, 0.1);
}

.date-separator {
  color: #666;
  font-weight: 500;
}

.search-field {
  display: flex;
  gap: 1rem;
}

.search-input {
  flex: 1;
  border-radius: 8px;
  border: 1px solid #e0e0e0;
  padding: 0.75rem 1rem;
  transition: all 0.3s ease;
}

.search-input:focus {
  border-color: #196DDC;
  box-shadow: 0 0 0 2px rgba(25, 109, 220, 0.1);
}

.btn-search {
  background-color: #196DDC;
  color: white;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.btn-search:hover {
  background-color: #1557b0;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(25, 109, 220, 0.2);
}

.transaction-list {
  background: white;
  border-radius: 16px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
  padding: 1.5rem;
}

@media (max-width: 768px) {
  .search-form {
    gap: 1rem;
  }

  .filter-section {
    flex-direction: column;
    gap: 1rem;
  }

  .date-range {
    flex-direction: column;
    width: 100%;
  }

  .search-field {
    flex-direction: column;
  }

  .btn-search {
    width: 100%;
  }
}
</style>

<script setup>
import transferHistoryItem from '@/components/transfer/transferHistoryItem.vue'
import { useTransferStore } from '@/stores/modules/transfer'
import { onMounted, ref, computed } from 'vue'

const store = useTransferStore()
const now = new Date()
const searchQuery = ref('')  // 검색어를 저장할 반응형 변수
const sortType = ref('recent')  // 기본값을 최신순으로 설정
const transactionType = ref('all')  // 기본값은 '전체'로 설정



// 검색어와 정렬 조건을 모두 적용한 computed 속성
const sortedAndFilteredHistory = computed(() => {
  // store.history가 없거나 배열이 아닌 경우 빈 배열 반환
  if (!store.history || !Array.isArray(store.history)) {
    return []
  }

  let result = [...store.history]  // 원본 배열을 복사

  // 입출금 필터링
  if (transactionType.value !== 'all') {
      result = result.filter(item => {
        if (transactionType.value === 'withdraw') {
          // 출금 필터링 (금액이 음수인 경우)
          return parseFloat(item.Tram) < 0
        } else {
          // 입금 필터링 (금액이 양수인 경우)
          return parseFloat(item.Tram) > 0
        }
      })
    }

    // 검색어 필터링
    if (searchQuery.value) {
      result = result.filter(item => 
        item.BnprCntn.toLowerCase().includes(searchQuery.value.toLowerCase())
      )
    }

    // 정렬 적용
    result.sort((a, b) => {
      const dateA = a.Trdd + a.TrTm
      const dateB = b.Trdd + b.TrTm
      return sortType.value === 'recent' 
        ? dateB.localeCompare(dateA)
        : dateA.localeCompare(dateB)
    })

    return result
  })


// 검색어에 따라 필터링된 거래내역을 반환하는 computed 속성
const filteredHistory = computed(() => {
  if (!searchQuery.value) {
    // 검색어가 없으면 전체 리스트 반환
    return store.history
  }
  // 검색어가 있으면 받는 분(BnprCntn)으로 필터링
  return store.history.filter(item => 
    item.BnprCntn.toLowerCase().includes(searchQuery.value.toLowerCase())
  )
})




// YYYYMMDD 형식의 날짜
const currentDate = now.getFullYear() +
                   String(now.getMonth() + 1).padStart(2, '0') +
                   String(now.getDate()).padStart(2, '0')

// YYYY-MM-DD 형식의 날짜 (달력 입력용)
const maxDate = now.toISOString().split('T')[0]

const insymd = ref(currentDate)
const ineymd = ref(currentDate)

// YYYYMMDD <-> YYYY-MM-DD 변환을 위한 computed 속성
const formattedInsymd = computed({
  get: () => {
    const date = insymd.value
    return `${date.slice(0, 4)}-${date.slice(4, 6)}-${date.slice(6, 8)}`
  },
  set: (value) => {
    insymd.value = value.replace(/-/g, '')
  }
})

const formattedIneymd = computed({
  get: () => {
    const date = ineymd.value
    return `${date.slice(0, 4)}-${date.slice(4, 6)}-${date.slice(6, 8)}`
  },
  set: (value) => {
    ineymd.value = value.replace(/-/g, '')
  }
})




// 컴포넌트 마운트 시 초기 데이터 로드
onMounted(() => {
  const payload = {
    insymd: insymd.value,
    ineymd: ineymd.value
  }
  store.transferHistory(payload)
})

const transferHistory = function() {
  const payload = {
    insymd: insymd.value,
    ineymd: ineymd.value
  }
  store.transferHistory(payload)
}
</script>

<!-- <style scoped>
.search-box {
  background-color: #f8f9fa;
  border-radius: 8px;
  border: 1px solid #dee2e6;
}

.form-check-group {
  min-width: 200px;
}

.form-check-input:checked {
  background-color: #0d6efd;
  border-color: #0d6efd;
}

.date-input {
  width: 140px;
  padding: 0.375rem 0.75rem;
  cursor: pointer;
}

.form-control {
  border: 1px solid #dee2e6;
  height: 38px;
  font-size: 0.9rem;
}

.btn-primary {
  background-color: #0d6efd;
  border-color: #0d6efd;
  min-width: 80px;
}

.btn-primary:hover {
  background-color: #0b5ed7;
  border-color: #0b5ed7;
}

input[type="date"]::-webkit-calendar-picker-indicator {
  cursor: pointer;
  padding: 5px;
  color: #0d6efd;
}

/* 반응형 조정 */
@media (max-width: 768px) {
  form {
    flex-direction: column;
    gap: 1rem;
  }
  
  .date-inputs {
    width: 100%;
  }
  
  .search-input {
    width: 100%;
  }
}

.search-input {
  position: relative;
}

.search-input input {
  width: 100%;
  padding-right: 30px;
}

/* 검색 결과가 없을 때 메시지 스타일 */
.no-results {
  text-align: center;
  padding: 20px;
  color: #666;
}
</style> -->