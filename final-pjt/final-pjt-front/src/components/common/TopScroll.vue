<template>
  <div>
    <Transition name="fade">
      <button 
        v-show="showButton"
        type="button" 
        class="btn btn-warning btn-floating btn-lg text-light" 
        id="btn-back-to-top"
        @click="backToTop"
      >
        <i class="fas fa-arrow-up fa-lg"></i>
      </button>
    </Transition>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const showButton = ref(false)

const scrollFunction = () => {
  if (
    document.body.scrollTop > 20 ||
    document.documentElement.scrollTop > 20
  ) {
    showButton.value = true
  } else {
    showButton.value = false
  }
}

const backToTop = () => {
  document.body.scrollTop = 0
  document.documentElement.scrollTop = 0
}

onMounted(() => {
  window.addEventListener('scroll', scrollFunction)
})

onUnmounted(() => {
  window.removeEventListener('scroll', scrollFunction)
})
</script>

<style scoped>
#btn-back-to-top {
  position: fixed;
  bottom: 40px;    /* 20px에서 40px로 변경 */
  right: 40px;     /* 20px에서 40px로 변경 */
  z-index: 99;
  width: 50px;     /* 버튼 너비 */
  height: 50px;    /* 버튼 높이 */
  border-radius: 50%;  /* 동그란 모양 유지 */
  display: flex;   /* 아이콘 중앙 정렬을 위해 */
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;  /* 아이콘 크기 증가 */
}
.btn .btn-warning {
  background-color: #FCC800;
}
/* 트랜지션 효과 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>