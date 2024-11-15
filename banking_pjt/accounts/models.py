from django.db import models
from products.models import Asset_type
# Create your models here.
class Member(models.Model):
    member_id=models.CharField(max_length=30)
    member_name=models.CharField(max_length=30)
    email = models.CharField(max_length=100)
    password=models.CharField(max_length=30, min_length=8)
    address=models.CharField(max_length=200) 
    address_detail=models.CharField(max_length=200) 
    tel=models.CharField(max_length=13)
    old_account_pk=models.ForeignKey("OldAccount", on_delete=models.CASCADE)
    sign_out=models.BooleanField()
    member_authorization=models.BooleanField()
    asset_type=models.ForeignKey(Asset_type, on_delete=models.CASCADE)

class OldAccount(models.Model):
    account_num=models.CharField(max_length=20)
    customer_name=models.CharField(max_length=30)
    join_date=models.DateField(auto_now_add=True)
    sing_in=models.BooleanField()