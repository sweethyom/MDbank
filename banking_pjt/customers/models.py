from django.db import models

# 공지사항
class Information(models.Model):
    title=models.CharField(max_length=50)
    member_pk=models.ForeignKey("member", on_delete=models.CASCADE)
    content=models.TextField()
    img_path=models.CharField(max_length=255)
    img_file=models.FileField(upload_to=None, max_length=100)
    file=models.FileField(upload_to=None, max_length=100)
    

# 문의하기
class Question(models.Model):
    member_pk=models.ForeignKey("member", on_delete=models.CASCADE)
    title=models.CharField( max_length=50)
    content=models.TextField()
    private
    공개/비공개 
    create_date
    update_date

# 답변하기


# FAQ
class Faq(models.Model):
    member_pk=models.ForeignKey("member", on_delete=models.CASCADE)
    question=models.CharField( max_length=200)
    answer=models.TextField()