<template>
    <div class="update-form">
      <h2 class="form-title">문의글 수정</h2>
      <form v-if="question" @submit.prevent="updateQuestion">
        <div class="form-group">
          <label for="category">카테고리</label>
          <select 
            id="category" 
            v-model="category"
            class="form-input"
          >
            <option value="1">이체서비스</option>
            <option value="2">금융상품</option>
            <option value="3">거래내역</option>
            <option value="4">자산관리 유형 서비스</option>
            <option value="5">회원가입 및 로그인</option>
            <option value="6">기타</option>
          </select>
        </div>
  
        <div class="form-group">
          <label for="title">제목</label>
          <input 
            type="text" 
            id="title"
            v-model="title"
            class="form-input"
            placeholder="제목을 입력하세요"
            required
          >
        </div>
  
        <div class="form-group">
          <label for="content">내용</label>
          <textarea 
            id="content"
            v-model="content"
            class="form-textarea"
            rows="10"
            placeholder="내용을 입력하세요"
            required
          ></textarea>
        </div>
  
        <div class="form-group private-group">
            <div class="toggle-wrapper">
            <label class="toggle">
                <input 
                type="checkbox" 
                id="isprivate"
                v-model="isprivate"
                >
                <span class="slider"></span>
                <span class="toggle-label">비공개</span>
            </label>
            </div>

            <input 
            v-if="isprivate"
            type="password" 
            id="password"
            v-model="password"
            class="form-input"
            placeholder="비밀번호를 입력하세요"
            >
        </div>
  
        <div class="button-group">
          <button type="submit" class="submit-button">수정하기</button>
          <RouterLink :to="{name:'QandAView'}" class="back-button">목록으로</RouterLink>
        </div>
      </form>
    </div>
  </template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useHelpStore } from '@/stores/modules/help'

const router = useRouter()
const route = useRoute()
const store = useHelpStore()
const question = ref(null)

// 폼 데이터
const category = ref('')
const title = ref('')
const content = ref('')
const isprivate = ref(false)
const password = ref('')

// 기존 데이터 불러오기
onMounted(async () => {
    try {
        // await를 사용하여 데이터를 기다림
        const data = await store.getQuestionDetail(route.params.id)
        question.value = data
        
        if (data) {
            const categoryMapping = {
                '이체서비스': '1',
                '금융상품': '2',
                '거래내역': '3',
                '자산관리 유형 서비스': '4',
                '회원가입 및 로그인': '5',
                '기타': '6'
            }
            category.value = categoryMapping[data.category] || '1'
            title.value = data.title
            content.value = data.content
            isprivate.value = data.private
            password.value = data.password
        }
    } catch (error) {
        console.error('데이터 로드 실패:', error)
        router.push('/qanda')
    }
})


// 수정 함수 - store의 updateQuestion 사용
const updateQuestion = () => {
    const payload = {
        id: route.params.id,
        category: category.value,
        title: title.value,
        content: content.value,
        isprivate: isprivate.value,
        password: password.value
    }
    store.updateQuestion(payload)
}



</script>

<style scoped>
.update-form {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.form-title {
  text-align: center;
  font-size: 24px;
  color: #333;
  margin-bottom: 30px;
  font-weight: normal;
  border-bottom: 1px solid #ddd;
  padding-bottom: 20px;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  color: #333;
  font-size: 14px;
}

.form-input,
.form-textarea {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  background-color: #f8f9fa;
  font-size: 14px;
}

.form-textarea {
  resize: vertical;
  min-height: 200px;
}

.private-group {
  margin-top: 20px;
}

.checkbox-wrapper {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 10px;
}

.checkbox-wrapper input[type="checkbox"] {
  margin: 0;
}

.button-group {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 30px;
}

.submit-button,
.back-button {
  padding: 8px 20px;
  border-radius: 4px;
  font-size: 14px;
  cursor: pointer;
  text-decoration: none;
  transition: all 0.3s ease;
}

.submit-button {
  background-color: #196DDC;
  color: #ffffff;
  border: none;
}

.back-button {
  display: inline-block;
  background-color: #f8f9fa;
  color: #4e4e4e;
  border: 1px solid #ddd;
  text-align: center;
}

.submit-button:hover,
.back-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.submit-button:hover {
  background-color: #196DDC;
}

.back-button:hover {
  background-color: #e9ecef;
}

/* 포커스 효과 */
.form-input:focus,
.form-textarea:focus {
  outline: none;
  border-color: #196DDC;
  box-shadow: 0 0 0 2px rgba(183, 220, 143, 0.2);
}

/* 반응형 디자인 */
@media (max-width: 768px) {
  .update-form {
    padding: 10px;
  }

  .button-group {
    flex-direction: column;
  }

  .submit-button,
  .back-button {
    width: 100%;
  }
}



.toggle-wrapper {
  margin-bottom: 15px;
}

.toggle {
  position: relative;
  display: inline-flex;
  align-items: center;
  cursor: pointer;
}

.toggle input {
  opacity: 0;
  width: 0;
  height: 0;
}

.slider {
  position: relative;
  display: inline-block;
  width: 48px;
  height: 24px;
  background-color: #e9ecef;
  border-radius: 24px;
  transition: .4s;
  margin-right: 10px;
}

.slider:before {
  position: absolute;
  content: "";
  height: 20px;
  width: 20px;
  left: 2px;
  bottom: 2px;
  background-color: white;
  border-radius: 50%;
  transition: .4s;
}

.toggle input:checked + .slider {
  background-color: #196DDC;
}

.toggle input:checked + .slider:before {
  transform: translateX(24px);
}

.toggle-label {
  color: #333;
  font-size: 14px;
}

/* 호버 효과 */
.toggle:hover .slider {
  box-shadow: 0 0 1px #196DDC;
}

.toggle input:checked:hover + .slider {
  background-color: #196DDC;
}
</style>