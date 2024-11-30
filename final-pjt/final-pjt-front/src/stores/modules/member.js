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
  const signup=function(payload){
    // 변수명은 백엔드랑 동일해야함!!!
    // const last_name=payload.lastName
    const first_name=payload.firstName
    const username=payload.username  // 아이디
    const password1=payload.password1
    const password2=payload.password2
    const email=payload.email
    const address=payload.address
    const address_detail=payload.addressDetail
    const tel=payload.tel
    const old_account=payload.oldAccount
    const birth=payload.birth
  
    axios({
      method:'post',
      url:`${API_URL}/accounts/signup/`,
      data:{
        // last_name, 
        first_name, username, password1, password2, 
        email, address, address_detail, tel, old_account,birth
      }
    })
    .then(res=>{
      console.log('회원가입 성공')
      const password=password1
      logIn({ username, password })
      router.push({name:'HomeView'})
    })
    .catch(err=>{
      console.log(err)
      if(err.response &&  err.response.data) {
        const errorData = err.response.data
        if(errorData.username){
          alert('이미 존재하는 아이디입니다.')
          // alert(`${errorData.username}`)
        }
        if(errorData.old_account){
          alert(`${errorData.old_account}`)
      }
    }
    })
  }
  // 로그인
  const logIn = function(payload){
    
    const username =payload.username
    const password =payload.password

    axios({
      method: 'post',
      url:`${API_URL}/accounts/login/`,
      data:{
        username, password
      }
    })
    .then((res)=>{
      token.value = res.data.key
      localStorage.setItem('authToken', token.value)
      console.log('로그인 성공')
      console.log(res.data)
      getUserInfo()
      router.push({name:'HomeView'})
    })
    .catch((err)=>{
      console.log(err)
      alert('아이디와 비밀번호를 다시 확인해주세요.')
    })
  }
  // 프로필
  const profileData=ref(null)
  const profile= function(){

    if(!token.value){
      console.error('인증되지 않은 요청입니다.')
      return
    }
    axios({
      method: 'get',
      url:`${API_URL}/accounts/profile/`,
      headers:{
        Authorization: `Token ${token.value}`
      }
    })
    .then((res)=>{
      // console.log(res.data)
      profileData.value=res.data
      console.log(profileData.value)
    })
    .catch((err)=>{
      console.log('error is', err)
    })
  }
  // 회원탈퇴
  const signOut = function(){
    axios({
      method:'post',
      url:`${API_URL}/accounts/signout/`,
      headers:{
        Authorization:`Token ${token.value}`
      }
    })
    .then((res)=>{
      console.log('회원탈퇴 됐습니다')
      logout() // 회원탈퇴 후 로그아웃 처리
      router.push({name:'LoginView'}) //로그인페이지로 리디렉션
    })
    .catch((err)=>{
      console.log(err)
    })
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
  const addFavorite = function(newFavorite){
    axios({
      method:'post',
      url:`${API_URL}/banks/favorites/create/`,
      headers:{
        Authorization: `Token ${token.value}`
      },
      data:newFavorite
    })
    .then((res)=>{
      console.log('즐겨찾기 추가 성공', res.data)
    })
    .catch((err)=>{
      console.log(err)
    })
  }

  // 즐겨 찾기 수정
  const updateFavorite = function(favoriteId, updateFavorite){
    axios({
      method:'put',
      url:`${API_URL}/banks/favorites/update/${favoriteId}/`,
      headers:{
        Authorization: `Token ${token.value}`
      },
      data:updateFavorite
    })
    .then((res)=>{
      console.log('즐겨찾기 수정 성공', res.data)
    })
    .catch((err)=>{
      console.log(err)
    })
  }

  // 즐겨 찾기 삭제
  const deleteFavorite = function(favoriteId){
    axios({
      method:'delete',
      url:`${API_URL}/banks/favorites/delete/${favoriteId}/`,
      headers:{
        Authorization: `Token ${token.value}`
      }
    })
    .then((res)=>{
      console.log('즐겨찾기 삭제 성공', res.data)
    })
    .catch((err)=>{
      console.log(err)
    })
  }

  // const isLoading = ref(false)
  // // 회원 정보 수정
  // const updateProfile = async (payload) => {
  //   isLoading.value = true;  // 로딩 상태를 true로 설정
  
  //   try {
  //     // axios를 통한 PUT 요청, payload는 요청의 데이터로 사용
  //     const response = await axios.put(`${API_URL}/accounts/updateprofile/`, payload);
  
  //     // 응답을 받으면 로그를 출력
  //     console.log('회원 정보 수정 성공', response.data);
  //   } catch (err) {
  //     // 오류 처리
  //     console.error('회원 정보 수정 실패:', err.response ? err.response.data : err);
  //     alert('회원 정보 수정에 실패했습니다. 다시 시도해 주세요.');
  //   } finally {
  //     // 로딩 상태 종료
  //     isLoading.value = false;
  //   }
  // };
  
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
