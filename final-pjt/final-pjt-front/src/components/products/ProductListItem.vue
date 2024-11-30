<template>
    <div v-if="product">
        <table class="table table-hover mb-0">
            <tbody>
                <tr>
                    <th scope="row">
                        <span v-if="product.type === 1" class="badge text-bg-warning">예금</span>
                        <span v-else-if="product.type === 2" class="badge text-bg-success">적금</span>
                        <span v-else class="badge text-bg-secondary">입출금</span>
                    <div class="d-flex flex-column ms-2">
                        <RouterLink 
                        :to="`/product/${product.id}`" 
                        class="d-flex align-items-center link-offset-2 link-underline link-underline-opacity-0 text-dark ms-2">
                            <h3 class="me-2 text-dark">
                                {{ product.fin_prdt_nm }}</h3>
                        </RouterLink>
                        <h6 class="text-muted mb-0 ms-2">최고 {{ product?.rates?.intr_rate2 }}%</h6>
                    </div>
                </th>
                </tr>
            </tbody>
        </table>
    </div>
    <div v-else>
        데이터를 로딩 중입니다.
    </div>
</template>

<script setup>

defineProps({
    product: Object
})


</script>

<style scoped>

</style>