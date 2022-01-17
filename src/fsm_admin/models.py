# from math import e
# from django.contrib.auth import login
from django.db import models
from django.db.models.deletion import CASCADE, SET_NULL
from django.db.models.fields import BigAutoField, CharField
from django.contrib.auth.models import User
from django.urls import reverse

import random as rd

# Create your models here.


class TAIKHOAN(models.Model):
    ma_taikhoan = models.ForeignKey(User, on_delete=CASCADE)
    hoten = models.CharField(max_length=20, null=False)
    ngaysinh = models.DateField(null=False)
    gioitinh = models.CharField(max_length=5, null=False)
    diachi = models.CharField(max_length=50, null=False)
    so_dienthoai = models.CharField(max_length=15, null=False)


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
    is_arranged = models.BooleanField(null=False, default=False)

    def __str__(self):
        return '%s' % (self.ten_giaidau)

    def get_absolute_url(self):
        return reverse('admin_view_tournament', kwargs={'pk': self.ma_giaidau})

    def get_ds_thamdu(self):
        ds_thamdu = DOIBONG.objects.filter(playin=self.ma_giaidau)
        return ds_thamdu

    def randomly_group_division(self):
        ds_thamdu = self.get_ds_thamdu()
        if self.sodoi_thamdu == 8:  # tour will consist of 2 groups A B
            # random team index to put in group
            list_of_teamindex = rd.sample(range(0, 8), 8)
            for i in range(0, 8):  # create group
                teamindex = list_of_teamindex[i]
                if i <= 3:  # then the team will be set in group A
                    doibong = ds_thamdu[teamindex]
                    xephang = XEPHANG(
                        ma_giaidau=self,
                        ma_doibong=doibong,
                        bangdau='A'
                    )
                    xephang.save()
                elif i >= 4:  # then the team will be set in group B
                    doibong = ds_thamdu[teamindex]
                    xephang = XEPHANG(
                        ma_giaidau=self,
                        ma_doibong=doibong,
                        bangdau='B'
                    )
                    xephang.save()
        elif self.sodoi_thamdu == 16:  # tour will consist of 4 groups A B C D
            # random team index to put in group
            list_of_teamindex = rd.sample(range(0, 16), 16)
            for i in range(0, 16):  # create group
                teamindex = list_of_teamindex[i]
                if i >= 12:  # then the team will be set in group A
                    doibong = ds_thamdu[teamindex]
                    xephang = XEPHANG(
                        ma_giaidau=self,
                        ma_doibong=doibong,
                        bangdau='A'
                    )
                    xephang.save()
                elif i >= 8:  # then the team will be set in group B
                    doibong = ds_thamdu[teamindex]
                    xephang = XEPHANG(
                        ma_giaidau=self,
                        ma_doibong=doibong,
                        bangdau='B'
                    )
                    xephang.save()
                elif i >= 4:  # then the team will be set in group B
                    doibong = ds_thamdu[teamindex]
                    xephang = XEPHANG(
                        ma_giaidau=self,
                        ma_doibong=doibong,
                        bangdau='C'
                    )
                    xephang.save()
                elif i >= 0:  # then the team will be set in group B
                    doibong = ds_thamdu[teamindex]
                    xephang = XEPHANG(
                        ma_giaidau=self,
                        ma_doibong=doibong,
                        bangdau='D'
                    )
                    xephang.save()

    def randomly_matches_gen_in_group(self, bangdau):
        # list of ma_doibong which in group bangdau,ex: bangdau: A, B, C,...
        list_xephang = XEPHANG.objects.filter(
            ma_giaidau=self.ma_giaidau, bangdau=bangdau)
        list_team_in_group = []
        for xh in list_xephang:
            ma_doibong = xh.ma_doibong
            list_team_in_group.append(ma_doibong)
        for i in range(0, 4):
            for j in range(i+1, 4):
                trandau = TRANDAU(
                    ma_giaidau=self,
                    trongtai=TRONGTAI.get_random_trongtai()
                )
                trandau.save()
                chitiettrandau = CHITIETTRANDAU(
                    ma_giaidau=self,
                    ma_trandau=trandau,
                    ma_doiA=list_team_in_group[i],
                    ma_doiB=list_team_in_group[j],
                )
                chitiettrandau.save()

    def randomly_matches_gen(self):
        self.randomly_group_division()
        if self.sodoi_thamdu == 8:
            self.randomly_matches_gen_in_group(bangdau='A')
            self.randomly_matches_gen_in_group(bangdau='B')
        elif self.sodoi_thamdu == 16:
            self.randomly_matches_gen_in_group(bangdau='A')
            self.randomly_matches_gen_in_group(bangdau='B')
            self.randomly_matches_gen_in_group(bangdau='C')
            self.randomly_matches_gen_in_group(bangdau='D')

        self.quarter_matches()
        self.semi_matches()
        self.final_match()

        self.is_arranged = True
        self.save()

    def quarter_matches(self):
        if self.sodoi_thamdu == 8:
            return None
        else:
            CHITIETTRANDAU.match_making(
                self, None, None, TRONGTAI.get_random_trongtai(), 'tuket1')
            CHITIETTRANDAU.match_making(
                self, None, None, TRONGTAI.get_random_trongtai(), 'tuket2')
            CHITIETTRANDAU.match_making(
                self, None, None, TRONGTAI.get_random_trongtai(), 'tuket3')
            CHITIETTRANDAU.match_making(
                self, None, None, TRONGTAI.get_random_trongtai(), 'tuket4')

    def semi_matches(self):
        CHITIETTRANDAU.match_making(
            self, None, None, TRONGTAI.get_random_trongtai(), 'banket1')
        CHITIETTRANDAU.match_making(
            self, None, None, TRONGTAI.get_random_trongtai(), 'banket2')

    def final_match(self):
        CHITIETTRANDAU.match_making(
            self, None, None, TRONGTAI.get_random_trongtai(), 'chungket')

    def get_ranking(self):
        bxh = []
        if self.trangthai == 'Đang diễn ra':
            xephang = XEPHANG.objects.filter(ma_giaidau=self.ma_giaidau)
            return xephang.order_by('thuhang', 'bangdau')

    def is_semi(self):
        chitiet1 = CHITIETTRANDAU.objects.filter(
            ma_giaidau=self.ma_giaidau, tinhchat='tuket1')
        chitiet2 = CHITIETTRANDAU.objects.filter(
            ma_giaidau=self.ma_giaidau, tinhchat='tuket2')
        chitiet3 = CHITIETTRANDAU.objects.filter(
            ma_giaidau=self.ma_giaidau, tinhchat='tuket3')
        chitiet4 = CHITIETTRANDAU.objects.filter(
            ma_giaidau=self.ma_giaidau, tinhchat='tuket4')
        if chitiet1 is None or chitiet2 is None or chitiet3 is None \
                or chitiet4 is None:
            return False
        return True

    def is_quater(self):
        chitiet = CHITIETTRANDAU.objects.filter(
            ma_giaidau=self.ma_giaidau, tinhchat='')
        for c in chitiet:
            if c.banthang_A is None:
                return False
        return True

    def is_final(self):
        chitiet1 = CHITIETTRANDAU.objects.filter(
            ma_giaidau=self.ma_giaidau, tinhchat='banket1')
        chitiet2 = CHITIETTRANDAU.objects.filter(
            ma_giaidau=self.ma_giaidau, tinhchat='banket2')

        if chitiet1 is None or chitiet2 is None:
            return False
        return True

    def update_playoff(self):
        if self.is_final():
            doiA = CHITIETTRANDAU.objects.get(
                ma_giaidau=self.ma_giaidau, tinhchat='banket1').get_winner()
            doiB = CHITIETTRANDAU.objects.get(
                ma_giaidau=self.ma_giaidau, tinhchat='banket2').get_winner()
            chitiet = CHITIETTRANDAU.objects.get(
                ma_giaidau=self.ma_giaidau, tinhchat='chungket')
            chitiet.ma_doiA, chitiet.ma_doiB = doiA, doiB
            chitiet.save()
        elif self.is_semi():
            if self.sodoi_thamdu == 8:
                nhatA = XEPHANG.get_first(self, 'A')
                nhiB = XEPHANG.get_second(self, 'B')
                chitiet = CHITIETTRANDAU.objects.get(
                    ma_giaidau=self.ma_giaidau, tinhchat='banket1')
                chitiet.ma_doiA, chitiet.ma_doiB = nhatA, nhiB
                chitiet.save()

                nhatB = XEPHANG.get_first(self, 'B')
                nhiA = XEPHANG.get_second(self, 'A')
                chitiet = CHITIETTRANDAU.objects.get(
                    ma_giaidau=self.ma_giaidau, tinhchat='banket2')
                chitiet.ma_doiA, chitiet.ma_doiB = nhatB, nhiA
                chitiet.save()
            else:
                doiA = CHITIETTRANDAU.objects.filter(
                    ma_giaidau=self.ma_giaidau, tinhchat='tuket1').get_winner()
                doiB = CHITIETTRANDAU.objects.filter(
                    ma_giaidau=self.ma_giaidau, tinhchat='tuket2').get_winner()
                chitiet = CHITIETTRANDAU.objects.get(
                    ma_giaidau=self.ma_giaidau, tinhchat='banket1')
                chitiet.ma_doiA, chitiet.ma_doiB = doiA, doiB
                chitiet.save()

                doiC = CHITIETTRANDAU.objects.filter(
                    ma_giaidau=self.ma_giaidau, tinhchat='tuket3').get_winner()
                doiD = CHITIETTRANDAU.objects.filter(
                    ma_giaidau=self.ma_giaidau, tinhchat='tuket4').get_winner()
                chitiet = CHITIETTRANDAU.objects.get(
                    ma_giaidau=self.ma_giaidau, tinhchat='banket2')
                chitiet.ma_doiA, chitiet.ma_doiB = doiC, doiD
                chitiet.save()
        elif self.is_quater():
            if self.sodoi_thamdu == 8:
                pass
            else:
                nhatA = XEPHANG.get_first(self, 'A')
                nhiB = XEPHANG.get_second(self, 'B')
                chitiet = CHITIETTRANDAU.objects.get(
                    ma_giaidau=self.ma_giaidau, tinhchat='tuket1')
                chitiet.ma_doiA, chitiet.ma_doiB = nhatA, nhiB
                chitiet.save()

                nhiA = XEPHANG.get_second(self, 'A')
                nhatB = XEPHANG.get_first(self, 'B')
                chitiet = CHITIETTRANDAU.objects.get(
                    ma_giaidau=self.ma_giaidau, tinhchat='tuket2')
                chitiet.ma_doiA, chitiet.ma_doiB = nhatB, nhiA
                chitiet.save()

                nhatC = XEPHANG.get_first(self, 'C')
                nhiD = XEPHANG.get_second(self, 'D')
                chitiet = CHITIETTRANDAU.objects.get(
                    ma_giaidau=self.ma_giaidau, tinhchat='tuket3')
                chitiet.ma_doiA, chitiet.ma_doiB = nhatC, nhiD
                chitiet.save()

                nhiC = XEPHANG.get_second(self, 'C')
                nhatD = XEPHANG.get_first(self, 'D')
                chitiet = CHITIETTRANDAU.objects.get(
                    ma_giaidau=self.ma_giaidau, tinhchat='tuket4')
                chitiet.ma_doiA, chitiet.ma_doiB = nhatD, nhiC
                chitiet.save()
        else:
            pass


class DOIBONG(models.Model):
    ma_doibong = models.BigAutoField(primary_key=True, null=False)
    ten_doibong = models.CharField(max_length=50, null=False)
    mauao_chinh = models.CharField(max_length=10, null=False)
    mauao_phu = models.CharField(max_length=10, null=False)
    ten_taikhoan = models.ForeignKey(User, on_delete=CASCADE)
    # is team playing in any tournament?
    playing = models.BooleanField(null=False, default=False)
    # playin {ma_giaidau} tournament
    playin = models.ForeignKey(GIAIDAU, on_delete=SET_NULL, null=True)


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


class TRONGTAI(models.Model):
    ma_trongtai = models.BigAutoField(primary_key=True, null=False)
    ten_trongtai = models.CharField(max_length=50, null=False)

    def get_random_trongtai():
        return TRONGTAI.objects.order_by('?').first()


class TRANDAU(models.Model):
    ma_trandau = models.BigAutoField(primary_key=True, null=False)
    ma_giaidau = models.ForeignKey(GIAIDAU, on_delete=CASCADE, null=False)
    thoigian = models.DateField(null=True)
    diadiem = models.CharField(max_length=50, null=True)
    trongtai = models.ForeignKey(TRONGTAI, on_delete=CASCADE)

    def tostring(self):
        chitiet = CHITIETTRANDAU.objects.get(
            ma_giaidau=self.ma_giaidau, ma_trandau=self.ma_trandau)
        doiA_ = chitiet.ma_doiA
        doiB_ = chitiet.ma_doiB
        return ''+doiA_.ten_doibong+' VS '+doiB_.ten_doibong


class CHITIETTRANDAU(models.Model):
    ma_ct = models.BigAutoField(primary_key=True, null=False)
    ma_trandau = models.ForeignKey(TRANDAU, on_delete=CASCADE)
    ma_giaidau = models.ForeignKey(GIAIDAU, on_delete=CASCADE)
    ma_doiA = models.ForeignKey(
        DOIBONG, on_delete=CASCADE, related_name='DoiA', null=True)
    ma_doiB = models.ForeignKey(
        DOIBONG, on_delete=CASCADE, related_name='DoiB', null=True)
    banthang_A = models.IntegerField(null=True)
    banthang_B = models.IntegerField(null=True)
    thephat_A = models.IntegerField(null=True)
    thephat_B = models.IntegerField(null=True)
    tinhchat = models.CharField(null=True, default='', max_length=10)
    ketqua = models.ForeignKey(
        DOIBONG, null=True, on_delete=CASCADE, related_name='ketqua')

    def get_winner(self):
        if self.banthang_A is None and self.banthang_B is None:
            return None
        elif self.banthang_A > self.banthang_B:
            return self.ma_doiA
        elif self.banthang_B > self.banthang_A:
            return self.ma_doiB

    def match_making(ma_giaidau, ma_doiA, ma_doiB, ma_trongtai, tinhchat):
        trandau = TRANDAU(
            ma_giaidau=ma_giaidau,
            trongtai=ma_trongtai,
        )
        chitiet = CHITIETTRANDAU(
            ma_giaidau=ma_giaidau,
            ma_trandau=trandau,
            ma_doiA=ma_doiA,
            ma_doiB=ma_doiB,
            tinhchat=tinhchat
        )
        trandau.save()
        chitiet.save()


class XEPHANG(models.Model):
    ma_bxh = models.BigAutoField(primary_key=True, null=False)
    ma_giaidau = models.ForeignKey(GIAIDAU, on_delete=CASCADE)
    ma_doibong = models.ForeignKey(DOIBONG, on_delete=CASCADE)
    so_tran = models.IntegerField(null=False, default=0)
    banthang = models.IntegerField(null=False, default=0)
    thephat = models.IntegerField(null=False, default=0)
    hieuso = models.IntegerField(null=False, default=0)
    so_diem = models.IntegerField(null=False, default=0)
    thuhang = models.IntegerField(null=False, default=0)
    bangdau = models.CharField(max_length=2, null=False)

    def update_thuhang(self):
        list_team_in_group = XEPHANG.objects.filter(
            ma_giaidau=self.ma_giaidau, bangdau=self.bangdau)
        list_score = []
        for team in list_team_in_group:
            list_score.append(team.so_diem)
        list_score.sort(reverse=True)
        for team in list_team_in_group:
            team.thuhang = list_score.index(team.so_diem)+1
            team.save()
        for team in list_team_in_group:
            for t in list_team_in_group:
                if team != t and team.thuhang == t.thuhang:
                    if team.hieuso > t.hieuso:
                        t.thuhang += 1
                        t.save()
                    else:
                        team.thuhang += 1
                        team.save()

    def get_first(giaidau, bangdau):  # get team at the first place
        first = XEPHANG.objects.get(
            ma_giaidau=giaidau, bangdau=bangdau, thuhang=1)
        if first:
            if first.sotran < 3:
                return first
            else:
                return None
        else:
            return None

    def get_second(giaidau, bangdau):
        second = XEPHANG.objects.get(
            ma_giaidau=giaidau, bangdau=bangdau, thuhang=2)
        if second.sotran < 3:
            return second
        else:
            return None
