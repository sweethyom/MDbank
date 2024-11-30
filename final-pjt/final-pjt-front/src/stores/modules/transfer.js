import { defineStore } from 'pinia'
import { ref,watch } from 'vue'
import axios from 'axios'


export const useTransferStore = defineStore('transfer', () => {
  const accessToken = import.meta.env.VITE_ACCESS_TOKEN
  const finacn=import.meta.env.VITE_FINACNO


 
  // localStorage.setItem('lastIsTuno', '0000800'); 
  const savedIsTuno = localStorage.getItem('lastIsTuno');
  const lastIsTuno = ref(savedIsTuno ? savedIsTuno : '0000282');



  const now = new Date()
  const history = ref(null)
  const currentDate = now.getFullYear() + 
                      String(now.getMonth() + 1).padStart(2, '0') + 
                      String(now.getDate()).padStart(2, '0')
  const currentTime = String(now.getHours()).padStart(2, '0') + 
                      String(now.getMinutes()).padStart(2, '0') +
                      String(now.getSeconds()).padStart(2, '0')
  

  //계좌이체
  const transfer = function (payload) {
    const nextIsTuno = (parseInt(lastIsTuno.value.replace('A0000', '')) + 1).toString().padStart(3, '0')
    const currentIsTuno = 'A'+'0000' + nextIsTuno
    axios({
      method:'post',
      url:'https://developers.nonghyup.com/DrawingTransfer.nh',
      data:{
        Header: {
          ApiNm: "DrawingTransfer",
          Tsymd: currentDate,
          Trtm: currentTime,
          Iscd: "002697",
          FintechApsno: "001",
          ApiSvcCd: "DrawingTransferA",
          IsTuno: currentIsTuno,
          AccessToken: accessToken
        },
        FinAcno: finacn,   // 핀어카운트
        Tram: payload.money, // 거래금액
        DractOtlt: payload.myMemo //출금계좌 인지 내용
      }
    })
    .then((res) => {
      lastIsTuno.value = res.data.Header.IsTuno
      localStorage.setItem('lastIsTuno', res.data.Header.IsTuno)  // 추가
      console.log(currentTime, currentDate)
      console.log(res.data)
      alert('이체가 완료되었습니다.')
      
    })
    .catch((err) => {
      console.log(err)
    })
  }  

  // 이체 내역
  const transferHistory = function(payload){
    const nextIsTuno = (parseInt(lastIsTuno.value.replace('A0000', '')) + 1).toString().padStart(3, '0')
    const currentIsTuno = 'A'+'0000' + nextIsTuno
    axios({
      method:'post',
      url: 'https://developers.nonghyup.com/InquireTransactionHistory.nh',
      data :{
        Header: {
          ApiNm: "InquireTransactionHistory",
          Tsymd: currentDate,
          Trtm: currentTime,
          Iscd: "002697",
          FintechApsno: "001",
          ApiSvcCd: "ReceivedTransferA",
          IsTuno: currentIsTuno,
          AccessToken: accessToken
        },
        Bncd: "011",
        Acno: 3020000011750,
        Insymd: payload.insymd,
        Ineymd: payload.ineymd,
        TrnsDsnc: "A",
        Lnsq: "ASC",
        PageNo: "1",
        Dmcnt: "100"

      }
    })
    .then((res) => {
      lastIsTuno.value = res.data.Header.IsTuno
      localStorage.setItem('lastIsTuno', res.data.Header.IsTuno)  // 추가  res.data.Header.IsTuno
      console.log(res.data)
      history.value = res.data.REC
      // console.log('history', history.value)
      // return history.value

    })
    .catch((err) => {
      console.log(err)
    })
  }


  // 잔액조회
  const balance = ref(null)
  const balanceSearch = function(){
    const nextIsTuno = (parseInt(lastIsTuno.value.replace('A0000', '')) + 1).toString().padStart(3, '0')
    const currentIsTuno = 'A'+'0000' + nextIsTuno

    axios({
      method:'post',
      url:'https://developers.nonghyup.com/InquireBalance.nh',
      data:{
        "Header": {
            "ApiNm": "InquireBalance",
            "Tsymd": currentDate,
            "Trtm": currentTime,
            "Iscd": "002697",
            "FintechApsno": "001",
            "ApiSvcCd": "ReceivedTransferA",
            "IsTuno": currentIsTuno,
            "AccessToken": accessToken
        },
        "FinAcno": finacn
      }
    })
    .then((res) => {
      lastIsTuno.value = res.data.Header.IsTuno
      localStorage.setItem('lastIsTuno', res.data.Header.IsTuno)  // 추가
      console.log(res.data)
      balance.value = res.data
    })
    .catch((err) => {
      console.log(err)
    })
  }

  
  

  return {  transfer, transferHistory, history, balance, balanceSearch }  // defineStore의 반환값
})  // defineStore 콜백 함수 끝
