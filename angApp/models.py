from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.

User = get_user_model()
   




class Category(models.Model):
    category_name = models.CharField(max_length=100)
    slug = models.CharField(max_length=255 , blank=True , null=True)
    slug_url = models.CharField(max_length=255, blank=True , null=True)
    meta_title = models.CharField(max_length=255 , blank=True , null=True)
    meta_description = models.TextField(blank=True , null=True)
    parent = models.IntegerField(max_length=100 , default=0 , db_column="parent_id")
    deleted = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add = True ,db_column="created_at")
    updated = models.DateTimeField(auto_now = True , db_column="updated_at")

    class Meta:
        managed = True,
        db_table = "tbl_category"

    def __str__(self):
        return self.category_name


class UserInfoDetails(models.Model):
    employee_type = (
        (1,'super_admin'),
        (2 , 'admin'),
        (3, 'manager'),
        (4 , 'report_handler'),
        (5 , 'sales_manager'),
        (6, 'user'),
    )
    employee = models.CharField(max_length = 255 , unique=True , default="EMP-001",db_column="employee_id",null=True)
    user = models.OneToOneField(User , related_name="user_info",on_delete=models.DO_NOTHING)
    designation = models.CharField(max_length=255,blank=True,null=True)
    address = models.TextField(blank=True , null=True)
    user_role=models.IntegerField(choices = employee_type , default=6)
    gender = models.CharField(max_length = 10 , null=True)
    country_code = models.CharField(max_length=3 , blank=True , null=True)
    mobile_no = models.CharField(max_length=13, blank=True,null=True)
    dob = models.DateField()
    doj = models.DateField()
    experience = models.FloatField(db_column='yers_exper' , default=0.0)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    class Meta:
        managed= True
        db_table="tbl_user_details"

    def __str__(self):
        return f"{self.user.username}"  

