<template>
  <div class="transaction-item">
    <div class="d-flex justify-content-between align-items-center mb-3">
      <!-- 왼쪽: 날짜와 거래처 -->
      <div class="transaction-info">
        <div class="date">{{ formatDate(item.Trdd) }}</div>
        <div class="recipient" style="font-weight: bold">{{ item.BnprCntn }}</div>
        <div :class="['memo', {'text-danger': item.TrnsAfAcntBlncSmblCd === '+', 'text-primary': item.TrnsAfAcntBlncSmblCd === '-'}]">
          {{ item.TrnsAfAcntBlncSmblCd === '+' ? '출금' : '입금' }}
        </div>
      </div>

      <!-- 오른쪽: 금액 -->
      <div class="amount-info text-end">
        <div :class="['amount', {'text-danger': item.TrnsAfAcntBlncSmblCd === '+', 'text-primary': item.TrnsAfAcntBlncSmblCd === '-'}]">
          {{ formatAmount(item.Tram) }}원
        </div>
      </div>
    </div>
    <hr>
  </div>
</template>

<script setup>

const props = defineProps({
  item: {
    type: Object,
    required: true
  }
})

// 날짜 포맷팅 함수
const formatDate = (date) => {
  return `${date.slice(0, 4)}.${date.slice(4, 6)}.${date.slice(6, 8)}`
}

// 금액 포맷팅 함수
const formatAmount = (amount) => {
  return new Intl.NumberFormat().format(amount)
}

// 입금/출금 구분에 따른 클래스 반환
const getAmountClass = (type) => {
  return type === '출금' ? 'text-primary' : 'text-danger'
}

</script>

<style scoped>
.transaction-item {
  padding: 10px 0;
}

.date {
  font-size: 0.9rem;
  color: #666;
  margin-bottom: 4px;
}

.recipient {
  font-weight: 500;
  font-size: 1.1rem;
  margin-bottom: 4px;
}

.memo {
  font-size: 0.85rem;
}

.amount {
  font-weight: 500;
  font-size: 1.1rem;
  margin-bottom: 8px;
}

.text-danger {
  color: #dc3545;
}

.text-primary {
  color: #0d6efd;
}

.btn-memo {
  font-size: 0.85rem;
  padding: 2px 8px;
  background-color: #e9ecef;
  border: 1px solid #dee2e6;
  border-radius: 4px;
  color: #666;
}

.btn-memo:hover {
  background-color: #dee2e6;
}

hr {
  margin: 10px 0;
  color: #dee2e6;
}


.text-danger {
  color: #ff3b30 !important;  /* 출금 금액 색상 - 빨간색 */
}

.text-primary {
  color: #007aff !important;  /* 입금 금액 색상 - 파란색 */
}

.amount {
  font-size: 1.1rem;
  font-weight: 600;  /* 또는 font-weight: bold; */
  margin-bottom: 8px;
}

</style>