from django.db import models
from accounts.models import Member
from django.db import models
from datetime import timedelta, date

# 상품 정보
class Product(models.Model):
    name=models.CharField(max_length=10)    # 상품 이름
    description=models.TextField()          # 상품 설명
    rate=models.FloatField()                # 금리
    superior_rate=models.FloatField()       # 우대금리
    period=models.IntegerField()            # 가입 기간
    limit_age=models.IntegerField()         # 가입대상
    limit_amount=models.IntegerField()      # 최소가입금액

    #금리 옵션관리

# 자산관리
class Asset_type(models.Model):
    title=models.CharField(max_length=20)
    description=models.TextField() 

def default_end_date():
    return date.today() - timedelta(days=90)

# 분석결과 api 가져오고나서 구체화
class analysis(models.Model):
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
