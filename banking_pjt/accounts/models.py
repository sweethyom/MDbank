from django.db import models

# Create your models here.
class memeber(models.Model):
    member_id=models.CharField(max_length=30)
    member_name=models.CharField(max_length=10)
    email = models.CharField()
    password=models.CharField(max_length=30, min_length=8)
    ## 글자수 길이 어떻게 할지
    address=models.CharField() 
    tel=models.CharField(max_length=13)
    old_account_pk=models.ForeignKey("old_account_list", on_delete=models.CASCADE)
    sign_out=models.BooleanField()
    member_authorization=models.BooleanField()

class old_account_list(models.Model):
    account_num=models.CharField(max_length=20)
    customer_name=models.CharField(max_length=10)
    sing_in=models.BooleanField()