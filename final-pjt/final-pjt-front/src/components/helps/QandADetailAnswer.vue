<template>
    <div class="answer-container">
      <!-- 답변 내용 표시 -->
      <div v-if="answer" class="answer-section">
        <h3 class="answer-title">답변</h3>
        <div class="answer-card">
          <div class="answer-content">{{ answer.content }}</div>
          <div class="answer-info">
            <span class="answer-author">{{ answer.username }}</span>
            <span class="answer-date">{{ answer.created_at }}</span>
          </div>
        </div>
      </div>
  
      <!-- 답변 작성 폼 -->
      <div v-if="!answer" class="answer-form">
        <h3 class="answer-title">답변 작성</h3>
        <form @submit.prevent="submitAnswer">
          <div class="form-group">
            <textarea 
              v-model="answerContent" 
              placeholder="답변을 입력하세요"
              rows="4"
              required
            ></textarea>
          </div>
          <div class="form-actions">
            <button type="submit" class="submit-button">답변 등록</button>
          </div>
        </form>
      </div>
    </div>
  </template>
<script setup>
import { ref, onMounted } from 'vue'
import { useHelpStore } from '@/stores/modules/help'
import { useMemberStore } from '@/stores/modules/member'

const props = defineProps({
    questionId: {
        type: [String, Number],
        required: true
    }
})

const store = useHelpStore()
const memberStore = useMemberStore()
const answer = ref(null)
const answerContent = ref('')

// 답변 데이터 로드
const loadAnswer = async () => {
    try {
        const answerData = await store.getAnswerForQuestion(props.questionId)
        if (answerData) {
            answer.value = answerData
            // console.log('답변 데이터:', answer.value)
        }
    } catch (error) {
        // console.error('답변 데이터 로드 실패:', error)
    }
}

// 답변 생성
const submitAnswer = async () => {
    try {
        const payload = {
            question_id: props.questionId,
            content: answerContent.value
        }
        await store.createAnswer(payload)
        answerContent.value = '' // 폼 초기화
        await loadAnswer() // 답변 데이터 새로고침
    } catch (error) {
        console.error('답변 생성 실패:', error)
        alert('답변 작성에 실패했습니다.')
    }
}

// 컴포넌트 마운트 시 답변 데이터 로드
onMounted(async () => {
    await loadAnswer()
})
</script>

<style scoped>
.answer-container {
  margin-top: 30px;
}

.answer-title {
  font-size: 20px;
  color: #333;
  margin-bottom: 15px;
  font-weight: normal;
}

.answer-card {
  background-color: #f8f9fa;
  border-radius: 8px;
  padding: 20px;
}

.answer-content {
  white-space: pre-line;
  margin-bottom: 15px;
  color: #333;
}

.answer-info {
  display: flex;
  justify-content: space-between;
  color: #666;
  font-size: 14px;
  padding-top: 15px;
  border-top: 1px solid #eee;
}

.form-group {
  margin-bottom: 15px;
}

textarea {
  width: 100%;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
  resize: vertical;
  background-color: #f8f9fa;
}

textarea:focus {
  outline: none;
  border-color: #196DDC;
  box-shadow: 0 0 0 2px rgba(54, 153, 245, 0.2);
}

.form-actions {
  display: flex;
  justify-content: flex-end;
}

.submit-button {
  padding: 8px 20px;
  background-color: #808080;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.3s ease;
}

.submit-button:hover {
  background-color: #196DDC;
  transform: translateY(-2px);
  box-shadow: 0 2px 4px rgba(54, 153, 245, 0.3);
}
</style>