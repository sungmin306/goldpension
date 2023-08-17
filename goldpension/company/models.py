from django.db import models
from django.conf import settings

# Create your models here.

class Job(models.Model):

    id = models.AutoField(primary_key=True, null=False, blank=False) # pk
    company_name = models.CharField(max_length=50, null=False, blank=False)# 회사명
    company_number = models.CharField(max_length=50,null=False,blank=False)# 사업자 등록번호
    company_address = models.CharField(max_length=50, null=False, blank=False) # 회사 주소
    company_call = models.CharField(max_length=50, null=False, blank=False)# 회사 연락처
    company_boss = models.CharField(max_length=10, null=False, blank=False)# 대표자 명
    company_size = models.CharField(max_length=50,null=True, blank=True)# 직원수
    company_homepage = models.CharField(max_length = 50, null=True, blank=True)# 홈페이지
    company_logo = models.CharField(max_length=50,null=True, blank=True)# 회사로고

    work_place = models.CharField(max_length = 50, null=False, blank=False) #근무지
    work_day = models.CharField(max_length= 50, null=False, blank=False ) #근무요일
    work_hour = models.CharField(max_length = 20, null = False, blank=False) #근무시간
    work_pay = models.CharField(max_length = 10, null = False, blank=False) # 급여
    work_term = models.CharField(max_length=20, null=True, blank=True)#근무기간
    work_experience = models.CharField(max_length=10, null=True, blank=True) #희망경력

    apply_num = models.CharField(max_length=50,null = False, blank = False)# 모집인원
    apply_deadline = models.CharField(max_length=20, null = False, blank = False) # 모집종료일
    apply_sex = models.CharField(max_length= 10, null = False, blank=False)# 성별
    apply_age = models.CharField(max_length=50,null = False, blank= False)# 연령
    apply_work = models.CharField(max_length=20, null = False, blank= False)# 직종
    apply_detail = models.CharField(max_length=20, null= False, blank= False) # 업무내용

    


