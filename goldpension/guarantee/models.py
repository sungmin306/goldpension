from django.db import models
from django.conf import settings
# Create your models here.

class Gcompany(models.Model):
    id = models.AutoField(primary_key=True, null=False, blank=False) # pk
    name = models.CharField(max_length=10, null=False, blank=False) # 이름
    age = models.CharField(max_length=50,null=False, blank=False) # 나이
    phone_number = models.CharField(max_length=20, null=False, blank=False) # 전화번호
    gender = models.CharField(max_length=10, null=False, blank=False) # 성별
    searching = models.CharField(max_length=10, null=True, blank=True) # 구인상태
    apply_detail =models.CharField(max_length=10, null=False, blank=False) #직종
    company_name = models.CharField(max_length=10, null=False, blank=False) #기업
    work_place = models.CharField(max_length=10, null=False, blank=False) #근무지역