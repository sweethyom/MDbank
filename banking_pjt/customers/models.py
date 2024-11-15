from django.db import models
from accounts.models import Member

# 공지사항
class Information(models.Model):
    member_pk=models.ForeignKey(Member, on_delete=models.CASCADE)
    title=models.CharField(max_length=50)
    content=models.TextField()
    img_path=models.CharField(max_length=255)
    img_file=models.FileField(upload_to=None, max_length=100)
    file=models.FileField(upload_to=None, max_length=100)
    

# 문의하기
class Question(models.Model):
    member_pk=models.ForeignKey(Member, on_delete=models.CASCADE)
    title=models.CharField( max_length=50)
    content=models.TextField()
    private = models.BooleanField 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

# 답변하기
class Answer(models.Model):
    question_pk = models.ForeignKey(Question, on_delete=models.CASCADE)
    member_pk=models.ForeignKey(Member, on_delete=models.CASCADE)
    private = models.ForeignKey(Question, on_delete=models.CASCADE)
    content=models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

# FAQ
class Faq(models.Model):
    member_pk=models.ForeignKey(Member, on_delete=models.CASCADE)
    question=models.CharField( max_length=200)
    answer=models.TextField()