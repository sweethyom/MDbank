from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class CustomAuthenticationBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        User = get_user_model()
        try:
            user = User.objects.get(username=username)
            # 회원탈퇴한 사용자인 경우 로그인 거부
            if user.sign_out:
                return None
            # 비밀번호 확인
            if user.check_password(password) != '0000':
                return user
            return None
        except User.DoesNotExist:
            return None