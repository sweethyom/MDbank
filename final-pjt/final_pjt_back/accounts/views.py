from django.shortcuts import get_object_or_404
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Member, OldAccount
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import Member
from products.models import Asset_type
from banks.models import BankAccount, Favorites, Bank  
from .serializers import MemberSerializers
from banks.serializers import BankAccountSerializers, FavoritesSerializers, BankSerializers
from products.serializers import AssetTypeSerializer
from django.http import JsonResponse 
from rest_framework.views import APIView
# from .serializers import CustomChangeSerializer


from django.contrib.auth import authenticate
# from django.contrib.auth.models import update_last_login

# Create your views here.
@api_view(['GET'])
@permission_classes([IsAuthenticated])   
def profile(request):
    print("User is_superuser:", request.user.is_superuser)  
    print("User is_staff:", request.user.is_staff)
    
    member = request.user
    member = Member.objects.get(pk=member.id)
    bank_accounts = BankAccount.objects.filter(member_pk=member)
    favories = Favorites.objects.filter(member_pk=member)
    banks = Bank.objects.all()
    
    # asset_type 조회 부분 수정
    try:
        asset_type = Asset_type.objects.get(member=member)
        asset_type_serializer = AssetTypeSerializer(asset_type)
        asset_type_data = asset_type_serializer.data
    except Asset_type.DoesNotExist:
        asset_type_data = None

    # 직렬화
    member_serializer = MemberSerializers(member)
    bank_accounts_serializer = BankAccountSerializers(bank_accounts, many=True)
    favories_serializer = FavoritesSerializers(favories, many=True)
    bank_serializer = BankSerializers(banks, many=True)
    
    response_data = {
        'member': member_serializer.data,
        'bank_accounts': bank_accounts_serializer.data,
        'favorites': favories_serializer.data,
        'banks': bank_serializer.data,
        'asset_type': asset_type_data
    }

    return Response(response_data, status=200)

# 유저 정보 받아오기
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_info(request):
      # 인증된 유저 객체
    member = Member.objects.get(pk=request.user.id)
    member_serializer = MemberSerializers(member)
    response_data={
        'member':member_serializer.data
    }
    return Response({'userId': response_data})  # 유저이름반환


@api_view(['POST'])
def signout(request):
    user= request.user
    # 해당하는 회원 찾기
    member = Member.objects.get(pk=user.id)
    # 회원의 정보 수정
    member.sign_out = True  # 값이 true로 안바뀜
    member.save()
    # 토큰만 삭제하고 아이디는 남겨두는 방식으로 간다. 다시는 가입 못하게 
    token = Token.objects.get(user=user)
    token.delete()
    
    return JsonResponse({"회원탈퇴":"성공"})


# class UpdateProfileView(APIView):
#     permission_classes = [IsAuthenticated]  # 인증된 사용자만 접근 가능

#     def put(self, request):
#         user = request.user  # 로그인된 사용자 정보
#         serializer = CustomChangeSerializer(user, data=request.data, partial=True)

#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=400)

    # permission_classes = [IsAuthenticated]

    # def put(self, request, *args, **kwargs):
    #     serializer = CustomChangeSerializer(data=request.data, instance=request.user)
    #     if serializer.is_valid():
    #         serializer.save(request)
    #         return Response()
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)