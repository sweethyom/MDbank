<template>
    <div class="asset-type-container">
        <!-- 상단 섹션 -->
        <section v-if="!store.myType" class="header-section">
            <br>
            <h4 class="slide-up-fade-in first">지금 나의 자산은 어떻게 관리 되고 있을까요? <br>
                나의 자산관리 유형을 검사해보세요!
            </h4>
            <br>
            <div class="slide-up-fade-in second">
                <button @click="assetType" class="test-button">
                    나의 자산관리 유형 검사하기
                </button>
            </div>
        </section>

        <!-- 분석 결과 섹션 -->
        <div v-if="store.myType" class="fade-in-up">
        <div v-if="store.myType">
            <!-- 유형 설명 섹션 -->
             
            <h4 style="text-align: center;">나의 자산관리 유형은</h4>
            <section class="type-section">
                <div class="type-card_animal" style="text-align: center;">
                    <img v-if="store.myType.type.title === '느릿느릿 거북이 타입'" 
                        src="../../public/images/turtle.jpeg" style="width: 200px; height: 200px;"
                        alt="거북이 이미지">
                    <img v-if="store.myType.type.title === '플렉스 호랑이 타입'" 
                        src="../../public/images/tiger.jpeg "  style="width: 200px; height: 200px;"
                        alt="호랑이 이미지">
                    <p>"{{ store.myType.type.title }}"</p>   
                </div>
                <div class="type-card">
                    <p>{{ store.myType.type.description }}</p>
                </div>
            </section>

            <!-- 차트 섹션 -->
            <section class="chart-section" style=" margin-top: 20px;">
                <h3 style="text-align: center;">{{store.memberName}} 님의 자산 관리 분석</h3>
                <div class="chart-grid">
                    <div class="chart-item">
                        <h4>나의 자산 분포</h4>
                        <Pie
                            v-if="myPieData"
                            :data="myPieData"
                            :options="pieOptions"
                            class="chart"
                        />
                    </div>
                    <div class="chart-item">
                        <h4>평균 자산 분포</h4>
                        <Pie
                            v-if="peerPieData"
                            :data="peerPieData"
                            :options="pieOptions"
                            class="chart"
                        />
                    </div>
                    <div class="chart-item">
                        <h4>자산 비교</h4>
                        <Bar
                            v-if="chartData"
                            :data="chartData"
                            :options="chartOptions"
                            class="chart"
                        />
                    </div>
                </div>
            </section>

            <!-- 추천 상품 섹션 -->
            <section class="recommendation-section">
                <h3>{{store.memberName}} 님을 위한 추천 상품</h3>
                <!-- store.recommendData?.recommendations가 없을 때만 버튼 표시 -->
                <button v-if="!store.recommendData" 
                        @click="recommend" 
                        class="recommend-button">
                    금융상품 추천받기
                </button>
                <div v-if="store.recommendData?.recommendations" class="recommendation-grid">
                    <div 
                        class="recommendation-item" 
                        v-for="(recommendation, index) in store.recommendData.recommendations" 
                        :key="index"
                    >
                        <div class="recommendation-card">
                            
                            <h4>{{ recommendation.product_name }}</h4>   
                            <p>{{ recommendation.explanation }}</p>
                            <p>최대 금리: {{ recommendation.max_interest }}</p>
                            <p>최대 가입기간: {{ recommendation.max_period }}</p>
                        </div>
                    </div>
                </div>
            </section>
        </div>
        </div>
    </div>
</template>

<script setup>
import { onBeforeUnmount } from 'vue';
import { useMemberStore } from '@/stores/modules/member';
import { ref, computed } from 'vue';
import { Bar, Pie } from 'vue-chartjs';
import { 
    Chart as ChartJS, 
    CategoryScale, 
    LinearScale, 
    BarElement, 
    Title, 
    Tooltip, 
    Legend,
    ArcElement
} from 'chart.js';
// Chart.js 컴포넌트 등록
ChartJS.register(
    CategoryScale,
    LinearScale,
    BarElement,
    Title,
    Tooltip,
    Legend,
    ArcElement
);

const store = useMemberStore();

// 나의 자산 분포 파이 차트 데이터
const myPieData = computed(() => {
    if (!store.myType) return null;
    
    const total = store.myType.customer_avg_expenses + 
                 store.myType.customer_avg_income + 
                 store.myType.customer_avg_savings;
                 
    return {
        labels: ['지출', '수입', '저축'],
        datasets: [{
            backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56'],
            data: [
                ((store.myType.customer_avg_expenses / total) * 100).toFixed(1),
                ((store.myType.customer_avg_income / total) * 100).toFixed(1),
                ((store.myType.customer_avg_savings / total) * 100).toFixed(1)
            ]
        }]
    };
});

// 평균 자산 분포 파이 차트 데이터
const peerPieData = computed(() => {
    if (!store.myType) return null;
    
    const total = store.myType.peer_avg_expenses + 
                 store.myType.peer_avg_income + 
                 store.myType.peer_avg_savings;
                 
    return {
        labels: ['지출', '수입', '저축'],
        datasets: [{
            backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56'],
            data: [
                ((store.myType.peer_avg_expenses / total) * 100).toFixed(1),
                ((store.myType.peer_avg_income / total) * 100).toFixed(1),
                ((store.myType.peer_avg_savings / total) * 100).toFixed(1)
            ]
        }]
    };
});

// 파이 차트 옵션
const pieOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
        legend: {
            position: 'bottom',
        },
        tooltip: {
            callbacks: {
                label: function(context) {
                    return `${context.label}: ${context.raw}%`;
                }
            }
        }
    }
};

// 기존의 Bar 차트 데이터와 옵션은 유지
const chartData = computed(() => {
    if (!store.myType) return null;
    
    return {
        labels: ['지출', '수입', '저축'],
        datasets: [
            {
                label: '나의 데이터',
                backgroundColor: '#36A2EB',
                data: [
                    store.myType.customer_avg_expenses,
                    store.myType.customer_avg_income,
                    store.myType.customer_avg_savings
                ]
            },
            {
                label: '평균 데이터',
                backgroundColor: '#FF6384',
                data: [
                    store.myType.peer_avg_expenses,
                    store.myType.peer_avg_income,
                    store.myType.peer_avg_savings
                ]
            }
        ]
    };
});

const assetType = function() {
    store.assetType();
};

const recommend = function() {
    store.recommend();
};

onBeforeUnmount(() => {
    store.myType = null;
    store.recommendData = null;
});
</script>
<style scoped>
.type-card_animal {
    width: 200px;
    height: 250px;
    background-color: white;  /* 배경색 */
    border-radius: 10px;  /* 모서리 둥글게 */
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);  /* 그림자 효과 */
    margin-bottom: 50px;  /* 가운데 정렬 */
    margin-top:50px
}


.asset-type-container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
    background-color: #e7f4fc;
}

.header-section {
    text-align: center;
    margin-bottom: 40px;
}

.empty-card {
    background-color: white;
    padding: 40px;
    border-radius: 10px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    margin: 20px auto;
    max-width: 400px;
}

.test-button {
    background-color: #3699f5;
    color: white;
    padding: 15px 30px;
    border: none;
    border-radius: 5px;
    font-size: 1.1em;
    cursor: pointer;
    transition: all 0.3s ease;  /* 모든 변화에 트랜지션 적용 */
    box-shadow: 0 4px 6px rgba(54, 153, 245, 0.2);  /* 기본 그림자 */
}

.test-button:hover {
    background-color: #3699f5;
    transform: translateY(-2px);  /* 호버시 살짝 위로 */
    box-shadow: 0 6px 12px rgba(54, 153, 245, 0.3);  /* 호버시 그림자 강화 */
}


.test-button:active {
    transform: translateY(1px);  /* 클릭시 살짝 아래로 */
    box-shadow: 0 2px 4px rgba(54, 153, 245, 0.2);  /* 클릭시 그림자 약화 */
}

.type-section {
    margin-bottom: 40px;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 20px;
}

.type-card {
    background-color: white;
    padding: 30px;
    border-radius: 10px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    text-align: center;
}

.chart-section {
    margin-bottom: 60px;  /* 섹션 간격 증가 */
    padding: 20px;
}

.chart-grid {
    display: grid;
    grid-template-columns: 1fr;  /* 3열에서 1열로 변경 */
    gap: 40px;
    margin-top: 30px;
    padding: 20px;
}

.chart-item {
    background-color: white;
    padding: 50px;
    border-radius: 10px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    height: 450px;
    text-align: center;
    transition: transform 0.2s ease;
    max-width: 800px;  /* 최대 너비 설정 */
    margin: 0 auto;  /* 중앙 정렬 */
}

.chart-item:hover {
    transform: translateY(-5px);  /* 호버 시 약간 위로 올라가는 효과 */
    box-shadow: 0 4px 8px rgba(0,0,0,0.15);
}

.chart-item h4 {
    margin-bottom: 20px;  /* 제목 아래 여백 증가 */
    color: #333;
    font-size: 1.2em;  /* 제목 크기 약간 증가 */
}

.chart {
    width: 100%;
    height: calc(100% - 40px);  
}


/* 반응형일 때도 높이 조정 */
@media (max-width: 768px) {
    .chart-item {
        height: 400px;  /* 모바일에서도 충분한 높이 유지 */
    }
}

@media (max-width: 768px) {
    .chart-grid {
        grid-template-columns: 1fr;
        gap: 30px;
    }
    
    .chart-item {
        height: 300px;
    }
}



.recommendation-section {
    margin-top: 40px;
    text-align: center;
}

.recommend-button {
    background-color: #3699f5;
    color: white;
    padding: 15px 30px;
    border: none;
    border-radius: 5px;
    font-size: 1.1em;
    cursor: pointer;
    transition: all 0.3s ease;  /* 모든 변화에 트랜지션 적용 */
    margin: 20px 0;
    box-shadow: 0 4px 6px rgba(54, 153, 245, 0.2);  /* 기본 그림자 */
}

.recommend-button:hover {
    background-color: #3699f5;
    transform: translateY(-2px);  /* 호버시 살짝 위로 */
    box-shadow: 0 6px 12px rgba(54, 153, 245, 0.3);  /* 호버시 그림자 강화 */
}

.recommend-button:active {
    transform: translateY(1px);  /* 클릭시 살짝 아래로 */
    box-shadow: 0 2px 4px rgba(54, 153, 245, 0.2);  /* 클릭시 그림자 약화 */
}

.recommendation-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 30px;
    margin-top: 30px;
    padding: 20px;
}

.recommendation-item {
    background-color: white;
    border-radius: 10px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    transition: transform 0.2s ease;
}

.recommendation-item:hover {
    transform: translateY(-5px);
    box-shadow: 0 4px 8px rgba(0,0,0,0.15);
}

.recommendation-card {
    padding: 30px;
}

.recommendation-card h4 {
    color: #333;
    margin-bottom: 15px;
    font-size: 1.2em;
}

.recommendation-card p {
    color: #666;
    margin: 10px 0;
    line-height: 1.5;
}

/* 반응형 디자인 */
@media (max-width: 1024px) {
    .recommendation-grid {
        grid-template-columns: repeat(2, 1fr);
    }
}

@media (max-width: 768px) {
    .recommendation-grid {
        grid-template-columns: 1fr;
    }
}


/* 슬라이드 업 애니메이션 */
@keyframes slideUpFadeIn {
    0% {
        transform: translateY(100px);
        opacity: 0;
    }
    100% {
        transform: translateY(0);
        opacity: 1;
    }
}

.slide-up-fade-in {
    opacity: 0;
    animation: slideUpFadeIn 0.8s ease forwards;
}

/* 순차적으로 애니메이션 적용 */
.first {
    animation-delay: 0.3s;
}

.second {
    animation-delay: 0.6s;
}
/* 슬라이드업 끝 */




/* 분석 결과 슬라이드업 */
@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(50px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.fade-in-up {
    animation: fadeInUp 0.8s ease-out forwards;
    opacity: 0;  /* 초기 상태는 투명 */
}

/* 모바일에서는 애니메이션 비활성화 (선택사항) */
@media (max-width: 768px) {
    .fade-in-up {
        animation: none;
        opacity: 1;
    }
}

</style>