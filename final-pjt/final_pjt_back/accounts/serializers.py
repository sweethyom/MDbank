from .models import Member, OldAccount
from rest_framework import serializers
from django.contrib.auth import get_user_model
from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import LoginSerializer, UserDetailsSerializer



# Registerserializer: 회원가입 시 사용되는 serializer
# >> 이 serializer를 커스터마이징한다!!
class CustomRegisterSerializer(RegisterSerializer):
    first_name = serializers.CharField(required=True, max_length=150)
    last_name= serializers.CharField(required=False, max_length=150)
    address= serializers.CharField(required=True, max_length=200) 
    address_detail= serializers.CharField(max_length=200)
    tel= serializers.CharField(required=True,max_length=13)
    old_account= serializers.CharField(required=True, max_length=20)
    birth = serializers.DateField(required=True)

    #기본적인 username, password1, password2 만 저장 
    def get_cleaned_data(self):
        cleaned_data = super().get_cleaned_data()
        return cleaned_data
    
    # 추가 필드 저장
    def save(self, request):
            # 아이디 중복 체크
            username=self.validated_data.get('username')
            if Member.objects.filter(username=username).exists():
                 raise serializers.ValidationError({"username":"이미 존재하는 아이디입니다."})
            
            old_account_num = self.validated_data.get('old_account')
            old_account_instance = OldAccount.objects.filter(account_num=old_account_num).first()
            if not old_account_instance:
                raise serializers.ValidationError({"old_account": "등록된 계좌가 아닙니다. 계좌 등록을 먼저 해주세요."})
            # old_account_num = OldAccount.objects.get(account_num=self.validated_data.get('old_account'))  # get으로 해서 단일 객체로 반환해야함 (filter 하면 쿼리셋 객체 반환해서 ValueError남)
            if old_account_num:
                user = super().save(request)  # 기본 사용자 저장 로직 실행
                user.first_name = self.validated_data.get('first_name', '')
                user.last_name = self.validated_data.get('last_name', '')
                user.address = self.validated_data.get('address', '')
                user.address_detail = self.validated_data.get('address_detail', '')
                user.tel = self.validated_data.get('tel', '')
                user.old_account = self.validated_data.get('old_account', '')
                user.old_account= old_account_num
                user.save()  # 변경 사항 저장

                # # OldAccount의 sign_in 을 ture로 바꾸기
                old_account_num.sign_in = True
                old_account_num.save()

                return user
            else:
                raise serializers.ValidationError({"old_account": "등록된 계좌가 아닙니다. 계좌 등록을 먼저 해주세요"})


class MemberSerializers(serializers.ModelSerializer):
     class Meta:
          model = Member
          fields = ['username', 'email', 'is_superuser', 'is_staff', 'first_name', 'last_name', 'address', 'tel', 'birth', 'old_account']


# # 회원정보수정
# class CustomChangeSerializer(UserDetailsSerializer):
#     class Meta:
#          model = Member
#          fields = ['email', 'address', 'address_detail', 'tel']
#     # email=serializers.EmailField(max_length=255)
#     # address= serializers.CharField(required=True, max_length=200) 
#     # address_detail= serializers.CharField(max_length=200)
#     # tel= serializers.CharField(required=True,max_length=13)

#     # 추가 필드 저장
#     def save(self, request):
#         user = request.user
#         user.email = self.validated_data.get('email', user.email)
#         user.address = self.validated_data.get('address', user.address)
#         user.address_detail = self.validated_data.get('address_detail', user.address_detail)
#         user.tel = self.validated_data.get('tel', user.tel)
#         user.save()  # 변경 사항 저장
#         return user
