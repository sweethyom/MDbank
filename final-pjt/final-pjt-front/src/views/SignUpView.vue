<template>
    <div>
        <div class="border border-light-subtle rounded p-4 text-center mt-5">
            <img src="../../public/images/logo.png" class="my-5" width="200"> 
            <form @submit.prevent="signup" class="text-start">
                <div style="width: 700px;" class="mx-auto">
                    <div class="input-group mb-3">
                        <span class="input-group-text" id="basic-addon1">
                            <img src="../../public/images/signup.png" width="20px" alt="signup">
                        </span>
                        <input type="text" class="form-control" placeholder="아이디" id="username" aria-label="Username" aria-describedby="basic-addon1" v-model="username">
                    </div>
                    <div class="input-group mb-3">
                        <span class="input-group-text" id="basic-addon1">
                            <img src="../../public/images/password.png" width="20px" alt="signup">
                        </span>
                        <input type="password" class="form-control" placeholder="비밀번호" id="password1" aria-label="Password1" aria-describedby="basic-addon1" v-model="password1">
                    </div>
                    <div class="input-group mb-3">
                        <span class="input-group-text" id="basic-addon1">
                            <img src="../../public/images/password.png" width="20px" alt="signup">
                        </span>
                        <input type="password" class="form-control" placeholder="비밀번호확인" id="password2" aria-label="Password2" aria-describedby="basic-addon1" v-model="password2">
                    </div>
                    <div class="input-group mb-3">
                        <span class="input-group-text" id="basic-addon1">
                            <img src="../../public/images/signup.png" width="20px" alt="signup">
                        </span>
                        <input type="text" class="form-control" placeholder="이름" id="first-name" aria-label="Firstname" aria-describedby="basic-addon1" v-model="firstName">
                    </div>
                    <div class="input-group mb-3">
                        <span class="input-group-text" id="basic-addon1">
                            <img src="../../public/images/signup.png" width="20px" alt="signup">
                        </span>
                        <input type="text" class="form-control" placeholder="생년월일" id="birth" aria-label="birth" aria-describedby="basic-addon1" v-model="birth">
                    </div>
                    <div class="input-group mb-3">
                        <span class="input-group-text" id="basic-addon1" style="width: 45px;">@</span>
                        <input type="email" class="form-control" placeholder="이메일" id="email" aria-label="Email" aria-describedby="basic-addon1" v-model="email">
                    </div>
                    <div class="input-group mb-3">
                        <span class="input-group-text" id="basic-addon1" style="width: 45px;">
                            <img src="../../public/images/address.png" width="20px" alt="signup">
                        </span>
                        <input type="text" class="form-control" placeholder="주소" id="address" aria-label="Address" aria-describedby="basic-addon1" v-model="address">
                    </div>
                    <div class="input-group mb-3">
                        <span class="input-group-text" id="basic-addon1" style="width: 45px;">
                            <img src="../../public/images/addressdetail.png" width="20px" alt="signup">
                        </span>
                        <input type="text" class="form-control" placeholder="상세주소" id="address-detail" aria-label="Addressdetail" aria-describedby="basic-addon1" v-model="addressDetail">
                    </div>
                    <div class="input-group mb-3">
                        <span class="input-group-text" id="basic-addon1" style="width: 45px;">
                            <img src="../../public/images/tel.png" width="20px" alt="signup">
                        </span>
                        <input type="tel" class="form-control" placeholder="연락처" id="tel" aria-label="Tel" aria-describedby="basic-addon1" v-model="tel">
                    </div>
                    <div class="input-group mb-3">
                        <span class="input-group-text" id="basic-addon1" style="width: 45px;">
                            <img src="../../public/images/account.png" width="20px" alt="signup">
                        </span>
                        <input type="text" class="form-control" placeholder="기존계좌" id="old-account" aria-label="ㅒldaccount" aria-describedby="basic-addon1" v-model="oldAccount">
                    </div>
                    <div class="text-center">
                        <input type="submit" class="btn btn-primary fw-bold" value="회원가입">
                    </div>
                </div>
            </form>
        </div>
    </div>
</template>

<script setup>
import { useMemberStore } from '@/stores/modules/member';
import { ref } from 'vue'
import { useRouter } from 'vue-router'
const router = useRouter()

const store = useMemberStore()

// const lastName = ref(null)   //성
const firstName = ref(null)  //이름
const username = ref(null)   //아이디
const password1 = ref(null)
const password2 = ref(null)
const email = ref(null)
const address = ref(null)
const addressDetail = ref(null)
const tel = ref(null)
const oldAccount = ref(null)
const birth = ref(null)

const signup = async function() {
    try {
        const payload = {
            firstName: firstName.value,
            username: username.value,
            password1: password1.value,
            password2: password2.value,
            email: email.value,
            address: address.value,
            addressDetail: addressDetail.value,
            tel: tel.value,
            oldAccount: oldAccount.value,
            birth: birth.value,
        }
        
        await store.signup(payload)
        await store.logIn({ username: username.value, password: password1.value })
        await store.profile()
        await store.getUserInfo()
        router.push({ name: 'HomeView' })
    } catch (error) {
        console.error('회원가입 중 오류 발생:', error)
        // 필요한 경우 사용자에게 에러 메시지 표시
    }
}


</script>

<style scoped>
.btn-primary, .btn-primary:hover, .btn-primary:active, .btn-primary:visited {
    background-color: #196DDC;
}
</style>
