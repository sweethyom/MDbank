<template>
  <div class="d-flex justify-content-between">
    <div>
    <span>{{ bankAccounts.account_name }}</span> <span>{{ bankAccounts.account_num }}</span>
  </div>
  <button class="btn btn-primary fw-bold">상세보기</button>


  </div>
</template>

<script setup>
defineProps({
  bankAccounts: Object
})

</script>

<style scoped>
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
</style>