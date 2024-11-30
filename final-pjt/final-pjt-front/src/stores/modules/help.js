import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import { useMemberStore } from '@/stores/modules/member' 
import { useRouter } from 'vue-router'


export const useHelpStore = defineStore('help', () => {
    
    const questions = ref([])
    const memberStore = useMemberStore()
    const router = useRouter()
    const API_URL = 'http://127.0.0.1:8000'
    // 문의 리스트 보기
    const QandA = async () => {
        try {
            const response = await axios({
                method: 'get',
                url: `${API_URL}/customers/qanda/`,
            })
            questions.value = response.data
            return response.data
        } catch (error) {
            console.error('문의 목록 조회 실패:', error)
            throw error
        }
    }

    // 상세 내역 보기
    const getQuestionDetail = async (questionId) => {
        try {
            console.log('Requesting question detail for ID:', questionId)  // 디버깅용
            const response = await axios({
                method: 'get',
                url: `${API_URL}/customers/qanda/${questionId}/`,
                headers: {
                    Authorization: `Token ${memberStore.token}`
                }
            })
            console.log('Server response:', response.data)  // 디버깅용
            return response.data
        } catch (error) {
            console.error('질문 상세 조회 실패:', error.response?.data || error)
            throw error
        }
    }

    // 카테고리 데이터 가져오기

    // const categories = ref([]);
    const fetchCategories = async () => {
        try {
            const response = await axios({
                method: 'get',
                url: `${API_URL}/customers/qanda/category/`, // API 엔드포인트
            });
            // categories.value = response.data; // 가져온 데이터 저장
            console.log(response.data)
            return response.data;
        } catch (error) {
            console.error('카테고리 데이터 가져오기 실패:', error);
            throw error;
        }
    };
    

    // 게시글 생성
    const createQuestion = async (questionData) => {
        try {
            // 데이터 형식 확인
            console.log('보내는 데이터:', questionData)
            
            // private이 false인 경우 password 제거
            if (!questionData.private) {
                delete questionData.password
            }
    
            const response = await axios({
                method: 'post',
                url: `${API_URL}/customers/qanda/create/`,
                data: {
                    category: questionData.category,
                    title: questionData.title,
                    content: questionData.content,
                    private: questionData.private,
                    password: questionData.password,
                    member_pk: questionData.memberPk                 
                },
                headers: {
                    Authorization: `Token ${memberStore.token}`
                }   
            })
            
            return response.data
        } catch (error) {
            console.error('문의글 생성 실패:', error.response?.data)
            throw error
        }
    }

    // 게시글 수정  
    const updateQuestion= function(payload){
  
        const id = payload.id
        const categoryId = parseInt(payload.category) 
        const title = payload.title
        const content = payload.content
        const isprivate = payload.isprivate
        const password = payload.password
        axios({
            method:'put',
            url:`${API_URL}/customers/qanda/update/${id}/`,
            data:{

                category:categoryId,
                title:title,
                content:content,
                private: isprivate, 
                password:password,
            },
            headers:{
                Authorization: `Token ${memberStore.token}`
            }
        })
        .then((res)=>{
            console.log('문의 수정 성공')
            console.log(res)
            router.push(`/qanda/${payload.id}`)
        })

    }

    // 게시글 삭제
    const deleteQuestion = (questionId)=>{
        axios({
            method:'delete',
            url:`${API_URL}/customers/qanda/delete/${questionId}/`,
            headers:{
                Authorization: `Token ${memberStore.token}`
            }
        })
        .then((res)=>{
            console.log('게시글 삭제 성공')
            router.push('/qna')
        })
        .catch((err)=>{
            console.log('게시글 삭제 실패', err)
        })
    }

    // 답변 조회
    const getAnswerForQuestion = async(questionId) => {
        try {
          const memberStore = useMemberStore()
          const response = await axios({
            method: 'get',
            url: `${API_URL}/customers/qanda/${questionId}/answer/`,
            headers: {
              Authorization: `Token ${memberStore.token}`
            }
          })
          console.log('답변 데이터 조회:', response.data)
          return response.data
        } catch (error) {
          console.error('답변 조회 실패:', error)
          return null  // 답변이 없는 경우 null 반환
        }
      }

    // 답변 생성
    const createAnswer = async(payload)=>{
        try {
            const content=payload.content
            const question_id=payload.question_id
            const response = await axios({
                method: 'post',
                url: `${API_URL}/customers/qanda/${payload.question_id}/answer/create/`,
                data: {
                    content, question_id
                },
                headers: {
                    Authorization: `Token ${memberStore.token}`
                }
            })
            // console.log('답변 생성 성공:', response.data)
            return response.data
        } catch (error) {
            // console.error('답변 생성 실패:', error)
            throw error
        }
    }
        
    return { QandA, questions, fetchCategories,
        createQuestion, getQuestionDetail,updateQuestion, deleteQuestion, 
        createAnswer, getAnswerForQuestion }
})
