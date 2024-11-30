<template>
    <div class="detail-container">
      <div v-if="question" class="detail-content">
        <QandADetailItem :question="question" />
      </div>
      <div v-else class="loading-state">
        <p>로딩 중...</p>
      </div>
    </div>
  </template>

<script setup>
import QandADetailItem from '@/components/helps/QandADetailItem.vue'
import { onMounted,ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useHelpStore } from '@/stores/modules/help'

const route = useRoute()
const router = useRouter()
const store = useHelpStore()
const question = ref(null)

const loadQuestion = async () => {
    try {
        const data = await store.getQuestionDetail(route.params.id)
        question.value = data
    } catch (error) {
        console.error('질문 데이터 로드 실패:', error)
        router.push('/qanda')
    }
}

onMounted(async () => {
    loadQuestion()
})
</script>

<style scoped>
.detail-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.detail-content {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.loading-state {
  text-align: center;
  padding: 40px;
  background-color: white;
  border-radius: 8px;
  color: #666;
}
</style>