<template>
  <nav class="navbar navbar-expand-lg bg-body-light" style="white-space:nowrap">
<div class="container-fluid">
  <!-- <a class="navbar-brand" href="#">Navbar</a> -->
   <!-- 홈 -->
  <RouterLink :to="{name:'HomeView'}" class="navbar-brand" aria-current="page">
    <img src="/images/logo.png" style="width: 200px;" alt="logo">
  </RouterLink>
  <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
    <span class="navbar-toggler-icon"></span>
  </button>
  <!-- 카테고리 -->
  <div class="collapse navbar-collapse" id="navbarSupportedContent">
    <ul class="navbar-nav me-auto mb-2 mb-lg-0">
      <li class="nav-item dropdown">
        <a class="nav-link dropdown-toggle fw-bold" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">
          금융서비스
        </a>
        <ul class="dropdown-menu">
          <!-- <li><RouterLink :to="{name:'TransferView'}" class="dropdown-item">가계부</RouterLink> </li> -->
          <li><RouterLink :to="{name:'TransferView'}" class="dropdown-item">계좌이체</RouterLink></li>
          <li><RouterLink :to="{name:'TransferHistoryView'}" class="dropdown-item">이체내역</RouterLink></li>
          <li><RouterLink :to="{name:'ExchangeView'}" class="dropdown-item">환율조회</RouterLink></li>
        </ul>
      </li>
      <li class="nav-item">
        <!-- <a class="nav-link active" aria-current="page" href="#">Home</a> -->
        <RouterLink :to="{name:'ProductView'}" class="nav-link">상품</RouterLink>
      </li>
      <li class="nav-item">
        <!-- <a class="nav-link active" aria-current="page" href="#">Home</a> -->
        <RouterLink :to="{name:'KakaoMapView'}" class="nav-link">지점찾기</RouterLink>
      </li>
      <li class="nav-item">
        <RouterLink :to="{name:'AssetTypeView'}" class="nav-link" >Ai 분석</RouterLink>
      </li>
      <li class="nav-item">
        <RouterLink :to="{name:'HelpView'}" class="nav-link">고객센터</RouterLink>
      </li>
    </ul>
   <!-- 검색 -->
    <!-- <form class="d-flex" role="search" style="width:400px;">
      <input class="form-control me-2" type="search" placeholder="Search" aria-label="Search" style="width:70%;">
      <button class="btn btn-outline-primary" type="submit">
        <img src="../../../public/images/search.png" width="35px" alt="">
      </button>
    </form> -->
   <!-- 회원가입/ 로그인 -->
   <ul class="navbar-nav mb-2 mb-lg-0 ms-5">
      <li v-if="store.isLogin" class="nav-item auth-container">
        <RouterLink :to="{name:'ProfileView'}" class="nav-link profile-link">
          <img src="../../../public/images/profile.png" width="40px" alt="profile"> 
          {{ store.memberName }} 고객님
        </RouterLink>
        <button class="logout-btn" @click="store.logout">
          <img src="../../../public/images/logout.png" width="30px" alt="logout"/>
        </button>
      </li>
      <li v-if="!store.isLogin" class="nav-item auth-container">
        <RouterLink :to="{name:'LoginView'}" class="nav-link">로그인</RouterLink>
        <button class="logout-btn invisible">
          <img src="../../../public/images/logout.png" width="30px" alt="logout"/>
        </button>
      </li>
    </ul>
  </div>
</div>
</nav>
</template>

<script setup>
import { RouterLink, RouterView } from 'vue-router';
import { useMemberStore } from '../../stores/modules/member';
import { onMounted, ref } from 'vue';
// import { onMounted } from 'vue';

const store = useMemberStore()


// store.login()

onMounted(()=>{
store.getUserInfo()
store.profile()
})

// console.log(store)



</script>

<style scoped>

.auth-container {
  display: flex;
  align-items: center;
}

.profile-link {
  display: flex;
  align-items: center;
  gap: 8px;
}

.logout-btn {
  border: none;
  background: none;
  padding: 0;
  cursor: pointer;
  display: flex;
  align-items: center;
}

.invisible {
  visibility: hidden;
}


</style>
