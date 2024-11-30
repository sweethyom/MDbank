<template>
  <div v-if="store.profileData">
    <Profileitem 
    :profile-data="store.profileData"
    @refresh="fetchProfileData"
    />
  </div>
  <div v-else>
    데이터를 불러오는 중입니다...
  </div>
</template>

<script setup>


import Profileitem from '@/components/profile/ProfileItem.vue';
import { useMemberStore } from '@/stores/modules/member'
import { onMounted, ref } from 'vue';

// const profileData= ref(null)
const store = useMemberStore()
const fetchProfileData =async()=>{
  await store.profile()
  // profileData.value = store.profileData 
}

onMounted(()=>{
  store.profile()
})

 
</script>

<style scoped>

</style>
