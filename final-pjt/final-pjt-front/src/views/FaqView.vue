<template>
    <div class="faq-container">
      <!-- FAQ 아코디언 리스트 -->
      <div class="faq-list">
        <div v-for="(faq, index) in 3" :key="index" class="faq-item">
          <div class="faq-question">
            <span class="q-mark">Q</span>
            <span class="question-text">자산분석 자산관리 유형이 무엇인가요?</span>
          </div>
          <div class="faq-answer">
            <span class="a-mark">A</span>
            <span class="answer-text">
              고객님의 자동, 자동 패턴을 파악하여 유형으로 나눈 것으로,
              유형과 더불어 자산관리 원칙과 그에 맞는 상품을 추천해드리고 있는 서비스 입니다.
            </span>
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
    </div>
  </template>
  
  <style scoped>
  .faq-container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
  }
  
  .faq-list {
    display: flex;
    flex-direction: column;
    gap: 20px;
  }
  
  .faq-item {
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    padding: 20px;
    background-color: white;
  }
  
  .faq-question {
    display: flex;
    align-items: flex-start;
    gap: 15px;
    margin-bottom: 15px;
  }
  
  .faq-answer {
    display: flex;
    align-items: flex-start;
    gap: 15px;
    padding-top: 15px;
    border-top: 1px solid #f0f0f0;
  }
  
  .q-mark, .a-mark {
    font-weight: bold;
    color: #3699f5;
    font-size: 18px;
    min-width: 20px;
  }
  
  .question-text {
    color: #333;
    font-weight: 500;
  }
  
  .answer-text {
    color: #666;
    line-height: 1.6;
  }
  
  .pagination {
    display: flex;
    justify-content: center;
    gap: 5px;
    margin-top: 30px;
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
  
  /* 반응형 디자인 */
  @media (max-width: 768px) {
    .faq-container {
      padding: 10px;
    }
  
    .faq-item {
      padding: 15px;
    }
  
    .faq-question, .faq-answer {
      gap: 10px;
    }
  
    .q-mark, .a-mark {
      font-size: 16px;
    }
  }
  
  /* 호버 효과 */
  .faq-item:hover {
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    transform: translateY(-2px);
    transition: all 0.3s ease;
  }
  
  .page-btn:hover {
    background-color: #f5f5f5;
    border-radius: 4px;
  }
  </style>