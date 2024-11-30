<template>
    <div v-if="question" class="question-detail">
      <h2 class="detail-title">문의 상세</h2>
      <div class="detail-card">
        <div class="detail-item">
          <strong>카테고리 </strong> {{ question.category }}
        </div>
        <div class="detail-item">
          <strong>제목 </strong> {{ question.title }}
        </div>
        <div class="detail-item content">
          <strong>내용 </strong> {{ question.content }}
        </div>
        <div class="detail-info">
          <div class="detail-item">
            <strong>작성자 </strong> {{ question.username }}
          </div>
          <div class="detail-item">
            <strong>작성일 </strong> {{ question.created_at }}
          </div>
        </div>
      </div>
  
      <!-- 답변 컴포넌트 -->
      <QandADetailAnswer v-if="question" :questionId="question.id" />
  
      <!-- 버튼 그룹 -->
      <div class="button-group">
        <RouterLink :to="{name:'QandAUpdateView'}" class="edit-button">수정하기</RouterLink>
        <button @click="deleteQuestion" class="delete-button">삭제하기</button>
        <RouterLink :to="{name:'QandAView'}" class="back-button">목록으로</RouterLink>
      </div>
    </div>
  </template>
<script setup>
import { computed, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useHelpStore } from '@/stores/modules/help';
import { RouterLink } from 'vue-router';
import { useMemberStore } from '@/stores/modules/member';
import QandADetailAnswer from '@/components/helps/QandADetailAnswer.vue';

defineProps({
    question:{
        type: Object
    }
})

const store = useHelpStore()
const memberStore = useMemberStore()
const route = useRoute()
const router = useRouter() // router 추가


// 삭제 함수
const deleteQuestion = async () => {
    await store.deleteQuestion(route.params.id)
    // router.push('/qna')
}

// 컴포넌트 마운트 시 실행
onMounted(async () => {
    await memberStore.getUserInfo()
    
})
</script>

<style scoped>
.question-detail {
  padding: 30px;
}

.detail-title {
  font-size: 24px;
  color: #333;
  margin-bottom: 20px;
  font-weight: normal;
}

.detail-card {
  background-color: #f8f9fa;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 20px;
}

.detail-item {
  padding: 12px 0;
  border-bottom: 1px solid #eee;
}

.detail-item:last-child {
  border-bottom: none;
}

.detail-item.content {
  white-space: pre-line;
}

.detail-info {
  display: flex;
  justify-content: space-between;
  margin-top: 10px;
}

.button-group {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 20px;
}

.edit-button,
.delete-button,
.back-button {
  padding: 8px 20px;
  border-radius: 4px;
  font-size: 14px;
  cursor: pointer;
  text-decoration: none;
  transition: all 0.3s ease;
}

.edit-button {
  background-color: #196DDC;
  color: white;
  border: none;
}

.delete-button {
  background-color: #dc3545;
  color: white;
  border: none;
}

.back-button {
  background-color: #f8f9fa;
  color: #666;
  border: 1px solid #ddd;
}

.button-group button:hover,
.button-group a:hover {
  transform: translateY(-2px);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}
</style>