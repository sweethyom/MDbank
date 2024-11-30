import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'

export const useProductStore = defineStore('product', () => {
    const products = ref([])
    const API_URL = 'http://127.0.0.1:8000'
    const histogramData = ref(null)
    const isLoading = ref(false);
    const productList = function(){
        axios({
            method: 'GET',
            url: `${API_URL}/products/productlist/`
        })
        .then(res=>{
            products.value = res.data
            console.log(products.value)
        })
        .catch(err=>{
            console.log(err)
        })
    }

    const exchange_data = ref(null)
    const exchange = function(currency){
        isLoading.value = true;
        axios({
            method:'get',
            url: `${API_URL}/products/exchange_rate/`,
            // get 요청에서는 parmas로 데이터 전달해야한다
            params: {
                cur_unit:currency,
            } 
        })
        .then(res=>{
            console.log(res.data.exchange_data)
            exchange_data.value = res.data.exchange_data
        })
        .catch(err => {
            console.error(err);
        })
        .finally(() => {
            isLoading.value = false;
        });
    }

    // const saveCurrency=function(currency){
    //     axios({
    //         method: 'post',

    //     })
    // }
    const requestCurrency = function(currency) {
        axios({
            method: 'post',
            url: `http://127.0.0.1:8000/products/request-currency/`,
            data: { cur_unit: currency }
        })
        .then(res => {
            const base64Image = res.data.histogram; // base64 인코딩된 이미지
            histogramData.value = `data:image/png;base64,${base64Image}`; // 반응형 데이터 업데이트
        })
        .catch(err => {
            console.error('환율 요청에 에러뜸', err);
        });
    }
    

  return {products, productList, exchange_data, exchange, requestCurrency, histogramData }
}, { persist: true })


