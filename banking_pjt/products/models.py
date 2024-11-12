from django.db import models
from accounts.models import Member

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


# 분석결과 api 가져오고나서 구체화
class analysis(models.Model):
    member_pk=models.ForeignKey(Member, on_delete=models.CASCADE)
    Asset_type=models.ForeignKey(Asset_type, verbose_name=_(""), on_delete=models.CASCADE)
    

