<template>
  <div class="customer-center">

    
    <table class="qa-table">
      <thead>
        <tr class="table-header">
          <th>카테고리</th>
          <th>내용</th>
          <th>작성자</th>
          <th>등록일</th>
          <th>답변여부</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(item, index) in store.questions" 
            :key="index"
            @click="checkPassword(item)"
            class="table-row">
          <td>{{ item.category }}</td>
          <td>{{ item.title }}</td>
          <td>{{ item.username }}</td>
          <td>{{ item.created_at }}</td>
          <td>{{ item.answer_status }}</td>
        </tr>
      </tbody>
    </table>

    <!-- 비밀번호 확인 모달 -->
    <div v-if="showPasswordModal" class="modal">
      <div class="modal-content">
        <h3>비밀번호 확인</h3>
        <p>비공개 글입니다. 비밀번호를 입력해주세요.</p>
        <input 
          type="password" 
          v-model="inputPassword" 
          placeholder="비밀번호를 입력하세요"
          maxlength="4"
        >
        <div class="modal-buttons">
          <button class="confirm-btn" @click="confirmPassword">확인</button>
          <button class="cancel-btn" @click="showPasswordModal = false">취소</button>
        </div>
      </div>
    </div>

    <!-- 페이지네이션 -->
    <div class="pagination">
      <button class="page-btn">&lt;&lt;</button>
      <button v-for="n in 1" :key="n" class="page-btn" :class="{ 'active': n === 1 }">
        {{ n }}
      </button>
      <button class="page-btn">&gt;&gt;</button>
    </div>

    <!-- 문의하기 버튼 -->
    <div class="button-container">
      <RouterLink :to="{ name: 'QandACreateView' }" class="write-button">
        문의하기
      </RouterLink>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useHelpStore } from '@/stores/modules/help'
import { RouterLink } from 'vue-router'
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const store = useHelpStore()

const showPasswordModal = ref(false)
const inputPassword = ref('')
const selectedQuestion = ref(null)

const checkPassword = (item) => {
  console.log('Clicked item:', item)  // 디버깅
  selectedQuestion.value = item  // item 전체를 먼저 저장
  console.log('Selected Question:', selectedQuestion.value)  // 디버깅

  if(item.private) {
    showPasswordModal.value = true
    console.log('Modal should show:', showPasswordModal.value)  // 디버깅
  } else {
    router.push(`/qanda/${item.id}`)
  }
}

const confirmPassword = () => {
  console.log('Confirming password for:', selectedQuestion.value)  // 디버깅
  if (parseInt(inputPassword.value) === selectedQuestion.value.password) {
    showPasswordModal.value = false
    inputPassword.value = ''  // 비밀번호 입력값 초기화
    router.push(`/qanda/${selectedQuestion.value.id}`)
  } else {

    console.log(selectedQuestion.value.password)
    console.log(inputPassword.value)
    alert('비밀번호가 일치하지 않습니다.')
    inputPassword.value = ''  // 비밀번호 입력값 초기화
  }
}

onMounted(() => {
  store.QandA()
})
</script>

<style scoped>
/* 기존 스타일 유지 */

/* 모달 관련 스타일 추가 */
.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  width: 300px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.modal-content h3 {
  margin-bottom: 10px;
  color: #333;
}

.modal-content input {
  width: 100%;
  padding: 8px;
  margin: 10px 0;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.modal-buttons {
  margin-top: 15px;
  display: flex;
  justify-content: center;
  gap: 10px;
}

.confirm-btn, .cancel-btn {
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
}

.confirm-btn {
  background-color: #196DDC;
  border: 1px solid #ccc;
}

.cancel-btn {
  background-color: #fff;
  border: 1px solid #ccc;
}

.confirm-btn:hover, .cancel-btn:hover {
  opacity: 0.8;
}

.customer-center {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.center-title {
  text-align: center;
  font-size: 24px;
  margin-bottom: 30px;
}

.tab-container {
  display: flex;
  justify-content: center;
  gap: 10px;
  margin-bottom: 20px;
}

.tab-button {
  padding: 10px 30px;
  border: none;
  border-radius: 20px;
  background-color: #f5f5f5;
  cursor: pointer;
  font-size: 16px;
}

.tab-button.active {
  background-color: #3699f5;
  color: white;
}

.qa-table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 20px;
  background-color: white;
}

.table-header {
  background-color: #f0f7ff;
}

.qa-table th {
  padding: 15px;
  text-align: center;
  border-top: 1px solid #ddd;
  border-bottom: 1px solid #ddd;
  font-weight: normal;
}

.qa-table td {
  padding: 15px;
  text-align: center;
  border-bottom: 1px solid #ddd;
}

.table-row {
  cursor: pointer;
  transition: background-color 0.2s;
}

.table-row:hover {
  background-color: #f8f9fa;
}

.pagination {
  display: flex;
  justify-content: center;
  gap: 5px;
  margin: 20px 0;
}

.page-btn {
  padding: 8px 12px;
  border: none;
  background-color: transparent;
  cursor: pointer;
  color: #666;
}

.page-btn.active {
  background-color: #e9f5ff;

  border-radius: 4px;
}

.button-container {
  display: flex;
  justify-content: flex-end;
  margin-top: 20px;
}

.write-button {
  padding: 8px 20px;
  background-color: white;
  border: 1px solid #ddd;
  border-radius: 4px;
  text-decoration: none;
  color: #333;
  font-size: 14px;
}

.write-button:hover {
  background-color: #f8f9fa;
}

/* 반응형 디자인 */
@media (max-width: 768px) {
  .qa-table {
    font-size: 14px;
  }
  
  .qa-table th,
  .qa-table td {
    padding: 10px 5px;
  }
  
  .tab-button {
    padding: 8px 20px;
    font-size: 14px;
  }
}
</style>
