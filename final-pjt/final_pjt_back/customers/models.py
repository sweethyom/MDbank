from django.db import models
from accounts.models import Member
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError


# 공지사항
class Information(models.Model):
    member_pk=models.ForeignKey(Member, on_delete=models.CASCADE)
    title=models.CharField(max_length=50)
    content=models.TextField()
    img_path=models.CharField(max_length=255)
    img_file=models.FileField(upload_to=None, max_length=100)
    file=models.FileField(upload_to=None, max_length=100)
    
# 문의하기 카테고리
class Category(models.Model):
    category=models.CharField(max_length=50)

# 문의하기
class Question(models.Model):
    member_pk = models.ForeignKey(Member, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    title = models.CharField(max_length=50)
    content = models.TextField()
    private = models.BooleanField(default=False)  
    password = models.IntegerField(
        validators=[
            MinValueValidator(0000),
            MaxValueValidator(9999)
        ],
        null=True,  # null 허용
        blank=True,  # 빈 값 허용
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    answer = models.ForeignKey('Answer', on_delete=models.CASCADE, related_name='questions', null=True, blank=True)

    def clean(self):
        # private이 True인데 password가 없는 경우 에러 발생
        if self.private and not self.password:
            raise ValidationError({
                'password': '비공개 글은 비밀번호가 필수입니다.'
            })
        
        # private이 False인 경우 password를 None으로 설정
        if not self.private:
            self.password = None

    def save(self, *args, **kwargs):
        self.full_clean()  # validation 실행
        super().save(*args, **kwargs)

# 답변하기
class Answer(models.Model):
    question_pk = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    member_pk=models.ForeignKey(Member, on_delete=models.CASCADE)
    private = models.BooleanField(default=0)
    content=models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


# FAQ
class Faq(models.Model):
    member_pk=models.ForeignKey(Member, on_delete=models.CASCADE)
    question=models.CharField( max_length=200)
    answer=models.TextField()