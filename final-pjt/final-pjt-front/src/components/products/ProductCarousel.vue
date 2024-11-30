<template>
  <div class="carousel-container">
    <div class="carousel-wrapper">
      <div id="carouselExample" 
           class="carousel slide" 
           data-bs-ride="carousel" 
           data-bs-interval="3000">
        <div class="carousel-inner">
          <div class="carousel-item active">
            <div class="carousel-image-wrapper">
              <RouterLink :to="{ name: 'ProductDetailView', params: { id: 26 }}">
                <img src="/images/banner1.png" alt="banner1">
              </RouterLink>
            </div>
          </div>
          <div class="carousel-item">
            <div class="carousel-image-wrapper">
              <RouterLink :to="{ name: 'ProductDetailView', params: { id: 27 }}">
                <img src="/images/banner2.png" alt="banner2">
              </RouterLink>
            </div>
          </div>
          <div class="carousel-item">
            <div class="carousel-image-wrapper">
              <img src="/images/banner3.png" alt="banner3">
            </div>
          </div>
        </div>

        <!-- 이전/다음 버튼 -->
        <button class="carousel-control-prev" type="button" data-bs-target="#carouselExample" data-bs-slide="prev">
          <span class="carousel-control-prev-icon" aria-hidden="true"></span>
          <span class="visually-hidden">Previous</span>
        </button>
        <button class="carousel-control-next" type="button" data-bs-target="#carouselExample" data-bs-slide="next">
          <span class="carousel-control-next-icon" aria-hidden="true"></span>
          <span class="visually-hidden">Next</span>
        </button>

        <!-- 인디케이터 -->
        <div class="carousel-indicators">
          <button type="button" data-bs-target="#carouselExample" data-bs-slide-to="0" class="active" aria-current="true"></button>
          <button type="button" data-bs-target="#carouselExample" data-bs-slide-to="1"></button>
          <button type="button" data-bs-target="#carouselExample" data-bs-slide-to="2"></button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.carousel-container {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.carousel-wrapper {
  border-radius: 15px;
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  background: white;
}

:deep(.carousel) {
  position: relative;
  width: 100%;
}

:deep(.carousel-inner) {
  position: relative;
  width: 100%;
  overflow: hidden;
}

:deep(.carousel-item) {
  position: relative;
  display: none;
  float: left;
  width: 100%;
  margin-right: -100%;
  backface-visibility: hidden;
  transition: transform 0.6s ease-in-out;
}

:deep(.carousel-image-wrapper) {
  position: relative;
  width: 100%;
  /* 16:9 비율 유지 */
  padding-top: 40%;  /* 이 값을 조절하여 원하는 비율 설정 */
  overflow: hidden;
}

:deep(.carousel-image-wrapper img) {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;  /* 이미지가 영역을 꽉 채우도록 설정 */
}
:deep(.carousel-item.active),
:deep(.carousel-item-next),
:deep(.carousel-item-prev) {
  display: block;
}
:deep(.carousel-item-prev:not(.carousel-item-end)),
:deep(.active.carousel-item-start) {
  transform: translateX(-100%);
}

:deep(.carousel-item-next.carousel-item-start),
:deep(.carousel-item-prev.carousel-item-end) {
  transform: translateX(0);
}

/* 기존 스타일 유지하고 아래 스타일 추가 */

/* 슬라이드 효과 완성 */
:deep(.carousel-item-next:not(.carousel-item-start)),
:deep(.active.carousel-item-end) {
  transform: translateX(100%);
}

/* 컨트롤 버튼 스타일 */
:deep(.carousel-control-prev),
:deep(.carousel-control-next) {
  width: 50px;
  height: 50px;
  background-color: rgba(0, 0, 0, 0.3);
  border-radius: 50%;
  top: 50%;
  transform: translateY(-50%);
  opacity: 0;
  transition: all 0.3s ease;
}

:deep(.carousel-control-prev) {
  left: 20px;
}

:deep(.carousel-control-next) {
  right: 20px;
}

/* 호버 효과 */
.carousel-wrapper:hover {
  :deep(.carousel-control-prev),
  :deep(.carousel-control-next) {
    opacity: 1;
  }
}

/* 인디케이터 스타일 */
:deep(.carousel-indicators) {
  bottom: 20px;
}

:deep(.carousel-indicators button) {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  margin: 0 5px;
  background-color: rgba(255, 255, 255, 0.5);
  border: none;
  transition: all 0.3s ease;
}

:deep(.carousel-indicators button.active) {
  background-color: #fff;
  transform: scale(1.2);
}

/* 반응형 디자인 */
@media (max-width: 768px) {
  .carousel-container {
    padding: 10px;
  }

  :deep(.carousel-control-prev),
  :deep(.carousel-control-next) {
    width: 40px;
    height: 40px;
  }

  :deep(.carousel-indicators) {
    bottom: 10px;
  }
}
</style>
<script setup>

</script>

