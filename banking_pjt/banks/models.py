from django.db import models
from products.models import Product
from accounts.models import Member
# Create your models here.

# 입출금분류
class Type(models.Model):
    type=models.IntegerField()

# 계좌 정보(회원가입한 사람들의 계좌만)
class BankAccount(models.Model):
    account_num=models.CharField(max_length=20)
    account_name=models.CharField(max_length=10)
    product_pk=models.ForeignKey(Product, on_delete=models.CASCADE)
    member_pk=models.ForeignKey(Member, on_delete=models.CASCADE)
    balance=models.IntegerField()
    join_date=models.DateField(auto_now_add=False)
    expire_date=models.DateField()

# 계좌이체 내역
class Payment(models.Model):
    account_pk=models.ForeignKey(BankAccount, on_delete=models.CASCADE)
    recipient=models.CharField(max_length=20)
    recipient_name=models.CharField(max_length=30)
    type_pk=models.ForeignKey(Type, on_delete=models.CASCADE)
    bank=models.ForeignKey("Bank", on_delete=models.CASCADE)
    payment_memo=models.CharField(max_length=100)
    payment_date=models.DateTimeField(auto_now_add=True)
    after_balance=models.IntegerField()

# 수신자 즐겨찾기
class Favorites(models.Model):
    ## 수신자가 다른 은행일수 있음
    member_pk=models.ForeignKey(Member, on_delete=models.CASCADE)
    recipient=models.CharField(max_length=20)     ## 수신자 계좌번호
    recipient_name=models.CharField(max_length=30)
    bank=models.ForeignKey("Bank", on_delete=models.CASCADE)

# 은행명
class Bank(models.Model):
    name=models.CharField(max_length=10)


