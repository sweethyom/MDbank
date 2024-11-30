from django.shortcuts import render
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Question, Answer, Category
from accounts.models import Member
from .serializers import QuestionSerializers, QuestionListSerializers, AnswerSerializer, CategorySerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework import status



# 문의 전체 리스트
@api_view(['GET'])
def questions_list(request):

    questions= Question.objects.all()
    
    serializer= QuestionListSerializers(questions, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)


# 카테고리 
@api_view(['GET'])
def get_category(request):
    category = Category.objects.all()
    serializer = CategorySerializer(category, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def question_detail(request, question_pk):
    print(f"상세 조회 요청: question_pk = {question_pk}")  # 디버깅용
    try:
        question = Question.objects.get(pk=question_pk)
        serializer = QuestionListSerializers(question)
        return Response(serializer.data)
    except Question.DoesNotExist:
        return Response(
            {'error': f'Question with id {question_pk} not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )

# 문의하기 POST
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def question_create(request):
    print("받은 데이터:", request.data)  # 디버깅용
    
    serializer = QuestionSerializers(data=request.data)
    if serializer.is_valid():
        serializer.save(member_pk=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    print("유효성 검사 에러:", serializer.errors)  # 디버깅용
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 문의 수정
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def question_update(request, question_pk):
    try:
        # 요청 데이터 출력
        print("Received data:", request.data)
        
        question = Question.objects.get(pk=question_pk)
        serializer = QuestionSerializers(question, data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            # 유효성 검사 실패 시 상세 에러 출력
            print("Validation errors:", serializer.errors)
            return Response(
                {
                    'error': 'Validation failed',
                    'details': serializer.errors
                }, 
                status=status.HTTP_400_BAD_REQUEST
            )
    except Question.DoesNotExist:
        return Response(
            {'error': f'Question with id {question_pk} not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )

#문의 삭제
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def question_delete(request, question_pk):
    question=Question.objects.get(pk=question_pk)
    question.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


## 댓글 생성
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_answer(request, question_pk):
    print(request.data)
    try:
        
        question = Question.objects.get(pk=question_pk)
        serializer = AnswerSerializer(data=request.data)
        
        if serializer.is_valid():
            answer = serializer.save(
                member_pk=request.user,
                question_pk_id=question.pk,
                private=question.private
            )
            
            question.answer = answer
            question.save()
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
    except Question.DoesNotExist:
        return Response({'error': 'Question not found'}, status=status.HTTP_404_NOT_FOUND)


  # 댓글 조회  
@api_view(['GET'])
def get_answer(request, question_pk):
    try:
        question = Question.objects.get(pk=question_pk)
        answer = Answer.objects.filter(question_pk=question).first()
        
        if answer:
            serializer = AnswerSerializer(answer)
            return Response(serializer.data)
        else:
            return Response(None, status=status.HTTP_204_NO_CONTENT)
            
    except Question.DoesNotExist:
        return Response(
            {'error': 'Question not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    
