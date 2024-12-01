<template>
  <div class="container">
    <!-- 헤더 섹션 -->
    <div class="page-header">
      <h1 class="page-title mb-4 mt-5">계좌이체</h1>
      <hr class="custom-hr">
    </div>
    <!-- 폼 컨테이너 -->
    <div class="transfer-form-container">
      <form @submit.prevent="transfer" class="transfer-form">
        <!-- 계좌 선택 및 잔액 -->
        <div class="form-section">
          <label for="account-select" class="form-label">내 계좌선택</label>
          <div class="account-card">
            <select v-model="selectedAccount" id="account-select" class="form-select">
              <option value="3020000011750">302-0000-9999-00</option>
            </select>
            <div class="account-balance">
              잔액 <span class="balance-amount" v-if="selectedAccount">{{ new Intl.NumberFormat().format(store.balance?.Ldbl || 0) }}원</span>
            </div>
          </div>

          <!-- 받는 분 정보 섹션 -->
          <div class="recipient-section">
            <div class="input-group">
              <input type="text" id="bank" v-model="bank" class="form-control" placeholder="받는 분 은행">
              <button type="button" @click="toggleBanks" class="btn btn-select">
                <i class="fas fa-building-columns me-2"></i>은행선택
              </button>
            </div>

            <div class="input-group mt-3">
              <input type="text" id="account" v-model="account" class="form-control" placeholder="받는 분 계좌번호">
              <button type="button" @click="toggleFavorites" class="btn btn-select">
                <i class="fas fa-star me-2"></i>즐겨찾기
              </button>
            </div>
          </div>

          <!-- 금액 입력 -->
          <div class="amount-section">
            <div class="input-group">
              <input type="text" id="money" v-model="money" class="form-control amount-input" placeholder="0">
              <span class="input-group-text">원</span>
            </div>
          </div>

          <!-- 메모 섹션 -->
          <div class="memo-section">
            <div class="memo-field">
              <label for="my-memo" class="form-label">내 통장 표시</label>
              <input type="text" id="memo" v-model="myMemo" class="form-control">
            </div>
            <div class="memo-field mt-3">
              <label for="recipient-memo" class="form-label">받는 분 통장 표시</label>
              <input type="text" id="recipient-memo" v-model="recipientMemo" class="form-control">
            </div>
          </div>

          <!-- 이체 버튼 -->
          <button type="submit" class="btn btn-transfer">
            <i class="fas fa-paper-plane me-2"></i>이체하기
          </button>
        </div>
      </form>
    </div>
  </div>
  <!-- 즐겨찾기 모달 -->
  <div v-if="showFavorites" class="modal-overlay" @click="toggleFavorites">
    <div class="modal fade show" style="display: block;" tabindex="-1" @click.stop>
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">즐겨찾기 계좌</h5>
            <button type="button" class="btn-close" @click="toggleFavorites"></button>
          </div>
          <div class="modal-body">
            <table class="table">
              <thead>
                <tr>
                  <th>별명</th>
                  <th>은행</th>
                  <th>계좌번호</th>
                  <th>예금주</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="favorite in memberStore.favorites" :key="favorite.id" @click="selectFavorite(favorite)" class="table-row">
                  <td><span class="division-box">{{ favorite.division }}</span></td>
                  <td>{{ favorite.bank_name }}</td>
                  <td>{{ favorite.recipient }}</td>
                  <td>{{ favorite.recipient_name }}</td>
                </tr>
              </tbody>
            </table>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="toggleFavorites">닫기</button>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- 은행선택 모달 -->
  <div v-if="showBanks" class="modal-overlay" @click="toggleBanks">
    <div class="modal fade show" style="display: block;" tabindex="-1" @click.stop>
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">은행목록</h5>
            <button type="button" class="btn-close" @click="toggleBanks"></button>
          </div>
          <div class="modal-body">
            <table class="table">
              <thead>
                <tr>
                  <th>#</th>
                  <th>은행</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(bank, index) in memberStore.banks" :key="bank.id" @click="selectBank(bank)" class="table-row">
                  <td><span class="division-box">{{ index+1 }}</span></td>
                  <td>{{ bank.name }}</td>
                </tr>
              </tbody>
            </table>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="toggleBanks">닫기</button>
          </div>
        </div>
      </div>
    </div>
  </div>

</template>


<script setup>
import { ref, onMounted, watch } from 'vue';
import { useTransferStore } from '@/stores/modules/transfer';
import { useMemberStore } from '@/stores/modules/member';
import { RouterLink } from 'vue-router';

const memberStore = useMemberStore();
const store = useTransferStore();

const money = ref(null);
const myMemo = ref(null);
const selectedAccount = ref(null);
const showFavorites = ref(false); // 즐겨찾기 모달 관련
const showBanks = ref(false) // 은행목록 모달 관련
const bank = ref(null);
const account = ref(null);

// 모달 토글 함수
const toggleFavorites = () => {
  showFavorites.value = !showFavorites.value;
};

const toggleBanks = () => {
  showBanks.value = !showBanks.value;
}

// 즐겨찾기 계좌 선택
const selectFavorite = (favorite) => {
  bank.value = favorite.bank_name;
  account.value = favorite.recipient;
  showFavorites.value = false; // 선택 후 모달 닫기
};

// 은행 선택
const selectBank = (selectedbank)=>{
  bank.value = selectedbank.name
  showBanks.value = false // 선택 후 모달 닫기
}

// 이체 함수
const transfer = () => {
  const payload = {
    money: money.value,
    myMemo: myMemo.value,
  };
  store.transfer(payload);
  money.value = '';
  myMemo.value = '';
  bank.value = null;
  account.value = null;
  selectedAccount.value = null;
};

// selectedAccount 변경 시 잔액 정보 갱신
watch(selectedAccount, async (newAccount) => {
  if (newAccount) {
    await store.balanceSearch();
  }
});

// 컴포넌트 마운트 시 즐겨찾기 목록 조회
onMounted(async () => {
  await memberStore.getFavorites();
  await memberStore.getBanks();
});
</script>

<style scoped>
/* 헤더 스타일 */
/* .container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
} */

.page-header {
  width: 100%;
  margin-bottom: 2rem;
}

.page-title {
  color: #196DDC;
  font-weight: 600;
  font-size: 2rem;
}

.custom-hr {
  border-color: #e0e0e0;
  margin: 1.5rem 0;
}

.transfer-title {
  color: #196DDC;
  font-weight: 600;
}

.custom-hr {
  border-color: #e0e0e0;
  margin: 2rem 0;
}

.transfer-container {
  display: flex;
  justify-content: center;
  padding: 2rem;
}

.transfer-form-container {
  background: white;
  border-radius: 16px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
  padding: 2rem;
  width: 800px;
  margin: 0 auto;
}

.transfer-form {
  max-width: 600px;
  margin: 0 auto;
}

.form-section {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.account-card {
  background: linear-gradient(145deg, #f8f9fa, #ffffff);
  border: 1px solid #e0e0e0;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.form-select {
  font-size: 1.1rem;
  font-weight: 500;
  border: none;
  background-color: transparent;
  padding: 0.5rem 0;
}

.account-balance {
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px dashed #e0e0e0;
  color: #666;
}

.balance-amount {
  color: #196DDC;
  font-weight: 600;
  font-size: 1.2rem;
}

.input-group {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  border-radius: 8px;
  overflow: hidden;
}

.btn-select {
  background-color: #f8f9fa;
  border: 1px solid #e0e0e0;
  color: #196DDC;
  min-width: 120px;
  transition: all 0.3s ease;
}

.btn-select:hover {
  background-color: #196DDC;
  color: white;
}

.amount-input {
  font-size: 1.3rem;
  font-weight: 600;
  text-align: right;
  padding: 1rem;
}

.input-group-text {
  background-color: #f8f9fa;
  border: 1px solid #e0e0e0;
  color: #666;
}

.memo-field label {
  color: #666;
  font-size: 0.9rem;
  margin-bottom: 0.5rem;
}

.btn-transfer {
  background-color: #196DDC;
  color: white;
  padding: 1rem;
  font-weight: 600;
  border-radius: 8px;
  width: 100%;
  margin-top: 1rem;
  transition: all 0.3s ease;
}

.btn-transfer:hover {
  background-color: #1557b0;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(25, 109, 220, 0.2);
}

/* 모달 스타일 개선 */
.modal-content {
  border-radius: 16px;
  border: none;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

.modal-header {
  border-bottom: 1px solid #f0f0f0;
  padding: 1.5rem;
}

.modal-body {
  padding: 1.5rem;
}

.table-row {
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.table-row:hover {
  background-color: #f8f9fa;
}

.division-box {
  background-color: #e9ecef;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.9rem;
}
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  z-index: 1050;
  display: flex;
  align-items: center;
  justify-content: center;
}

.modal-dialog {
  margin: 1.75rem auto;
  max-width: 500px;
}

.modal-content {
  border-radius: 16px;
  border: none;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

.modal-header {
  border-bottom: 1px solid #f0f0f0;
  padding: 1.5rem;
}

.modal-body {
  padding: 1.5rem;
}

.table-row {
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.table-row:hover {
  background-color: #f8f9fa;
}

.division-box {
  background-color: #e9ecef;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.9rem;
}

.btn-close:focus {
  box-shadow: none;
}

.modal-footer {
  border-top: 1px solid #f0f0f0;
  padding: 1rem 1.5rem;
}

.table {
  margin-bottom: 0;
}

.table th {
  border-bottom: 2px solid #dee2e6;
  font-weight: 600;
  color: #495057;
}

.table td {
  vertical-align: middle;
  padding: 1rem 0.75rem;
}
</style>