from django.db import models

# Create your models here.

# 입출금분류
class type(models.Model):
    type=models.IntegerField()

# 계좌 정보
class bank_account(models.Model):
    account_num=models.CharField(max_length=16)
    account_name=models.CharField(max_length=10)
    product_pk=models.ForeignKey("product_info", on_delete=models.CASCADE)
    member_pk=models.ForeignKey("memeber", on_delete=models.CASCADE)
    balance=models.IntegerField()
    join_date=models.DateField(auto_now_add=True)
    expire_date=models.DateField()

# 계좌이체 내역
class payment(models.Model):
    account_pk=models.ForeignKey("bank_account", on_delete=models.CASCADE)
    ## 다른 은행일 경우에는 fk 가 아닐듯 합니다..
    transaction_pk=models.ForeignKey("bank_account", on_delete=models.CASCADE)
    type_pk=models.ForeignKey("type", on_delete=models.CASCADE)
    bank=models.CharField(max_length=10)
    payment_memo=models.CharField(max_length=100)
    payment_date=models.DateTimeField(auto_now_add=True)

# 수신자 즐겨찾기
class favorites(models.Model):
    ## 수신자가 다른 은행일수 있음
    member_pk=models.ForeignKey("memeber", on_delete=models.CASCADE)
    recipient=models.CharField(max_length=20)
    recipient_name=models.CharField(max_length=10)
    bank=models.CharField(max_length=20)






    