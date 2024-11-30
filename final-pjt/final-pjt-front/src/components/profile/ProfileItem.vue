<template>
  <div class="profile-container" v-if="profileData.member">
    <!-- 프로필 헤더 -->
    <div class="profile-header">
      <div class="profile-image-wrapper">
        <img src="../../../public/images/profile.png" alt="profile" class="profile-image">
      </div>
      <div class="profile-name">
        <h2 class="user-name">{{ profileData.member.first_name }}<span>고객님</span></h2>
      </div>
      <div class="profile-actions">
        <RouterLink :to="{name:'ProfileChangeView'}" class="edit-button">
          <i class="fas fa-edit me-2"></i>프로필 수정
        </RouterLink>
      </div>
    </div>

    <!-- 프로필 정보 -->
    <div class="profile-content">
      <table class="profile-table">
        <tbody>
          <!-- 기본 정보 섹션 -->
          <tr>
            <th>아이디</th>
            <td>{{ profileData.member.username }}</td>
          </tr>
          <tr>
            <th>비밀번호</th>
            <td class="password-field">
              <span>********</span>
              <button class="action-button">
                <i class="fas fa-key me-2"></i>비밀번호 변경
              </button>
            </td>
          </tr>
          <tr>
            <th>연락처</th>
            <td>{{ profileData.member.tel }}</td>
          </tr>
          <tr>
            <th>이메일</th>
            <td>{{ profileData.member.email }}</td>
          </tr>
          <tr>
            <th>주소</th>
            <td>{{ profileData.member.address }}</td>
          </tr>
          <tr>
            <th>상세주소</th>
            <td>{{ profileData.member.address_detail }}</td>
          </tr>

          <!-- 계좌 정보 섹션 -->
          <tr class="section-divider">
            <th>보유계좌</th>
            <td class="accounts-list">
              <ProfileItemAccountList 
                v-for="bankAccounts in profileData.bank_accounts"
                :key="bankAccounts.id"
                :bank-accounts="bankAccounts"
              />
            </td>
          </tr>

          <!-- 즐겨찾기 섹션 -->
          <tr class="section-divider">
            <th>즐겨찾기</th>
            <td class="favorites-section">
              <div class="favorites-list">
                <ProfileItemFavoriteList
                  v-for="favorites in profileData.favorites"
                  :key="favorites.id"
                  :favorites="favorites"
                  :profileData="profileData"
                  @refresh="$emit('refresh')"
                />
              </div>
              <button class="add-favorite-button" @click="toggleModal">
                <i class="fas fa-plus me-2"></i>즐겨찾기 추가
              </button>
            </td>
          </tr>
        </tbody>
      </table>

      <!-- 회원탈퇴 버튼 -->
      <div class="signout-section">
        <button class="signout-button" @click="signOut">
          <i class="fas fa-user-times me-2"></i>회원탈퇴
        </button>
      </div>
    </div>

    <!-- 즐겨찾기 추가 모달 -->
    <div v-if="showModal" class="modal" @click.self="toggleModal">
      <div class="modal-content">
        <h3 class="modal-title">
          <i class="fas fa-star me-2"></i>즐겨찾기 추가
        </h3>
        <form @submit.prevent="addFavorite">
          <div class="form-group">
            <label for="division">별명</label>
            <input type="text" id="division" v-model="newFavorite.division" placeholder="별명을 입력하세요">
          </div>

          <div class="form-group">
            <label for="bank">은행</label>
            <select id="bank" v-model="newFavorite.bank" class="form-select">
              <option value="" disabled selected>은행을 선택하세요</option>
              <option v-for="bank in profileData.banks" :key="bank.id" :value="bank.id">
                {{ bank.name }}
              </option>
            </select>
          </div>

          <div class="form-group">
            <label for="recipient">계좌번호</label>
            <input type="text" id="recipient" v-model="newFavorite.recipient" placeholder="계좌번호를 입력하세요">
          </div>

          <div class="form-group">
            <label for="recipient-name">받는 분 이름</label>
            <input type="text" id="recipient-name" v-model="newFavorite.recipient_name" placeholder="받는 분 이름을 입력하세요">
          </div>

          <div class="modal-actions">
            <button type="submit" class="submit-button">
              <i class="fas fa-check me-2"></i>추가
            </button>
            <button type="button" @click="toggleModal" class="cancel-button">
              <i class="fas fa-times me-2"></i>취소
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>

  <!-- 로딩 상태 -->
  <div v-else class="loading-state">
    <i class="fas fa-spinner fa-spin me-2"></i>
    데이터를 불러오는 중입니다...
  </div>
</template>

<style scoped>
.profile-container {
  max-width: 1000px;
  margin: 2rem auto;
  padding: 2rem;
  background: white;
  border-radius: 15px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.profile-header {
  text-align: center;
  margin-bottom: 3rem;
  position: relative;
}

.profile-image-wrapper {
  width: 150px;
  height: 150px;
  margin: 0 auto 1.5rem;
  border-radius: 50%;
  overflow: hidden;
  border: 3px solid #196DDC;
  padding: 3px;
}

.profile-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 50%;
}

.profile-name {
  margin-bottom: 1rem;
}

.user-name {
  font-size: 2rem;
  color: #196DDC;
  font-weight: 700;
}

.user-name span {
  font-size: 1.2rem;
  color: #666;
  margin-left: 0.5rem;
}

.profile-actions {
  position: absolute;
  top: 0;
  right: 0;
}

.edit-button {
  padding: 0.8rem 1.5rem;
  background: #196DDC;
  color: white;
  border-radius: 10px;
  text-decoration: none;
  transition: all 0.3s ease;
}

.edit-button:hover {
  background: #1557B0;
  transform: translateY(-2px);
}

.profile-table {
  width: 100%;
  margin-bottom: 2rem;
}

.profile-table th {
  width: 200px;
  padding: 1.5rem 2rem;
  text-align: right;
  color: #666;
  font-weight: 600;
  vertical-align: top;
}

.profile-table td {
  padding: 1.5rem 2rem;
  color: #333;
}

.password-field {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.action-button {
  padding: 0.5rem 1rem;
  background: #196DDC;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.action-button:hover {
  background: #1557B0;
  transform: translateY(-2px);
}

.section-divider {
  border-top: 1px solid #eee;
}

.favorites-section {
  position: relative;
}

.add-favorite-button {
  margin-top: 1rem;
  padding: 0.5rem 1rem;
  background: #196DDC;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.add-favorite-button:hover {
  background: #1557B0;
  transform: translateY(-2px);
}

.signout-section {
  text-align: center;
  margin-top: 3rem;
}

.signout-button {
  padding: 0.8rem 2rem;
  background: #dc3545;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.signout-button:hover {
  background: #c82333;
  transform: translateY(-2px);
}

/* 모달 스타일링 */
.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  padding: 2rem;
  border-radius: 15px;
  width: 90%;
  max-width: 500px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
}

.modal-title {
  font-size: 1.5rem;
  color: #196DDC;
  margin-bottom: 1.5rem;
  font-weight: 700;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  color: #666;
  font-weight: 600;
}

.form-group input,
.form-group select {
  width: 100%;
  padding: 0.8rem;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  font-size: 1rem;
  transition: all 0.3s ease;
}

.form-group input:focus,
.form-group select:focus {
  border-color: #196DDC;
  box-shadow: 0 0 0 3px rgba(25, 109, 220, 0.1);
  outline: none;
}

.modal-actions {
  display: flex;
  gap: 1rem;
  margin-top: 2rem;
}

.submit-button,
.cancel-button {
  flex: 1;
  padding: 0.8rem;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.submit-button {
  background: #196DDC;
  color: white;
}

.submit-button:hover {
  background: #1557B0;
  transform: translateY(-2px);
}

.cancel-button {
  background: #6c757d;
  color: white;
}

.cancel-button:hover {
  background: #5a6268;
  transform: translateY(-2px);
}

.loading-state {
  text-align: center;
  padding: 3rem;
  color: #666;
  font-size: 1.2rem;
}

/* 반응형 디자인 */
@media (max-width: 768px) {
  .profile-container {
    padding: 1rem;
    margin: 1rem;
  }

  .profile-table th {
    width: 120px;
    padding: 1rem;
  }

  .profile-table td {
    padding: 1rem;
  }

  .password-field {
    flex-direction: column;
    gap: 1rem;
  }

  .action-button {
    width: 100%;
  }
}
</style>

<script setup>
import { ref, defineEmits } from 'vue';
import { useMemberStore } from '@/stores/modules/member';
import ProfileItemAccountList from './ProfileItemAccountList.vue';
import ProfileItemFavoriteList from './ProfileItemFavoriteList.vue';
import { RouterLink } from 'vue-router';
import ProfileChangeView from '@/views/ProfileChangeView.vue';
defineProps({
  profileData: Object
})

const store = useMemberStore()
const showModal = ref(false)
const emit = defineEmits(['refresh'])

const newFavorite = ref({
  division:'',
  bank:'',
  recipient:'',
  recipient_name:''
})

const toggleModal = function(){
  // 현재 모달 값과 반대의 모달 값을 넣겠다
  showModal.value = !showModal.value
  //모달 닫을 때 입력 값 초기화
  if (!showModal.value){
      newFavorite.value = {
      division:'',
      bank:'',
      recipient:'',
      recipient_name:''
    }
  }
}

const addFavorite = async ()=>{
  await store.addFavorite(newFavorite.value) // 즐겨찾기 추가
  emit('refresh') // 즐겨찾기 목록 다시 불러오기
  toggleModal() // 모달 다기
}

const signOut = function(){
  store.signOut()
}

</script>

<!-- <style scoped>
.btn-primary, .btn-primary:hover, .btn-primary:active, .btn-primary:visited {
    background-color: #196DDC;
}
.btn-outline-primary{
  color: #196DDC;
  padding : 0px;
}
.text-primary{
  color: #196DDC;
}
.justify-content-custom {
    display: flex;
    justify-content: space-evenly; /* 기본적으로 evenly 적용 */
    gap: 700px; /* 간격 조정 */
  }
.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {  /* modal-contetn -> modal-content로 수정 */
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  min-width: 300px;
  max-width: 500px;
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
}

.form-group input {
  width: 100%;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.submit-button, .cancel-button {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  margin-right: 10px;
}

.submit-button {
  background-color: #007bff;
  color: white;
}

.cancel-button {
  background-color: #6c757d;
  color: white;
}
</style> -->