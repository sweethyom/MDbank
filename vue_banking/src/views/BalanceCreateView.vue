<template>
    <div>
        <p v-if="balance.Ldbl">{{ balance.Ldbl }}</p>
        <p v-if="balance.Header && balance.Header.Rsms">{{ balance.Header.Rsms }}</p>
    </div>
</template>

<script setup>
import axios from 'axios';
import { onMounted, ref } from 'vue';

const count = ref(localStorage.getItem('count') ? parseInt(localStorage.getItem('count')) : 56);

const incrementCount = () => {
  count.value++;
  localStorage.setItem('count', count.value); // 증가한 값을 localStorage에 저장
};
const balance = ref({ Header: {} })
onMounted(()=>{
    incrementCount()
    axios({
    method:'post',
    url:'https://developers.nonghyup.com/InquireBalance.nh',
    data:{
        "Header": {
            "ApiNm": "InquireBalance",
            "Tsymd": "20241115",
            "Trtm": "112428",
            "Iscd": "002697",
            "FintechApsno": "001",
            "ApiSvcCd": "ReceivedTransferA",
            "IsTuno": "0000"+count.value,
            "AccessToken": "ff021967c9d8bc5b846e9a8b8911d96d2030ad17a56df1139b62b620bcabbc36"
        },
        "FinAcno": "00820100026970000000000018376"
    }
})
.then((res)=>{
    console.log(res)
    console.log(res.data)
    balance.value = res.data
})
.catch((err)=>{
    console.log(err)
})
})
</script>

<style scoped>

</style>