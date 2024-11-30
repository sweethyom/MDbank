<template>
    <div class="create-form">
      <h2 class="form-title">문의하기</h2>
      <form @submit.prevent="submitQuestion">
        <!-- 카테고리 선택 -->
        <div class="form-group">
          <label for="category">카테고리</label>
          <select 
            id="category"
            v-model="questionData.category"
            class="form-input"
            required
          >
            <option 
              v-for="category in categories" 
              :key="category.id" 
              :value="category.id"
            >
              {{ category.category }}
            </option>
          </select>
        </div>
  
        <div class="form-group">
          <label for="title">제목</label>
          <input 
            type="text" 
            id="title"
            v-model="questionData.title"
            class="form-input"
            placeholder="제목을 입력하세요"
            required
          >
        </div>
  
        <div class="form-group">
          <label for="content">내용</label>
          <textarea 
            id="content"
            v-model="questionData.content"
            class="form-textarea"
            rows="10"
            placeholder="내용을 입력하세요"
            required
          ></textarea>
        </div>
  
        <!-- 비공개 설정 -->
        <div class="form-group private-group">
          <div class="toggle-wrapper">
            <label class="toggle">
              <input 
                type="checkbox" 
                v-model="questionData.private"
              >
              <span class="slider"></span>
              <span class="toggle-label">비공개</span>
            </label>
          </div>
  
          <input 
            v-if="questionData.private"
            type="number" 
            v-model="questionData.password"
            class="form-input"
            placeholder="비밀번호 4자리"
            min="0000"
            max="9999"
            required
          >
        </div>
  
        <div class="button-group">
          <button type="submit" class="submit-button">등록</button>
          <RouterLink :to="{name:'QandAView'}" class="back-button">목록으로</RouterLink>
        </div>
      </form>
    </div>
  </template>

<script setup>
import { ref,onMounted } from 'vue';
import { useHelpStore } from '@/stores/modules/help';
import { useMemberStore } from '@/stores/modules/member';
import { useRouter } from 'vue-router';

const store = useHelpStore()
const memberStore = useMemberStore()
const router = useRouter()

const questionData = ref({
    title: '',
    content: '',
    private: false,
    password: null,
    category: 1
})


// 카테고리 데이터
const categories = ref([]);
// 서버에서 카테고리 데이터를 가져오는 함수
const fetchCategories = async () => {
    try {
        const response = await store.fetchCategories(); // 카테고리 데이터를 가져오는 Pinia 액션
        console.log(response)
        categories.value = response; // 서버에서 받은 데이터를 categories에 저장
        
    } catch (error) {
        console.error('카테고리 데이터 로드 실패:', error);

    }
};


onMounted(()=>{
    fetchCategories();
})

const submitQuestion = async () => {
    try {
        // 폼 데이터가 비어있는지 확인
        if (!questionData.value.title.trim()) {
            alert('제목을 입력해주세요.')
            return
        }
        if (!questionData.value.content.trim()) {
            alert('내용을 입력해주세요.')
            return
        }

        // 비공개글인 경우 비밀번호 확인
        if (questionData.value.private && !questionData.value.password) {
            alert('비공개 글은 비밀번호가 필요합니다.')
            return
        }

        console.log('전송할 데이터:', questionData.value)  // 디버깅용

        await store.createQuestion(questionData.value)
        alert('문의글이 등록되었습니다.')
        router.push({ name: 'QandAView' })
    } catch (error) {
        console.error('문의글 작성 실패:', error)
        if (error.response?.data) {
            alert(JSON.stringify(error.response.data))
        } else {
            alert('문의글 작성에 실패했습니다.')
        }
    }
}
</script>

<style scoped>
.create-form {
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

.file-input-wrapper {
  display: flex;
  gap: 10px;
}

.file-button {
  padding: 10px 20px;
  background-color: #f8f9fa;
  border: 1px solid #ddd;
  border-radius: 4px;
  color: #333;
  cursor: pointer;
  width: 100px;
}

.hidden-inputs {
  display: none;
}

.button-group {
  display: flex;
  justify-content: flex-end;
  margin-top: 30px;
}

.submit-button {
  padding: 8px 30px;
  background-color: #196DDC;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.3s ease;
}

.submit-button:hover {
  background-color: #196DDC;
  transform: translateY(-2px);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
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
  .create-form {
    padding: 10px;
  }

  .file-input-wrapper {
    flex-direction: column;
  }

  .submit-button {
    width: 100%;
  }
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
  padding: 8px 20px;
  background-color: #f8f9fa;
  color: #666;
  border: 1px solid #ddd;
  border-radius: 4px;
  text-decoration: none;
  font-size: 14px;
  transition: all 0.3s ease;
  text-align: center;
}

.submit-button:hover {
  background-color: #196DDC;
  transform: translateY(-2px);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.back-button:hover {
  background-color: #e9ecef;
  transform: translateY(-2px);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

/* 반응형 디자인 */
@media (max-width: 768px) {
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