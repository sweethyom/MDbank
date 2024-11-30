<template>
    <div>
        <ProductListItem 
        v-for="product in products"
        :key="product.id"
        :product="product" />
    </div>
</template>

<script setup>
import ProductListItem from '@/components/products/ProductListItem.vue';

defineProps({
    products: Array
})
</script>

<style scoped>

</style>