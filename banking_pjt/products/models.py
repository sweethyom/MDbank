from django.db import models

# 상품 정보
class product_info(models.Modle):
    name=models.CharField(max_length=10)    # 상품 이름
    description=models.TextField()          # 상품 설명
    rate=models.FloatField()                # 금리
    superior_rate=models.FloatField()       # 우대금리
    period=models.IntegerField()            # 가입 기간
    limit_age=models.IntegerField()         # 가입대상
    limit_amount=models.IntegerField()      # 최소가입금액

# 자산관리
class asset_type(models.Modle):
    title=models.CharField(max_length=20)
    description=models.TextField() 