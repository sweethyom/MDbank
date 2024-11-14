<template>
    <div>
        <form @submit.prevent="searchPayment">
            <div>
            <label for="Acno">Acno</label>
            <input type="text" id="Acno" v-model="Acno">
            </div>
            <div>
            <label for="Insymd">Insymd</label>
            <input type="text" id="Insymd" v-model="Insymd">
            </div>
            <div>
            <label for="Ineymd">Ineymd</label>
            <input type="text" id="Ineymd" v-model="Ineymd">
            </div>
            <input type="submit" value="조회하기">
        </form>
    </div>
</template>

<script setup>
import axios from 'axios';
import { ref } from 'vue';

const Acno = ref('')
const Insymd = ref('')
const Ineymd = ref('')
const transaction = ref('')
const count = ref(localStorage.getItem('count') ? parseInt(localStorage.getItem('count')) : 37)
const searchPayment = (() =>{
    ++count.value
    axios({
      method: 'post',
      url: 'https://developers.nonghyup.com/InquireTransactionHistory.nh',
      data :{
        Header: {
          ApiNm: "InquireTransactionHistory",
          Tsymd: "20241115",
          Trtm: "112428",
          Iscd: "002697",
          FintechApsno: "001",
          ApiSvcCd: "ReceivedTransferA",
          IsTuno: "0000"+count.value,
          AccessToken: "ff021967c9d8bc5b846e9a8b8911d96d2030ad17a56df1139b62b620bcabbc36"
        },
        Bncd: "011",
        Acno: Acno.value,
        Insymd: Insymd.value,
        Ineymd: Ineymd.value,
        TrnsDsnc: "A",
        Lnsq: "ASC",
        PageNo: "1",
        Dmcnt: "100"

      }
    })
    .then ((response)=>{
      transaction.value = response.data
      console.log(response)
      console.log(response.data)
    })
    .catch((err)=>{
      console.log(err)
    })
})
</script>

<style scoped>

</style>