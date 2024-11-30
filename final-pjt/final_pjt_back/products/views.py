import base64
import datetime
from django.shortcuts import render
from django.conf import settings
from rest_framework.response import Response
from django.db.models import Max
import requests
from .models import Product, Option
from banks.models import Payment, BankAccount
from products.models import Asset_type
from .serializers import ProductSerializer, RateComparisonSerializer, ExchangeRateSerializer
from django.http import JsonResponse, HttpResponse
from rest_framework.decorators import api_view, permission_classes
from django.db.models import Sum, Avg
from rest_framework.permissions import IsAuthenticated
import openai
from datetime import datetime, timedelta
from django.utils import timezone
from django.shortcuts import get_object_or_404
from rest_framework import status


import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
# Create your views here.
@api_view(['GET'])
def save_product(request):
    api_key=settings.PRODUCT_API_KEY
    url1 = f'http://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json?auth={api_key}&topFinGrpNo=020000&pageNo=1'
    response1=requests.get(url1).json()
    url2 = f'http://finlife.fss.or.kr/finlifeapi/savingProductsSearch.json?auth={api_key}&topFinGrpNo=020000&pageNo=1'
    response2 = requests.get(url2).json()
    # for문 작성 차례
    for product in response1.get('result').get('baseList'):
        if product.get('fin_co_no') !='0013175':
            continue        
        dcls_month=product.get('dcls_month', 'None')                  # 공시 제출월
        fin_prdt_cd=product.get('fin_prdt_cd', 'None')      # 금융회사 코드
        fin_co_no = product.get('fin_co_no', 'None')
        kor_co_nm = product.get('kor_co_nm', 'None')                 # 금융 회사 명
        fin_prdt_nm= product.get('fin_prdt_nm', 'None')                # 상품 이름
        join_way=product.get('join_way', 'None')                    # 가입 방법
        mtrt_int=product.get('mtrt_int', 'None')                    # 만기 후 이자율
        spcl_cnd=product.get('spcl_cnd', 'None')                    # 우대 조건
        join_deny=product.get('join_deny', 'None')                   # 가입 제한
        join_member=product.get('join_member', 'None')                 # 가입 대상
        etc_note=product.get('etc_note', 'None')                    # 기타 유의 사항
        max_limit=product.get('max_limit') or -1                   # 최고 한도
        dcls_strt_day=product.get('dcls_strt_day', 'None')               # 공시 시작일
        dcls_end_day=product.get('dcls_end_day', 'None')                # 공시 종료일
        fin_co_subm_day=product.get('fin_co_subm_day', 'None')             # 금융회사 제출일

        if Product.objects.filter(
        dcls_month=dcls_month,                  # 공시 제출월
        fin_prdt_cd=fin_prdt_cd,                # 금융회사 코드
        kor_co_nm =kor_co_nm,                   # 금융 회사 명
        fin_co_no = fin_co_no,                  
        fin_prdt_nm=fin_prdt_nm,                # 상품 이름
        join_way=join_way,                      # 가입 방법
        mtrt_int=mtrt_int,                      # 만기 후 이자율
        spcl_cnd=spcl_cnd,                      # 우대 조건
        join_deny=join_deny,                    # 가입 제한
        join_member=join_member,                # 가입 대상
        etc_note=etc_note,                      # 기타 유의 사항
        max_limit=max_limit,                    # 최고 한도
        dcls_strt_day=dcls_strt_day,            # 공시 시작일
        dcls_end_day=dcls_end_day,              # 공시 종료일
        fin_co_subm_day=fin_co_subm_day
        ).exists():
            continue

        save_data1={
        'type': 1,
        'dcls_month':dcls_month,                  # 공시 제출월
        'fin_co_no': fin_co_no,
        'fin_prdt_cd':fin_prdt_cd,    # 금융회사 코드
        'kor_co_nm' :kor_co_nm,            # 금융 회사 명
        'fin_prdt_nm':fin_prdt_nm,              # 상품 이름
        'join_way':join_way,                   # 가입 방법
        'mtrt_int':mtrt_int,                   # 만기 후 이자율
        'spcl_cnd':spcl_cnd,                 # 우대 조건
        'join_deny':join_deny,                # 가입 제한
        'join_member':join_member,                 # 가입 대상
        'etc_note':etc_note,                  # 기타 유의 사항
        'max_limit':max_limit,                   # 최고 한도
        'dcls_strt_day':dcls_strt_day,               # 공시 시작일
        'dcls_end_day':dcls_end_day,                # 공시 종료일
        'fin_co_subm_day':fin_co_subm_day
        }

        serializer_product = ProductSerializer(data=save_data1)
        if serializer_product.is_valid(raise_exception=True):
            product_data = serializer_product.save()
            for option in response1.get('result').get('optionList'):                ## option 리스트
                if product.get('fin_prdt_cd') == option.get('fin_prdt_cd'):        ## 상품 코드가 같은 것을 가져온다.
                    dcls_month=option.get('dcls_month', 'None')                    # 공시 제출일
                    fin_co_no= option.get('fin_co_no')                     # 금융회사 코드
                    fin_prdt_cd = option.get('fin_prdt_cd')                # 금융 상품 코드
                    intr_rate_type= option.get('intr_rate_type', 'None')           # 저축 금리 유형
                    intr_rate_type_nm= option.get('intr_rate_type_nm', 'None')     # 저축 금리 유형명
                    rsrv_type=option.get('rsrv_type')                      # 적립 유형
                    rsrv_type_nm= option.get('rsrv_type_nm')               # 적립 유형명
                    save_trm= option.get('save_trm', 'None')                        # 가입 기간
                    intr_rate=option.get('intr_rate') or -1                      # 금리
                    intr_rate2=option.get('intr_rate2') or -1                    # 우대금리

                    option, created = Option.objects.get_or_create(
                        product=product_data,
                        dcls_month=dcls_month,                  # 공시 제출일
                        fin_co_no= fin_co_no,                   # 금융회사 코드
                        fin_prdt_cd =fin_prdt_cd,               # 금융 상품 코드
                        intr_rate_type= intr_rate_type,         # 저축 금리 유형
                        intr_rate_type_nm=intr_rate_type_nm,    # 저축 금리 유형명
                        rsrv_type = rsrv_type,                    # 적립 유형
                        rsrv_type_nm = rsrv_type_nm,              # 적립 유형명
                        save_trm=save_trm,                      # 가입 기간
                        intr_rate=intr_rate,                    # 금리
                        intr_rate2=intr_rate2                   # 우대금리
                    )
        

     # for문 작성 차례
    for product in response2.get('result').get('baseList'):
        if product.get('fin_co_no') !='0013175':
            continue
        dcls_month=product.get('dcls_month', 'None')                  # 공시 제출월
        fin_prdt_cd=product.get('fin_prdt_cd', 'None')      # 금융회사 코드
        fin_co_no = product.get('fin_co_no', 'None')
        kor_co_nm = product.get('kor_co_nm', 'None')                 # 금융 회사 명
        fin_prdt_nm= product.get('fin_prdt_nm', 'None')                # 상품 이름
        join_way=product.get('join_way', 'None')                    # 가입 방법
        mtrt_int=product.get('mtrt_int', 'None')                    # 만기 후 이자율
        spcl_cnd=product.get('spcl_cnd', 'None')                    # 우대 조건
        join_deny=product.get('join_deny', 'None')                   # 가입 제한
        join_member=product.get('join_member', 'None')                 # 가입 대상
        etc_note=product.get('etc_note', 'None')                    # 기타 유의 사항
        max_limit=product.get('max_limit') or -1                   # 최고 한도
        dcls_strt_day=product.get('dcls_strt_day', 'None')               # 공시 시작일
        dcls_end_day=product.get('dcls_end_day', 'None')                # 공시 종료일
        fin_co_subm_day=product.get('fin_co_subm_day', 'None')             # 금융회사 제출일

        if Product.objects.filter(
        dcls_month=dcls_month,                  # 공시 제출월
        fin_prdt_cd=fin_prdt_cd,    # 금융회사 코드
        kor_co_nm =kor_co_nm,            # 금융 회사 명
        fin_co_no = fin_co_no,
        fin_prdt_nm=fin_prdt_nm,              # 상품 이름
        join_way=join_way,                   # 가입 방법
        mtrt_int=mtrt_int,                   # 만기 후 이자율
        spcl_cnd=spcl_cnd,                 # 우대 조건
        join_deny=join_deny,                # 가입 제한
        join_member=join_member,                 # 가입 대상
        etc_note=etc_note,                  # 기타 유의 사항
        max_limit=max_limit,                   # 최고 한도
        dcls_strt_day=dcls_strt_day,               # 공시 시작일
        dcls_end_day=dcls_end_day,                # 공시 종료일
        fin_co_subm_day=fin_co_subm_day
        ).exists():
            continue

        save_data2={
        'type': 2,
        'dcls_month':dcls_month,                  # 공시 제출월
        'fin_co_no': fin_co_no,
        'fin_prdt_cd':fin_prdt_cd,    # 금융회사 코드
        'kor_co_nm' :kor_co_nm,            # 금융 회사 명
        'fin_prdt_nm':fin_prdt_nm,              # 상품 이름
        'join_way':join_way,                   # 가입 방법
        'mtrt_int':mtrt_int,                   # 만기 후 이자율
        'spcl_cnd':spcl_cnd,                 # 우대 조건
        'join_deny':join_deny,                # 가입 제한
        'join_member':join_member,                 # 가입 대상
        'etc_note':etc_note,                  # 기타 유의 사항
        'max_limit':max_limit,                   # 최고 한도
        'dcls_strt_day':dcls_strt_day,               # 공시 시작일
        'dcls_end_day':dcls_end_day,                # 공시 종료일
        'fin_co_subm_day':fin_co_subm_day
        }

        serializer_product = ProductSerializer(data=save_data2)
        if serializer_product.is_valid(raise_exception=True):
            product_data = serializer_product.save()
            for option in response2.get('result').get('optionList'):                ## option 리스트
                if product.get('fin_prdt_cd') == option.get('fin_prdt_cd'):        ## 상품 코드가 같은 것을 가져온다.
                    dcls_month=option.get('dcls_month', 'None')                    # 공시 제출일
                    fin_co_no= option.get('fin_co_no')                     # 금융회사 코드
                    fin_prdt_cd = option.get('fin_prdt_cd')                # 금융 상품 코드
                    intr_rate_type= option.get('intr_rate_type', 'None')           # 저축 금리 유형
                    intr_rate_type_nm= option.get('intr_rate_type_nm', 'None')     # 저축 금리 유형명
                    rsrv_type=option.get('rsrv_type')                      # 적립 유형
                    rsrv_type_nm= option.get('rsrv_type_nm')               # 적립 유형명
                    save_trm= option.get('save_trm', 'None')                        # 가입 기간
                    intr_rate=option.get('intr_rate') or -1                      # 금리
                    intr_rate2=option.get('intr_rate2') or -1                    # 우대금리

                    option, created = Option.objects.get_or_create(
                        product=product_data,
                        dcls_month=dcls_month,                  # 공시 제출일
                        fin_co_no= fin_co_no,                   # 금융회사 코드
                        fin_prdt_cd =fin_prdt_cd,               # 금융 상품 코드
                        intr_rate_type= intr_rate_type,         # 저축 금리 유형
                        intr_rate_type_nm=intr_rate_type_nm,    # 저축 금리 유형명
                        rsrv_type = rsrv_type,                    # 적립 유형
                        rsrv_type_nm = rsrv_type_nm,              # 적립 유형명
                        save_trm=save_trm,                      # 가입 기간
                        intr_rate=intr_rate,                    # 금리
                        intr_rate2=intr_rate2                   # 우대금리
                    )
    return JsonResponse({'message':'저장 성공!'})

@api_view(['GET'])
def productlist(request):
    products = Product.objects.prefetch_related('rates').all()  # option_set 미리 로드
    serializer = RateComparisonSerializer(products, many=True)
    return JsonResponse(serializer.data, safe=False)





# 환율 조회 
import requests
from django.http import JsonResponse
from rest_framework.decorators import api_view
from datetime import datetime, timedelta
from django.conf import settings

@api_view(['GET'])
def exchange_rate(request):
    today = datetime.now()

    # 월요일이거나 주말인 경우, 금요일로 날짜를 조정
    if today.weekday() == 0:  # 월요일 오전 9시 이전
        today = today - timedelta(days=3)  # 금요일로 변경
    elif today.weekday() >= 5:  # 주말인 경우
        today = today - timedelta(days=today.weekday() - 4)  # 금요일로 변경

    # 날짜를 'YYYYMMDD' 형식으로 변환
    today = today.strftime('%Y%m%d')

    # API 키 확인
    api_key = settings.EXCHANGE_API_KEY
    url = f'https://www.koreaexim.go.kr/site/program/financial/exchangeJSON?authkey={api_key}&searchdate={today}&data=AP01'

    # 외부 API 호출 및 응답 처리
    try:
        api_response = requests.get(url, verify=False)
        if api_response.status_code != 200:
            return JsonResponse({'error': 'Failed to fetch data from the exchange API'}, status=500)
        
        try:
            response = api_response.json()
        except ValueError:
            return JsonResponse({'error': 'Invalid JSON response from API'}, status=500)
    except requests.exceptions.RequestException as e:
        return JsonResponse({'error': f'API request failed: {str(e)}'}, status=500)

    # 요청한 통화 단위 받아오기
    cur_unit = request.GET.get('cur_unit')
    if not cur_unit:
        return JsonResponse({'error': 'No currency provided'}, status=400)
    
    # 통화 코드에 맞는 데이터를 찾기
    filtered_data = next(
        (data for data in response if data['cur_unit'] == cur_unit and 'ttb' in data and data['ttb']),
        None
    )
    if filtered_data:
        return JsonResponse({'exchange_data': filtered_data['ttb']}, safe=False)
    else:
        return JsonResponse({'error': 'Currency not found'}, status=404)

def fetch_exchange_rates(url):
    try:
        print(f"요청 URL: {url}")
        response = requests.get(url, verify=True)
        print(f"응답 상태 코드: {response.status_code}")
        print(f"응답 본문: {response.text}")
        response.raise_for_status()
        if not response.text:
            print("응답 본문이 비어 있습니다.")
            return None
        data = response.json()
        print(f"API 응답 데이터: {data}")
        return data
    except requests.RequestException as e:
        print(f"API 요청 실패: {e}")
        return None
    
def save_exchange_rates():
    api_key = settings.EXCHANGE_API_KEY
    today = datetime.now()
    dates = [
    (today - timedelta(days=i)).strftime('%Y%m%d') 
    for i in range(1, 31)  # 1일~30일 전까지
    if (today - timedelta(days=i)).weekday() < 5  # 월(0) ~ 금(4)만 포함
    ]
    for date in dates:
        url = f'https://www.koreaexim.go.kr/site/program/financial/exchangeJSON?authkey={api_key}&searchdate={date}&data=AP01'
        data = fetch_exchange_rates(url)
            # API 호출 결과가 있는 경우 처리
        if data:
            for record in data:
                # 환율 데이터를 데이터베이스에 저장
                serializer = ExchangeRateSerializer(data={
                    'date':date,
                    'cur_unit': record.get('cur_unit'),
                    'ttb': record.get('ttb'),
                    'tts': record.get('tts'),
                    'deal_bas_r':record.get('deal_bas_r'),
                    'bkpr': record.get('bkpr'),
                    'yy_efee_r': record.get('yy_efee_r'),
                    'ten_dd_efee_r': record.get('ten_dd_efee_r'),
                    'kftc_bkpr': record.get('kftc_bkpr'),
                    'kftc_deal_bas_r': record.get('kftc_deal_bas_r'),
                    'cur_nm': record.get('cur_nm'),
                })
                if not serializer.is_valid():
                    # 유효하지 않으면 오류 메시지 출력
                    print(f"유효하지 않은 데이터: 날짜={date}, 오류={serializer.errors}")
                    continue  # 오류가 발생하면 다음 데이터로 넘어감

                serializer.save()
                print(f"저장됨: 날짜={date}, 통화={record.get('cur_unit')}, 환율={record.get('deal_bas_r')}")
        else:
            print(f"데이터 없음: 날짜={date}")
    return Response({"message": "환율 데이터가 저장되었습니다."}, status=status.HTTP_200_OK)  

import pandas as pd
from .serializers import ExchangeRateSerializer
from .models import ExchangeRate
def load_exchange_rates():
    print('로딩레쓰고')
    queryset = ExchangeRate.objects.all()
    print('환율모델 싹가져와:', queryset)
    
    # 데이터 직렬화
    serializer = ExchangeRateSerializer(queryset, many=True)
    print('씨리얼라이저만들었써')
    
    # DataFrame 생성
    df = pd.DataFrame(serializer.data)
    print('DataFrame:', df.columns)  # 컬럼 확인
    
    # 날짜 형식 변환
    df['date'] = pd.to_datetime(df['date'])
    
    # deal_bas_r을 float으로 변환 (문자열 -> float)
    df['deal_bas_r'] = df['deal_bas_r'].replace({',': ''}, regex=True).astype(float)
    
    # 결과 출력
    print('변환된 DataFrame:', df.head())  # 상위 5개 행 확인
    return df

import matplotlib
matplotlib.use('Agg') 
import matplotlib.pyplot as plt
import numpy as np
import io
def plot_histogram(cur_unit, bins=20):
    print('히스토그램그리러왔음', cur_unit)
    
    # 환율 데이터를 로드
    df = load_exchange_rates()
    
    # 상위 5개 확인
    print('상위 다섯개', df.head())
    print('df 열', df.columns)

    # 'cur_unit'의 공백을 제거하고 소문자로 변환하여 필터링
    filtered_df = df[df['cur_unit'].str.strip().str.lower() == cur_unit.strip().lower()]

    if filtered_df.empty:
        print(f"{cur_unit}에 대한 데이터가 없습니다.")
        return None  # 데이터가 없으면 None 반환
    
        # 날짜를 datetime 형식으로 변환
    filtered_df['date'] = pd.to_datetime(filtered_df['date'])
    # 'date'를 x축으로, 'deal_bas_r'를 y축으로 설정
    plt.plot(filtered_df['date'], filtered_df['deal_bas_r'], color='#196DDC', linewidth=2)
    # plt.hist(rates, bins=bins, color='#196DDC', edgecolor='grey')

    # 'deal_bas_r' 열을 사용하여 히스토그램을 그립니다
    # rates = filtered_df['deal_bas_r'].dropna()  # NaN 값을 제외하고 사용
    # plt.hist(rates, bins=bins, color='skyblue')

    plt.title(f'{cur_unit} Exchange Rate over Time')
    plt.xlabel('Date')
    plt.ylabel('Exchange Rate')
    # 이미지를 메모리로 저장
    buf = io.BytesIO()
    plt.xticks(rotation=45)  # x축 레이블이 겹치지 않도록 회전
    plt.tight_layout()  # 그래프 레이아웃 자동 조정
    plt.savefig(buf, format='png')
    buf.seek(0)  # 버퍼의 처음으로 돌아가기
    plt.close('all')  # 그래프 닫기
    
    return buf  # 이미지 데이터를 반환


@api_view(['POST'])
def request_currency(request):
    cur_unit = request.data.get('cur_unit')
    print('통화', cur_unit)
    if not cur_unit:
        return Response({"error": "통화명을 전달해 주세요."}, status=status.HTTP_400_BAD_REQUEST)
    
    # 환율 데이터가 없는 경우 자동으로 저장
    if not ExchangeRate.objects.exists():
        save_exchange_rates()

    # 히스토그램을 그립니다
    histogram_image = plot_histogram(cur_unit, bins=20)

    if histogram_image is None:
        return Response({"error": f"{cur_unit}에 대한 데이터가 없습니다."}, status=status.HTTP_404_NOT_FOUND)

    # 이미지를 base64로 인코딩
    encoded_image = base64.b64encode(histogram_image.getvalue()).decode('utf-8')

    return Response({"histogram": encoded_image}, status=status.HTTP_200_OK)




# 상수 정의: Type 모델의 유형값
INCOME_TYPE = "1"  # 수익
EXPENSES_TYPE = "2"  # 지출
SAVINGS_TYPE = "3"  # 저축


# 상수 정의: Type 모델의 유형값
INCOME_TYPE = "1"  # 수익
EXPENSES_TYPE = "2"  # 지출
SAVINGS_TYPE = "3"  # 저축


# 자산관리 유형검사
@api_view(['GET'])
@permission_classes([IsAuthenticated]) # 인증된 사용자만 접근 가능
def asset_type(request):
    user = request.user
    print(user)
    # 1. 고객 계좌와 연결된 이체 데이터 가져오기
    accounts = user.bankaccount_set.all()  # 현재 사용자와 연결된 계좌들
    payments = Payment.objects.filter(account_pk__in=accounts)

    # 2. 3개월 이체 내역 필터링 
    three_months_ago = timezone.now() - timedelta(days=90)  
    recent_payments = payments.filter(payment_date__gte=three_months_ago)

    # 3. 전체 평균 데이터 계산 
    total_payments = Payment.objects.filter(payment_date__gte=three_months_ago)

    # 해당 고객의 데이터
    customer_data = {
        "income": recent_payments.filter(type_pk__type=INCOME_TYPE).aggregate(Sum("money"))["money__sum"] or 0,
        "expenses": recent_payments.filter(type_pk__type=EXPENSES_TYPE).aggregate(Sum("money"))["money__sum"] or 0,
        "savings": recent_payments.filter(type_pk__type=SAVINGS_TYPE).aggregate(Sum("money"))["money__sum"] or 0,
    }

    # 전체 고객의 데이터
    peer_data = {
        "income": total_payments.filter(type_pk__type=INCOME_TYPE).aggregate(Avg("money"))["money__avg"] or 0,
        "expenses": total_payments.filter(type_pk__type=EXPENSES_TYPE).aggregate(Avg("money"))["money__avg"] or 0,
        "savings": total_payments.filter(type_pk__type=SAVINGS_TYPE).aggregate(Avg("money"))["money__avg"] or 0,
    }

    # 자산관리 유형
    asset_types = "\n".join([f"- {asset.title}: {asset.description}" for asset in Asset_type.objects.all()])

    # 4. ChatGPT 요청 데이터 준비
    prompt = f"""
    고객의 자산관리 유형을 분석하세요.

    고객 3개월 평균:
    - 지출: {customer_data['expenses']}
    - 수익: {customer_data['income']}
    - 저축: {customer_data['savings']}

    동일 연령대 평균:
    - 지출: {peer_data['expenses']}
    - 수익: {peer_data['income']}
    - 저축: {peer_data['savings']}

    자산관리 유형 기준:{asset_types}
    

    대답 예시:
    {{"type": 1,
     "customer_avg_expenses": 1000000,
     "customer_avg_income": 1000000,
     "customer_avg_savings": 1000000,
     "peer_avg_expenses": 1000000,
     "peer_avg_income": 1000000,
     "peer_avg_savings": 1000000}}

    참고: 
        type은 자산관리 유형 기준{asset_types}의 id 를 뜻함 해당 고객에 알맞은 타입을 출력
        customer_avg_expensesd은 해당 고객의 평균지출을 뜻함
        customer_avg_income 해당 고객의 평균 수익을 뜻함
        customer_avg_savings 해당 고객의 평균지출을 뜻함
        peer_avg_expenses 전체 고객의 평균지출을 뜻함
        peer_avg_income 전체 고객의 평균지출을 뜻함
        peer_avg_savings 전체 고객의 평균지출을 뜻함

    
    """
    # OpenAI API 호출 및 응답 처리
    try:
        openai.api_key = settings.ASSAET_API_KEY
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a financial advisor."},
                {"role": "user", "content": prompt},
            ],
        )
        result = response['choices'][0]['message']['content']

        # ChatGPT의 응답을 JSON으로 변환
        import json
        try:
            result_json = json.loads(result)  # JSON으로 변환
        except json.JSONDecodeError:
            return JsonResponse({"error": "ChatGPT 응답이 유효한 JSON 형식이 아닙니다.", "raw_result": result}, status=400)

        # Asset_type 데이터 추가
        asset_type_id = result_json.get("type")
        asset_type = get_object_or_404(Asset_type, id=asset_type_id)

        user.asset_type = asset_type
        user.save()

        # JSON 응답 데이터 재구성
        enriched_result = {
            "analysis": {
                "type": {
                    "title": asset_type.title,
                    "description": asset_type.description,
                },
                "customer_avg_expenses": result_json["customer_avg_expenses"],
                "customer_avg_income": result_json["customer_avg_income"],
                "customer_avg_savings": result_json["customer_avg_savings"],
                "peer_avg_expenses": result_json["peer_avg_expenses"],
                "peer_avg_income": result_json["peer_avg_income"],
                "peer_avg_savings": result_json["peer_avg_savings"],
            }
        }

    except openai.OpenAIError as e:
        print(f"Error in asset_type view: {str(e)}")  # 서버 로그에 에러 출력
        return JsonResponse({"error": f"OpenAI API 호출 중 오류가 발생했습니다: {str(e)}"}, status=500)

    # 최종 결과 반환
    return JsonResponse(enriched_result, status=200)





import json
@api_view(['POST'])
@permission_classes([IsAuthenticated]) # 인증된 사용자만 접근 가능
def recommend(request):
    asset_type = request.data.get('assetType')
    print('자산관리 유형', asset_type)

    if not asset_type:
        return Response({"error": "자산관리 유형 정보가 필요합니다."}, status=400)

    products = Product.objects.all().prefetch_related('rates')
     # 3. 상품 목록 문자열 생성
    products_str = "다음은 사용할 수 있는 금융 상품 목록입니다:\n\n"
    
    for product in products:
        # rates를 사용하여 최대 금리와 기간 계산
        max_interest = product.rates.aggregate(Max('intr_rate'))['intr_rate__max'] or 0
        max_period = product.rates.aggregate(Max('save_trm'))['save_trm__max'] or 0
        
        products_str += f"상품명: {product.fin_prdt_nm}\n"
        products_str += f"상품 설명: {product.etc_note}\n"
        products_str += f"상품 타입: {product.type}\n"
        products_str += f"최대 금리: {max_interest}%\n"
        products_str += f"최대 가입기간: {max_period}개월\n\n"




     # 4. GPT API 호출을 위한 프롬프트 구성
    prompt = f"""
    사용자의 자산관리 유형 분석 결과:
    유형: {asset_type['type']['title']}
    설명: {asset_type['type']['description']}
    고객 평균 지출: {asset_type['customer_avg_expenses']}
    고객 평균 수입: {asset_type['customer_avg_income']}
    고객 평균 저축: {asset_type['customer_avg_savings']}
    
    {products_str}
    
    위 정보를 바탕으로 이 사용자에게 가장 적합한 상품 타입이 1인 상품 1개, 예금 상품 1개를 추천해주세요.
    반드시 다음 JSON 형식으로 답변해주세요:
    
    
    {{
        "recommendations": [
            {{
                "product_name": "상품명",
                "explanation": "추천 이유 설명",
                "max_interest": "최대 금리",
                "max_period": "최대 가입기간"
            }},
            {{
                "product_name": "상품명",
                "explanation": "추천 이유 설명",
                "max_interest": "최대 금리",
                "max_period": "최대 가입기간"
            }},
            {{
                "product_name": "상품명",
                "explanation": "추천 이유 설명",
                "max_interest": "최대 금리",
                "max_period": "최대 가입기간"
            }}
        ]
    }}
    """

    try:
        # 5. GPT API 호출
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "당신은 금융 상품 추천 전문가입니다. 요청된 JSON 형식을 정확히 지켜서 답변해주세요."},
                {"role": "user", "content": prompt}
            ]
        )
        
        # JSON 형식으로 파싱
        recommendation = json.loads(response.choices[0].message.content)

        return Response(recommendation)

    except Exception as e:
        return Response({
            'error': str(e)
        }, status=500)
    



