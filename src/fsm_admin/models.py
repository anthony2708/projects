from django.db import models
from django.db.models.fields import CharField

# Create your models here.

class GIAIDAU(models.Model):
    ma_giaidau = models.CharField(primary_key=True, max_length=10, null=False)
    ten_giaidau = models.CharField(max_length=50, null=False)
    sodoi_thamdu = models.IntegerField(null=False)
    thethuc = models.CharField(max_length=50, null=False)
    luatuoi = models.IntegerField(null=False)
    lephi = models.IntegerField(null=False)
    loaisan = models.IntegerField(null=False)
    chedo = models.IntegerField(null=False)
    trangthai = models.CharField(max_length=50, null=False)

    def __str__(self):
        return '%s' % (self.ten_giaidau)
