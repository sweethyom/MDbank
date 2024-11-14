<template>
  <div>
    <RouterLink :to="{name:'BankingCreateView'}">거래내역 조회해보기</RouterLink> |
    <RouterLink :to="{name:'BalanceCreateView'}">잔액조회</RouterLink>
    <RouterView />
  </div>
</template>

<script setup>
import { RouterLink, RouterView } from 'vue-router';
import { useBankingStore } from './stores/Banking';

const store= useBankingStore()
store.postPayment

</script>

<style scoped>

</style>