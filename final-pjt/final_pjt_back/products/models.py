from django.db import models
from accounts.models import Member
from django.utils import timezone
from datetime import timedelta

# 상품 정보
class Product(models.Model):
    type=models.IntegerField()                      # 상품 타입 ( 1: 예금, 2: 적금 3:입출금)
    dcls_month=models.CharField(max_length=50)      # 공시 제출월
    fin_co_no=models.CharField(max_length=20)         # 금융회사 코드
    fin_prdt_cd=models.CharField(max_length=50)     # 금융 회사 명
    kor_co_nm=models.CharField(max_length=50)       # 금융 상품 코드
    fin_prdt_nm=models.TextField()                  # 상품 이름
    join_way=models.CharField(max_length=50)        # 가입 방법
    mtrt_int=models.TextField()                     # 만기 후 이자율
    spcl_cnd=models.TextField()                     # 우대 조건
    join_deny=models.CharField(max_length=2)        # 가입 제한
    join_member=models.TextField()                  # 가입 대상
    etc_note=models.TextField()                     # 기타 유의 사항
    max_limit=models.IntegerField()                 # 최고 한도
    dcls_strt_day=models.CharField(max_length=50)   # 공시 시작일
    dcls_end_day=models.CharField(max_length=50, null=True)    # 공시 종료일
    fin_co_subm_day=models.CharField(max_length=50) # 금융회사 제출일
    description=models.TextField(null=True, blank=True)


#금리 옵션관리
class Option(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='rates')  # 제품 pk
    dcls_month=models.CharField(max_length=20)                      # 공시 제출일
    fin_co_no=models.CharField(max_length=20)                       # 금융회사 코드
    fin_prdt_cd=models.CharField(max_length=50)                     # 금융 상품 코드
    intr_rate_type=models.CharField(max_length=50)                  # 저축 금리 유형
    intr_rate_type_nm=models.CharField(max_length=50)               # 저축 금리 유형명
    rsrv_type=models.CharField(max_length=50, null=True)           # 적립 유형, 적금 옵션에만 있음 (예금일 경우 공백)
    rsrv_type_nm=models.CharField(max_length=50, null=True)        # 적립 유형명
    save_trm=models.CharField(max_length=20)                        # 가입 기간
    intr_rate=models.FloatField()                                   # 금리
    intr_rate2=models.FloatField()                                  # 우대금리

# 자산관리
class Asset_type(models.Model):
    title=models.CharField(max_length=20)
    description=models.TextField() 

def default_end_date():
    # timezone-aware한 날짜 반환
    return (timezone.now() - timedelta(days=90)).date()

# 분석결과 api 가져오고나서 구체화
class Analysis(models.Model):
    member_pk=models.ForeignKey(Member, on_delete=models.CASCADE)
    avg_deposit = models.FloatField()
    avg_withdraw = models.FloatField()
    avg_save = models.FloatField()
    sum_deposit = models.IntegerField()
    sum_withdraw = models.IntegerField()
    sumSave = models.IntegerField()
    # 저축 비율
    savings_rate=models.IntegerField()      # 저축/입금 비율
    # 지출 비율
    expense_rate=models.IntegerField()      # 출금/입금 비율
    content = models.TextField()
    # 시작날짜에서 3개월 전 데이터까지만 분석
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(default=default_end_date)

class ExchangeRate(models.Model):
    date = models.CharField(max_length=10)
    cur_unit= models.CharField(max_length=10)
    ttb = models.CharField(max_length=10)       # 송금받을때
    tts= models.CharField(max_length=10)        # 송금보을때
    deal_bas_r= models.CharField(max_length=10) # 매매기준율
    bkpr= models.CharField(max_length=10)
    yy_efee_r= models.CharField(max_length=10)
    ten_dd_efee_r= models.CharField(max_length=10)
    kftc_bkpr= models.CharField(max_length=10)
    kftc_deal_bas_r= models.CharField(max_length=10)
    cur_nm= models.CharField(max_length=30)
    
    def __str__(self):
        return f"{self.date} - {self.cur_nm}: {self.deal_bas_r}"