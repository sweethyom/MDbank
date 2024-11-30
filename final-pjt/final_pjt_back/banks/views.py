from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import Favorites, Bank
from rest_framework.response import Response
from rest_framework import status
from .serializers import BankSerializers, FavoritesSerializers
# Create your views here.

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_banks(request):
    banks = Bank.objects.all().order_by('name')
    serializer = BankSerializers(banks, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_favorites(request):
    favorites = Favorites.objects.filter(member_pk=request.user)
    serializer = FavoritesSerializers(favorites, many=True)

    data= serializer.data
    for item in data:
        bank = Bank.objects.get(id=item['bank'])
        item['bank_name'] = bank.name
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_favorites(request): 
    serializer = FavoritesSerializers(data=request.data)
    if serializer.is_valid():
        serializer.save(member_pk=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_favorites(request, favorite_pk):

    favorite = Favorites.objects.get(pk=favorite_pk)
    if favorite.member_pk.id == request.user.id:  # id값으로 비교
        serializer = FavoritesSerializers(favorite, data=request.data)
        if serializer.is_valid():
            serializer.save(member_pk=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    return Response(
            {"detail": "Favorite not found."}, 
            status=status.HTTP_404_NOT_FOUND )
        

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_favorites(request, favorite_pk):
    favorite = Favorites.objects.get(pk = favorite_pk)
    if favorite.member_pk == request.user:
        favorite.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(status=status.HTTP_400_BAD_REQUEST)
