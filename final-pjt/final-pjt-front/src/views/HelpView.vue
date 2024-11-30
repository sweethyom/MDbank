<template>
    <div class="help-container">
      <h2 class="help-title">고객센터</h2>
      
      <!-- 탭 메뉴 -->
      <div class="tab-container">
        <RouterLink 
          :to="{ name: 'QandAView' }" 
          class="tab-button"
          :class="{ active: $route.name === 'QandAView' }"
        >
          Q&A
        </RouterLink>
        <RouterLink 
          :to="{ name: 'FaqView' }" 
          class="tab-button"
          :class="{ active: $route.name === 'FaqView' }"
        >
          FAQ
        </RouterLink>
      </div>
  
      <!-- 라우터 뷰 -->
      <div class="help-content">
        <RouterView />
      </div>
    </div>
  </template>

<script setup >
import { RouterLink,RouterView } from 'vue-router';

</script>
<style scoped>
.help-container {
  max-width: 1200px;
  margin: 40px auto;
  padding: 0 20px;
}

.help-title {
  text-align: center;
  color: #333;
  margin-bottom: 30px;
  font-size: 24px;
}

.tab-container {
  display: flex;
  justify-content: center;
  gap: 10px;
  margin-bottom: 30px;
  background-color: #fff;
  padding: 20px 0;
}

.tab-button {
  padding: 12px 60px;
  text-decoration: none;
  color: #666;
  font-size: 16px;
  border: 1px solid #ddd;
  border-radius: 25px;
  transition: all 0.3s ease;
  background-color: white;
  /* 그림자 효과 추가 */
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.tab-button:hover {
  background-color: #f8f9fa;
  transform: translateY(-2px);
  /* 호버시 그림자 강화 */
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.tab-button.active {
  background-color: #3699f5;
  color: white;
  border-color: #3699f5;
  /* 활성화된 탭의 그림자 */
  box-shadow: 0 4px 8px rgba(54, 153, 245, 0.3);
}

/* 클릭 효과 추가 */
.tab-button:active {
  transform: translateY(1px);
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
}


.help-content {
  background-color: #fff;
  border-radius: 10px;
  min-height: 400px;
}

/* 반응형 디자인 */
@media (max-width: 768px) {
  .tab-container {
    flex-direction: column;
    padding: 10px;
  }

  .tab-button {
    width: 100%;
    text-align: center;
    padding: 10px 20px;
  }

  .help-title {
    font-size: 20px;
  }
}
</style>