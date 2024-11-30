<template>
    <div>
        <div class="border border-light-subtle rounded p-4 text-center mt-5">
            <img src="../../public/images/logo.png" class="my-5" width="200"> 
            <form @submit.prevent="updateProfile" class="text-start">
                <div style="width: 700px;" class="mx-auto">
                    <!-- 아이디, 비밀번호, 이름 등 수정 불가 필드 -->
                    <div class="input-group mb-3">
                        <span class="input-group-text" id="basic-addon1">
                            <img src="../../public/images/signup.png" width="20px" alt="signup">
                        </span>
                        <input type="text" class="form-control" placeholder="아이디" id="username" v-model="user.username" disabled>
                    </div>
                    <div class="input-group mb-3">
                        <span class="input-group-text" id="basic-addon1">
                            <img src="../../public/images/password.png" width="20px" alt="signup">
                        </span>
                        <input type="password" class="form-control" placeholder="비밀번호" id="password1" v-model="password1" disabled>
                    </div>
                    <div class="input-group mb-3">
                        <span class="input-group-text" id="basic-addon1">
                            <img src="../../public/images/password.png" width="20px" alt="signup">
                        </span>
                        <input type="password" class="form-control" placeholder="비밀번호확인" id="password2" v-model="password2" disabled>
                    </div>
                    <div class="input-group mb-3">
                        <span class="input-group-text" id="basic-addon1">
                            <img src="../../public/images/signup.png" width="20px" alt="signup">
                        </span>
                        <input type="text" class="form-control" placeholder="이름" id="first-name" v-model="user.firstName" disabled>
                    </div>
                    <div class="input-group mb-3">
                        <span class="input-group-text" id="basic-addon1">
                            <img src="../../public/images/signup.png" width="20px" alt="signup">
                        </span>
                        <input type="text" class="form-control" placeholder="생년월일" id="birth" v-model="user.birth" disabled>
                    </div>

                    <!-- 수정 가능한 정보 -->
                    <div class="input-group mb-3">
                        <span class="input-group-text" id="basic-addon1" style="width: 45px;">@</span>
                        <input type="email" class="form-control" placeholder="이메일" id="email" v-model="email">
                    </div>
                    <div class="input-group mb-3">
                        <span class="input-group-text" id="basic-addon1" style="width: 45px;">
                            <img src="../../public/images/address.png" width="20px" alt="signup">
                        </span>
                        <input type="text" class="form-control" placeholder="주소" id="address" v-model="address">
                    </div>
                    <div class="input-group mb-3">
                        <span class="input-group-text" id="basic-addon1" style="width: 45px;">
                            <img src="../../public/images/addressdetail.png" width="20px" alt="signup">
                        </span>
                        <input type="text" class="form-control" placeholder="상세주소" id="address-detail" v-model="addressDetail">
                    </div>
                    <div class="input-group mb-3">
                        <span class="input-group-text" id="basic-addon1" style="width: 45px;">
                            <img src="../../public/images/tel.png" width="20px" alt="signup">
                        </span>
                        <input type="tel" class="form-control" placeholder="연락처" id="tel" v-model="tel">
                    </div>
                    <div class="input-group mb-3">
                        <span class="input-group-text" id="basic-addon1" style="width: 45px;">
                            <img src="../../public/images/account.png" width="20px" alt="signup">
                        </span>
                        <input type="text" class="form-control" placeholder="기존계좌" id="old-account" v-model="oldAccount" disabled>
                    </div>
                    <div class="text-center">
                        <input type="submit" class="btn btn-primary fw-bold" value="수정하기" :disabled="isLoading">
                    </div>
                </div>
            </form>
        </div>
    </div>
</template>

<script setup>
import { useMemberStore } from '@/stores/modules/member';
import axios from 'axios';
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const store = useMemberStore();

// 반응형 변수 선언
const token = ref(null); // ref로 감싸서 반응형으로 관리

const user = ref({
    username: '',
    firstName: '',
    birth: ''
});

const email = ref('');
const address = ref('');
const addressDetail = ref('');
const tel = ref('');
const isLoading = ref(false);
const API_URL = 'http://127.0.0.1:8000';

onMounted(async () => {
    // onMounted 안에서 token을 새로 가져오는 코드
    token.value = localStorage.getItem('authToken');  // token을 갱신

    console.log('토큰 확인:', token.value); // 콘솔에서 token 확인

    try {
        await store.getUserInfo();  // 사용자 정보를 비동기로 가져옴
        const userData = store.userData;  // store에서 사용자 정보를 가져옴
        if (userData) {
            user.value = { 
                username: userData.username,
                firstName: userData.firstName,
                birth: userData.birth 
            };
        }
    } catch (err) {
        console.error('사용자 정보 로딩 실패:', err);
        alert('사용자 정보를 불러오는 데 실패했습니다.');
    }
});

// 회원 정보 수정 함수
const updateProfile = async () => {
    console.log('찐토큰', token.value)
    // 토큰이 없으면 알림을 띄우고 함수를 종료
    if (!token) {
        alert('로그인이 필요합니다.');
        return;
    }

    const payload = {
        email: email.value,
        address: address.value,
        address_detail: addressDetail.value,
        tel: tel.value,
    };

    try {
        const response = await axios.put(`${API_URL}/accounts/updateprofile/`, payload, {
            headers: {
                'Authorization': `Token ${token.value}`,
                'Content-Type': 'application/json',
            }
        });
        console.log('회원 정보 수정 성공', response.data);
        await alert('회원 정보가 성공적으로 수정되었습니다.');
        await router.push('/profile');

    } catch (err) {
         // 더 자세한 에러 로깅
         console.error('에러 상세 정보:', {
            status: err.response?.status,
            data: err.response?.data,
            message: err.message
        });

        // 에러 상황별 다른 메시지 표시
        if (err.response) {
            if (err.response.status === 400) {
                // 유효성 검사 실패 등의 에러
                const errorMessage = Object.values(err.response.data).join('\n');
                alert(`회원 정보 수정 실패:\n${errorMessage}`);
            } else if (err.response.status === 401) {
                alert('로그인이 필요합니다.');
            } else {
                alert('회원 정보 수정에 실패했습니다. 다시 시도해 주세요.');
            }
        } else if (err.request) {
            // 요청은 보냈으나 응답을 받지 못한 경우
            alert('서버와의 통신에 실패했습니다. 네트워크 연결을 확인해주세요.');
        } else {
            // 요청 자체를 보내지 못한 경우
            alert('요청 처리 중 오류가 발생했습니다.');
        }
    }
};
</script>


<style scoped>
.btn-primary, .btn-primary:hover, .btn-primary:active, .btn-primary:visited {
    background-color: #196DDC;
}

.btn-primary:disabled {
    background-color: #9e9e9e; /* 로딩 중 비활성화된 버튼 색상 */
}
</style>
