import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import { useRouter } from 'vue-router'


export const useMemberStore = defineStore('member', () => {
  const userData = ref(null);

  const API_URL = 'http://127.0.0.1:8000'
  const token = ref(null)
  const router = useRouter()
  const isAdmin = ref(false)
  const username =ref(null)

  // 로그인된 계정인 경우 로그인, 회원가입 접근 제한
  const isLogin = computed(()=>{
    if(token.value === null){
      return false
    }else{
      return true
    }
  })

// 로그아웃 함수
const logout = () => {
  // 상태 초기화
  token.value = null
  memberName.value = null
  profileData.value = null  // profileData도 ref/reactive로 선언되어 있다면 .value 사용

  // 세션스토리지 클리어
  sessionStorage.removeItem('access_token')
  sessionStorage.removeItem('refresh_token')
  
  // 알림
  window.alert('로그아웃 되었습니다.')
  
  // 홈으로 이동 (router.push 사용)
  router.push({ name: 'HomeView' })
}
  
  // 회원가입
  const signup = async function(payload) {
    // 변수명은 백엔드랑 동일해야함!!!
    // const last_name=payload.lastName
    const {
      firstName: firstName,
      username,
      password1,
      password2,
      email,
      address,
      addressDetail: address_detail,
      tel,
      oldAccount: old_account,
      birth
    } = payload
  
    try {
      await axios({
        method: 'post',
        url: `${API_URL}/accounts/signup/`,
        data: {
          first_name:firstName,
          username,
          password1,
          password2,
          email,
          address,
          address_detail,
          tel,
          old_account,
          birth
        }
      })
  
      console.log('회원가입 성공')
      const password = password1
      
  
    } catch (err) {
      console.log(err)
      if (err.response?.data) {
        const errorData = err.response.data
        if (errorData.username) {
          alert('이미 존재하는 아이디입니다.')
        }
        if (errorData.old_account) {
          alert(errorData.old_account)
        }
      }
    }
  }
  // 로그인
  const logIn = async function(payload) {
    try {
        const username = payload.username
        const password = payload.password

        const res = await axios({
            method: 'post',
            url: `${API_URL}/accounts/login/`,
            data: {
                username, password
            }
        })

        token.value = res.data.key
        localStorage.setItem('authToken', token.value)
        console.log('로그인 성공')
        console.log(res.data)
        
        // 순차적으로 사용자 정보와 프로필 데이터를 가져옴
        
        return true // 로그인 성공 시 true 반환
        
    } catch (error) {
        console.error('로그인 실패:', error)
        throw error // 에러를 상위로 전파하여 컴포넌트에서 처리할 수 있도록 함
    }
  }


  // 프로필
  const profileData=ref(null)
  const profile = async function() {
    if (!token.value) {
      console.error('인증되지 않은 요청입니다.');
      return;
    }
    try {
      const res = await axios({
        method: 'get',
        url: `${API_URL}/accounts/profile/`,
        headers: {
          Authorization: `Token ${token.value}`
        }
      });
      profileData.value = res.data;  // 데이터 업데이트
      console.log('프로필 데이터', profileData.value) // 디버깅용 로그  
    } catch (err) {
      console.error(err);
    }
  };
  // 회원탈퇴
  const signOut = async function() {
    try {
      await axios({
        method: 'post',
        url: `${API_URL}/accounts/signout/`,
        headers: {
          Authorization: `Token ${token.value}`
        }
      })
      
      console.log('회원탈퇴 됐습니다')
      alert('회원탈퇴 됐습니다')
      await logout() // 회원탈퇴 후 로그아웃 처리
      router.push({ name: 'LoginView' }) //로그인페이지로 리디렉션
      
    } catch (err) {
      console.error('회원탈퇴 실패:', err)
      if (err.response) {
        // 서버에서 응답이 왔지만 에러인 경우
        alert(err.response.data.message || '회원탈퇴에 실패했습니다.')
      } else if (err.request) {
        // 요청은 보냈지만 응답을 받지 못한 경우
        alert('서버와의 통신에 실패했습니다. 잠시 후 다시 시도해주세요.')
      } else {
        // 요청 자체를 보내지 못한 경우
        alert('회원탈퇴 처리 중 오류가 발생했습니다.')
      }
    }
  }
    //자산관리유형검사
    const myType=ref(null)
    const assetType=function(){
      axios({
          method:'get',
          url:`${API_URL}/products/asset_type/`,
          headers:{
              Authorization: `Token ${token.value}`
          }
      })
      .then((res)=>{
        console.log(res.data )
        myType.value=res.data.analysis
      })
      .catch((err)=>{
        console.log(err)
      })
  }

  // 금융상품 추천
  const recommendData=ref(null)
  
  const recommend=function(){
    
    if (!myType.value) {
      alert('먼저 자산관리 유형 검사를 진행해주세요.')
      return
    }
    axios({
      method:'post',
      url:`${API_URL}/products/recommend/`,
      headers:{
        Authorization: `Token ${token.value}`
      },
      data:{
        assetType:myType.value
      }
    })
    .then((res)=>{
      console.log(res.data)
      recommendData.value=res.data
    })
    .catch((err)=>{
      console.log(err)
    })
  }

  // 사용자 정보 가져오기 (관리자 여부 확인)
  const checkAdmin = () => {
    if (!token.value) return

    axios({
      method: 'get',
      url: `${API_URL}/accounts/profile/`,
      headers: {
        Authorization: `Token ${token.value}`
      }
    })
    .then((res) => {
      console.log('Profile response:', res.data)  // 전체 응답 데이터 확인
      const memberData = res.data.member  // member 객체에서 데이터 추출
      username.value = memberData.username
      isAdmin.value = memberData.is_superuser || memberData.is_staff
      console.log('관리자 여부:', isAdmin.value)
      console.log('is_superuser:', memberData.is_superuser)
      console.log('is_staff:', memberData.is_staff)
    })
    .catch((err) => {
      console.log('사용자 정보 가져오기 실패:', err)
    })
  }
  
  const memberName = ref('')
  // 유저 정보 가져오기 (프로필 또는 로그인된 유저 정보)
  const getUserInfo = function() {
    if (!token.value) {
      console.error('인증되지 않은 요청입니다.')
      return
    }
    axios({
      method: 'get',
      url: `${API_URL}/accounts/user_info/`, // 서버에서 유저 정보를 반환하는 엔드포인트
      headers: {
        Authorization: `Token ${token.value}`
      }
    })
    .then(response => {
      userData.value = response.data.userId.member;
      memberName.value = response.data.userId.member.first_name // 유저 정보 저장
      console.log('response:', response.data.userId.member.first_name)
    })
    .catch(err => {
      console.error('유저 정보 가져오기 실패:', err)
    })
  }


  // 즐겨찾기 목록 조회
  const favorites=ref(null)
  const getFavorites=function(){
    axios({
      method:'get',
      url: `${API_URL}/banks/favorites/`,
      headers:{
        Authorization: `Token ${token.value}`
      }
    })
    .then((res)=>{
      favorites.value=res.data
      console.log('즐겨찾기 목록', favorites.value)
    })
    .catch((err)=>{
      console.log(err)
    })
  }
// 즐겨찾기 추가
const addFavorite = async function(newFavorite) {
  try {
    const res = await axios({
      method: 'post',
      url: `${API_URL}/banks/favorites/create/`,
      headers: {
        Authorization: `Token ${token.value}`
      },
      data: newFavorite
    });
    console.log('즐겨찾기 추가 성공', res.data);
  } catch (err) {
    console.log(err);
  }
}

// 즐겨 찾기 수정
const updateFavorite = async function(favoriteId, updateFavorite) {
  try {
    const res = await axios({
      method: 'put',
      url: `${API_URL}/banks/favorites/update/${favoriteId}/`,
      headers: {
        Authorization: `Token ${token.value}`
      },
      data: updateFavorite
    });
    console.log('즐겨찾기 수정 성공', res.data);
  } catch (err) {
    console.log(err);
  }
}

// 즐겨 찾기 삭제
const deleteFavorite = async function(favoriteId) {
  try {
    const res = await axios({
      method: 'delete',
      url: `${API_URL}/banks/favorites/delete/${favoriteId}/`,
      headers: {
        Authorization: `Token ${token.value}`
      }
    });
    console.log('즐겨찾기 삭제 성공', res.data);
  } catch (err) {
    console.log(err);
  }
}



// const isLoading = ref(false)
// // 회원 정보 수정
// const updateProfile = async (payload) => {
//   isLoading.value = true;  // 로딩 상태를 true로 설정

//   try {
//     const response = await axios({
//       method: 'put',
//       url: `${API_URL}/accounts/updateprofile/`,
//       headers: {
//         Authorization: `Token ${token.value}`,
//         // 'Content-Type': 'application/json'
//       },
//       data: payload
//     });

//     // 응답을 받으면 로그를 출력
//     console.log('회원 정보 수정 성공', response.data);
//     return response.data;  // 성공 시 데이터 반환
//   } catch (err) {
//     // 오류 처리
//     console.error('회원 정보 수정 실패:', err.response ? err.response.data : err);
//     throw err;  // 에러를 상위로 전파하여 컴포넌트에서 처리할 수 있도록 함
//   } finally {
//     // 로딩 상태 종료
//     isLoading.value = false;
//   }
// }
  
    // 은행선택 목록 조회
    const banks = ref([]); // 은행 목록을 저장
  
    const getBanks = function () {
      axios({
        method: 'get',
        url: `${API_URL}/banks/getbanks/`,
        headers:{
          Authorization: `Token ${token.value}`
        }
      })
        .then((res) => {
          banks.value = res.data; // 은행 목록 저장
          console.log('은행 목록:', banks.value);
        })
        .catch((err) => {
          console.error('은행 목록 조회 실패:', err); // 디버깅용 에러 로그
          alert('은행 목록을 불러올 수 없습니다. 다시 시도해주세요.'); // 사용자 알림
        });
    };

  return { signup, API_URL, logIn, token, isLogin, logout, profileData, profile, 
          signOut, assetType, myType, isAdmin, getUserInfo, recommend, recommendData,
          favorites, getFavorites, addFavorite, updateFavorite, deleteFavorite, memberName,checkAdmin, userData, getBanks, banks}
}, {
  persist: {
    paths: ['token', 'isAdmin', 'username'],
    storage: localStorage
  }
})
