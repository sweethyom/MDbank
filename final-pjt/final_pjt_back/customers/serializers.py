from .models import Question, Answer, Category
from accounts.models import Member
from rest_framework import serializers

# 문의하기 POST, PUT
class QuestionSerializers(serializers.ModelSerializer):
    class Meta:
        model = Question
        exclude = ('member_pk', 'created_at', 'updated_at', 'answer')

    def validate(self, data):
        # private이 True인데 password가 없는 경우
        if data.get('private', False) and not data.get('password'):
            raise serializers.ValidationError({
                'password': '비공개 글은 비밀번호가 필수입니다.'
            })
        
        # private이 False인 경우 password를 None으로 설정
        if not data.get('private', False):
            data['password'] = None
            
        return data

# 문의리스트, 디테일 GET
class QuestionListSerializers(serializers.ModelSerializer):
    username = serializers.CharField(source='member_pk.username', read_only=True)
    answer_status = serializers.SerializerMethodField()
    isprivate = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    password = serializers.IntegerField(required=False)  # password를 필수가 아닌 필드로 설정

    def get_category(self, obj):
        return obj.category.category

    def get_answer_status(self, obj):
        return "답변완료" if obj.answer else "답변대기"
    
    def get_isprivate(self, obj):
        return "비공개" if obj.private else "공개"
    
    def validate(self, data):
        # private이 True인데 password가 없는 경우
        if data.get('private', False) and not data.get('password'):
            raise serializers.ValidationError({
                'password': '비공개 글은 비밀번호가 필수입니다.'
            })
        
        # private이 False인 경우 password를 None으로 설정
        if not data.get('private', False):
            data['password'] = None
            
        return data
    
    class Meta:
        model = Question
        fields = ['id', 'title', 'password', 'content', 'private', 'created_at', 
                 'updated_at', 'username', 'category', 'answer', 'answer_status', 
                 'isprivate', 'category']

# 댓글 달기          
class AnswerSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='member_pk.username', read_only=True)

    class Meta:
        model = Answer
        fields = ['id', 'content', 'created_at', 'updated_at', 'username', 'private']
        read_only_fields = ['member_pk', 'question_pk', 'private']  # 자동으로 설정되는 필드들

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields ='__all__'