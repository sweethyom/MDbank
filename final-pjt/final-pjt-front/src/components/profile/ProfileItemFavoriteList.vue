<template>
  <div class="favorite-item">
    <div class="favorite-info">
      <span class="favorite-label">{{ favorites.division }}</span>
      <span class="divider">|</span>
      <span class="favorite-name">{{ favorites.recipient_name }}</span>
      <span class="divider">|</span>
      <span class="favorite-bank">{{ bankName }}</span>
      <span class="divider">|</span>
      <span class="favorite-account">{{ favorites.recipient }}</span>
    </div>
    <div class="favorite-actions">
      <button class="action-btn edit-btn" @click="toggleModal">
        <i class="fas fa-edit"></i> 수정
      </button>
      <button class="action-btn delete-btn" @click="deleteFavorite">
        <i class="fas fa-trash-alt"></i> 삭제
      </button>
    </div>

    <!-- 즐겨찾기 수정 모달 -->  
    <Teleport to="body">
      <div v-if="showModal" class="modal-backdrop" @click="toggleModal">
        <div class="modal-content" @click.stop>
          <h2 class="modal-title">
            <i class="fas fa-star me-2"></i>즐겨찾기 수정
          </h2>
          <form @submit.prevent="updateFavorite">
            <div class="form-group">
              <label for="division">별명</label>
              <input type="text" id="division" v-model="editFavorite.division" :placeholder="favorites.division">
            </div>
            <div class="form-group">
              <label for="bank">은행이름</label>
              <select id="bank" v-model="editFavorite.bank" class="form-select">
                <option value="" disabled selected>{{ bankName }}</option>
                <option v-for="bank in profileData.banks" :key="bank.id" :value="bank.id" >
                  {{ bank.name }}
                </option>
              </select>
            </div>
            <div class="form-group">
              <label for="recipient">계좌번호</label>
              <input type="text" id="recipient" v-model="editFavorite.recipient" :placeholder="favorites.recipient">
            </div>
            <div class="form-group">
              <label for="recipient-name">받는 분 이름</label>
              <input type="text" id="recipient-name" v-model="editFavorite.recipient_name" :placeholder="favorites.recipient_name">
            </div>
            <div class="modal-actions">
              <button type="submit" class="submit-button">
                <i class="fas fa-check me-2"></i>수정
              </button>
              <button type="button" @click="toggleModal" class="cancel-button">
                <i class="fas fa-times me-2"></i>취소
              </button>
            </div>
          </form>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script setup>
import { ref,computed } from 'vue';
import { useMemberStore } from '@/stores/modules/member';
const store = useMemberStore()

const props = defineProps({
  favorites: Object,
  profileData: Object
})

const bankName = computed(()=>{
  const bank = props.profileData.banks.find(bank=>bank.id === props.favorites.bank)
  return bank? bank.name: ''
})
const emit = defineEmits(['refresh'])
const showModal = ref(false)

const editFavorite = ref({
  division:'',
  bank:'',
  recipient:'',
  recipient_name:''
})

const toggleModal = function(){
  showModal.value = !showModal.value
  if (!showModal.value){
    editFavorite.value = {
      division:'',
      bank:'',
      recipient:'',
      recipient_name:'' 
    }
  }
}

const updateFavorite = async () => {
  await store.updateFavorite(props.favorites.id, editFavorite.value)
  toggleModal()
  emit('refresh')
}


const deleteFavorite = async () => {
  if(confirm('정말 삭제하시겠습니까?')) {
    await store.deleteFavorite(props.favorites.id)
    emit('refresh')
  }
}
</script>

<style scoped>
.favorite-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  background: white;
  border-radius: 10px;
  margin-bottom: 0.5rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
}

.favorite-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.favorite-info {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.favorite-label {
  font-weight: 600;
  color: #196DDC;
}

.divider {
  color: #ccc;
}

.favorite-name, .favorite-account {
  color: #666;
}
.favorite-bank{
  color: #666;
}
.favorite-actions {
  display: flex;
  gap: 0.5rem;
}

.action-btn {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 8px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.edit-btn {
  background: #196DDC;
  color: white;
}

.edit-btn:hover {
  background: #1557B0;
}

.delete-btn {
  background: #dc3545;
  color: white;
}

.delete-btn:hover {
  background: #c82333;
}

/* 모달 스타일링 */
.modal-backdrop {
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
  position: relative;
  background: white;
  padding: 2rem;
  border-radius: 15px;
  width: 90%;
  max-width: 500px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
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
  border: 2px solid rgba(25, 109, 220, 0.1);
  border-radius: 10px;
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
  border-radius: 10px;
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

@media (max-width: 768px) {
  .favorite-item {
    flex-direction: column;
    gap: 1rem;
    text-align: center;
  }
  
  .favorite-info {
    flex-direction: column;
    gap: 0.5rem;
  }
  
  .divider {
    display: none;
  }
}
</style>
