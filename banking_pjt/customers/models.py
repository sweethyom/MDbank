from django.db import models

# 공지사항
class information(models.Modle):
    title=models.CharField(max_length=50)
    content=models.models.TextField()
    img_path=models.CharField(max_length=255)
    img_file=models.FileField(upload_to=None, max_length=100)

# 문의하기
class question(models.Model):
    member_id=models.ForeignKey("memeber", verbose_name=_(""), on_delete=models.CASCADE)
    title=models.CharField( max_length=50)
    content=models.TextField()

# FAQ
class faq(models.Model):
    question=models.TextField()
    answer=models.TextField()