from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager  # user를 생성할때 상속하는 클래스
from django.core.validators import MinLengthValidator

# Create your models here.

class OldAccount(models.Model):
    account_num=models.CharField(max_length=20)  #계좌번호
    customer_name=models.CharField(max_length=30) #회원이름
    join_date=models.DateField(auto_now_add=True) 
    sign_in=models.BooleanField(default=False)




class Member(AbstractUser): 
    # email,password =  AbstractUser 에서 제공됨 충될될 가능성으로 인해 주석처리
    email = models.EmailField(max_length=255)  # 캐릭터 필드 >> 이메일 필드로 변경
    # password=models.CharField(max_length=30, validators=[MinLengthValidator(8)])
    address=models.CharField(max_length=200) 
    address_detail=models.CharField(max_length=200) 
    tel=models.CharField(max_length=13)
    # birth=models.DateField()
    # permission 구분하기 
    birth = models.DateField(null=False, blank=False, default='2006-01-01') 
    # old_account_pk=models.ForeignKey('OldAccount', on_delete=models.CASCADE, blank=True, null=True )  # blank=True, null=True추가

    # 관리자계정 만들때는 이거 쓰기
    old_account_pk = models.ForeignKey(
    OldAccount, 
    on_delete=models.SET_NULL, 
    null=True,  # null 허용
    blank=True,  # 빈 값 허용
    default=None  # 기본값 None
    )
    old_account=models.CharField(max_length=20)
    sign_out=models.BooleanField(default=False)  # null=True추가 
    is_staff = models.BooleanField(default=False)      # 관리자 추가
    is_superuser = models.BooleanField(default=False)  # 관리자 추가
    asset_type=models.ForeignKey('products.Asset_type', on_delete=models.CASCADE, null=True, blank=True)  # blank=True, null=True추가




    # USERNAME_FIELD = 'member_id'  # 기본 로그인 필드
    # REQUIRED_FIELDS = ['email', 'address', 'old_account_pk']  # 필수 입력 필드  관리자 계정 만들때는 이거 막기
    
