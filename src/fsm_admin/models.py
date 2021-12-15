from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields import BigAutoField, CharField
from django.contrib.auth.models import User

# Create your models here.


class GIAIDAU(models.Model):
    ma_giaidau = models.BigAutoField(primary_key=True, null=False)
    ten_giaidau = models.CharField(max_length=50, null=False)
    sodoi_thamdu = models.IntegerField(null=False)
    thethuc = models.CharField(max_length=50, null=False)
    luatuoi = models.IntegerField(null=False)
    lephi = models.IntegerField(null=False)
    loaisan = models.IntegerField(null=False)
    chedo = models.IntegerField(null=False)
    trangthai = models.CharField(max_length=50, null=False)
    sodoi_hientai = models.IntegerField(null=False, default=0)

    def __str__(self):
        return '%s' % (self.ten_giaidau)

class DOIBONG(models.Model):
    ma_doibong = models.BigAutoField(primary_key=True, null=False)
    ten_doibong = models.CharField(max_length=50, null=False)
    mauao_chinh = models.CharField(max_length=10, null=False)
    mauao_phu = models.CharField(max_length=10, null=False)
    ten_taikhoan = models.ForeignKey(User, on_delete=CASCADE)
    playing = models.BooleanField(null=False, default='False') # is football team joining a tournament?

class CAUTHU(models.Model):
    ma_cauthu = models.BigAutoField(primary_key=True, null=False)
    ten_cauthu = models.CharField(null=False, max_length=50)
    dotuoi = models.IntegerField(null=False)
    so_ao = models.IntegerField(null=False)
    vitri_thidau = models.CharField(null=False, max_length=20)
    ma_doibong = models.ForeignKey(DOIBONG, on_delete=CASCADE)

class HLVIEN(models.Model):
    ma_hlv = models.BigAutoField(primary_key=True, null=False)
    ten_hlv = models.CharField(max_length=50, null=False)
    ma_doibong = models.ForeignKey(DOIBONG, on_delete=CASCADE)
    vaitro = models.CharField(max_length=20, null=False)

class HAUCAN(models.Model):
    ma_haucan = models.BigAutoField(primary_key=True)
    ten_haucan = models.CharField(max_length=50, null=False)
    ma_doibong = models.ForeignKey(DOIBONG, on_delete=CASCADE)
