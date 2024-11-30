<template>
    <div>
        <h1>어딘데 여기</h1>
        <h1>{{ product.fin_prdt_nm }}</h1>
        <h2>{{ product.mtrt_int }}</h2>
        <h5>{{ product.cpcl_cnd }}</h5>
        <h5>{{ product.join_member }}</h5>
        <h5>{{ product.etc_note}}</h5>
        <h5>{{ product.rates.intr_rate2 }}</h5>
        <hr>
    </div>
</template>

<script setup>
defineProps({
    product: Object
})
</script>

<style scoped>

</style>