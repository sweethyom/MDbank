<template>
    <div class="border border-light-subtle rounded p-4 text-center">
        <img src="../../public/images/logo.png" width="200" class="mb-3">    
        <div class="d-flex justify-content-center">
                
            <form @submit.prevent="logIn">
                <div class="input-group flex-nowrap mb-3 justify-content-center" style="width: 300px;">
                    <span class="input-group-text" id="addon-wrapping">
                        <img src="../../public/images/signup.png" width="40px" alt="login id">
                    </span>
                    <input type="text" id="username" class="form-control form-control-sm" placeholder="아이디를 입력하세요" aria-label="Memberid" aria-describedby="addon-wrapping" v-model="username">
                </div>
                <div class="input-group flex-nowrap mb-3" style="width: 300px;">
                    <span class="input-group-text" id="addon-wrapping">
                        <img src="../../public/images/password.png" width="40px" alt="login pswd">
                    </span>
                    <input type="password" id="password" class="form-control form-control-sm" placeholder="비밀번호를 입력하세요" aria-label="password" aria-describedby="addon-wrapping" v-model="password"><br>
                </div>
                <input type="submit" value="로그인" id="login-button" class="btn btn-primary text-light fw-bold mt-1">
            </form>
        </div>
            <div class="d-flex justify-content-center mt-3">
                <RouterLink :to="{name:'SignUpView'}" class="btn-link" style="font-size: 14px;">NH for teens 가입하기</RouterLink>
            </div>

    </div>
</template>

<script setup>
import { useMemberStore } from '@/stores/modules/member';
import { ref } from 'vue';
const store = useMemberStore()

const username= ref(null)
const password= ref(null)

const logIn = function(){

    const payload = {
        username: username.value,
        password: password.value
    } 
    store.logIn(payload)
}

</script>

<style scoped>

.btn-primary, .btn-primary:hover, .btn-primary:active, .btn-primary:visited {
    background-color: #196DDC;
}
</style>