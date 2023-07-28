from django.core.checks.messages import Error
# from django.http import request
from django.http.response import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
# from django.urls import reverse, reverse_lazy
import random
import os
# from .forms import CreateUserForm

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from fsm_admin.models import CAUTHU, CHITIETTRANDAU, DOIBONG, GIAIDAU, \
    HAUCAN, HLVIEN, TAIKHOAN, TRANDAU, XEPHANG, TRONGTAI
# Create your views here.


def index(req):
    return render(req, 'home.html')


def signup(req):
    context = {
        'fail': False,
    }
    if req.user.is_authenticated:
        return redirect('/home')

    if req.method == 'POST':
        email = req.POST['email']
        username = req.POST['username']
        password = req.POST['password']

        if User.objects.filter(username=username).exists():
            messages.info(req, "Tên đăng nhập đã tồn tại.")
            context['fail'] = True
        elif User.objects.filter(email=email).exists():
            messages.info(req, "Email đã tồn tại.")
            context['fail'] = True
        else:
            user = User.objects.create_user(
                username=username, password=password, email=email)
            user.save()
            return redirect('/signin')

    return render(req, 'registration/signup.html', context)


def signin(req):
    context = {
        'fail': False,
    }

    if req.user.is_authenticated:
        return redirect('/home')
    if req.method == 'POST':
        username = req.POST.get('username')
        password = req.POST.get('password')
        rememberme = req.POST.get('rememberme', False)

        user = authenticate(req, username=username, password=password)

        if user is not None and user.get_username() != "admin":
            auth.login(req, user)

            if rememberme is not False:
                req.session.set_expiry(2629746)  # 1 tháng
            return redirect('/')
        else:
            messages.error(req, "Tên đăng nhập hoặc mật khẩu không đúng.")
            context['fail'] = True

    return render(req, 'registration/signin.html', context)


def signout(req):
    if req.user.is_authenticated:
        auth.logout(req)
    return redirect('/home')


def editprofile(request):
    current_user = request.user
    if request.method == 'POST':
        hoten = request.POST.get('hoten')
        ngaysinh = request.POST.get('ngaysinh')
        gioitinh = request.POST.get('gioitinh')
        diachi = request.POST.get('diachi')
        so_dienthoai = request.POST.get('so_dienthoai')
        print(gioitinh)

        if gioitinh == 'male':
            gioitinh = "Nam"
        elif gioitinh == 'female':
            gioitinh = "Nữ"

        taikhoan = TAIKHOAN.objects.get(ma_taikhoan = current_user)
        taikhoan.hoten = hoten
        taikhoan.ngaysinh = ngaysinh
        taikhoan.gioitinh = gioitinh
        taikhoan.diachi = diachi
        taikhoan.so_dienthoai = so_dienthoai
        taikhoan.save()
        return redirect('index')

    return render(request, 'account/UpdateInfo.html',
                  {'taikhoan': current_user})


def search(request):
    if request.method == 'POST':
        query = request.POST.get('nameOrId')
        agecond = request.POST.get('age')
        numofteamcond = request.POST.get('numOfTeam')
        giaidau = GIAIDAU.objects.filter(ten_giaidau=query)
        if agecond == '' and numofteamcond == '':
            giaidaus = []
            if giaidau:
                for g in giaidau:
                    giaidaus.append(g)
                return render(request, 'tournament/SearchResult.html',
                              {'giaidau': giaidau})
            else:
                return render(request, 'tournament/TournamentNotExist.html')
        elif agecond == '' and numofteamcond != '':
            giaidaus = []
            if giaidau:
                for g in giaidau:
                    if g.sodoi_thamdu == int(numofteamcond):
                        giaidaus.append(g)
            if len(giaidaus) != 0:
                return render(request, 'tournament/SearchResult.html',
                              {'giaidau': giaidaus})
            else:
                return render(request, 'tournament/TournamentNotExist.html')
        elif agecond != '' and numofteamcond == '':
            giaidaus = []
            if giaidau is not None:
                for g in giaidau:
                    if g.luatuoi == int(agecond):
                        giaidaus.append(g)

            if len(giaidaus) > 0:
                return render(request, 'tournament/SearchResult.html',
                              {'giaidau': giaidaus})
            else:
                return render(request, 'tournament/TournamentNotExist.html')
        elif agecond != '' and numofteamcond != '':
            giaidaus = []
            if giaidau:
                for g in giaidau:
                    if g.luatuoi == int(agecond) and g.sodoi_thamdu == \
                            int(numofteamcond):
                        giaidaus.append(g)
            if len(giaidaus) > 0:
                return render(request, 'tournament/SearchResult.html',
                              {'giaidau': giaidaus})
            else:
                return render(request, 'tournament/TournamentNotExist.html')

    return render(request, 'tournament/search.html')


# Get all tournaments from the database
def allTournaments(request):
    giaidau = GIAIDAU.objects.all()
    return render(request, 'tournament/viewalltournament.html',
                  {'tournament': giaidau})


# Get tournament base on key
def tournament(request, pk):
    giaidau = GIAIDAU.objects.get(ma_giaidau=pk)
    bxh = []
    if giaidau.trangthai != 'Chuẩn bị':
        bxh = giaidau.get_ranking().order_by('bangdau', 'thuhang')
    chitiet = CHITIETTRANDAU.objects.filter(ma_giaidau=pk)
    doibong = []
    if bxh:
        for b in bxh:
            doibong.append(b.ma_doibong)
    return render(request, 'tournament/viewtournament.html',
                  {'tournament': giaidau,
                   'ranking': bxh,
                   'team': doibong,
                   'detail': chitiet, })


@login_required(login_url='/signin')
def createtournaments(request):
    current_user = request.user
    if current_user.is_superuser:
        if request.method == 'POST':
            tengiaidau = request.POST.get('ten_giaidau')
            sodoithamdu = request.POST.get('sodoi_thamdu')
            thethuc = request.POST.get('thethuc')
            luatuoi = request.POST.get('luatuoi')
            lephi = request.POST.get('lephi')
            loaisan = request.POST.get('loaisan')
            chedo = request.POST.get('chedo')
            chedo_final = 0
            trangthai = request.POST.get('trangthai')

            if chedo == 'Cong khai':
                chedo_final = 1

            giaidau = GIAIDAU(ten_giaidau=tengiaidau,
                              sodoi_thamdu=sodoithamdu,
                              thethuc=thethuc, luatuoi=luatuoi, lephi=lephi,
                              loaisan=loaisan, chedo=chedo_final,
                              trangthai=trangthai)
            giaidau.save()

            return redirect('index')
    else:
        return render(request, 'admin/createtournamentNotGranted.html')

    return render(request, "admin/createtournament.html")


@login_required(login_url='/signin')
def edittournament(request, pk):
    giaidau = GIAIDAU.objects.filter(ma_giaidau=pk)
    current_user = request.user
    if current_user.is_superuser:
        if request.method == "POST":
            ten = request.POST.get('new_ten_giaidau')
            sodoi_thamdu = request.POST.get('new_sodoi_thamdu')
            thethuc = request.POST.get('new_thethuc')
            luatuoi = request.POST.get('new_luatuoi')
            lephi = request.POST.get('new_lephi')
            loaisan = request.POST.get('new_loaisan')
            chedo = request.POST.get('new_chedo')
            trangthai = request.POST.get('new_trangthai')
            chedo_final = 0

            if chedo == 'Cong khai':
                chedo_final = 1

            giaidau.ten_giaidau = ten
            giaidau.sodoi_thamdu = sodoi_thamdu
            giaidau.thethuc = thethuc,
            giaidau.luatuoi = luatuoi
            giaidau.lephi = lephi
            giaidau.loaisan = loaisan
            giaidau.chedo = chedo_final
            giaidau.trangthai = trangthai

            giaidau.save()

            return redirect('index')
    else:
        return render(request, 'admin/EditTournamentNotGranted.html')

    return render(request, 'tournament/EditTournament.html',
                  {'tournament': giaidau})


@login_required(login_url='/signin')
def jointournament(request, pk):
    current_user = request.user
    userteams = DOIBONG.objects.filter(ten_taikhoan=current_user.id)
    giaidau = GIAIDAU.objects.get(ma_giaidau=pk)
    if request.method == 'POST':
        teampk = request.POST.get('teamchoice')
        doibong = DOIBONG.objects.get(ma_doibong=teampk)
        doibong.playing = True
        doibong.playin = giaidau
        doibong.save()
        giaidau.sodoi_hientai += 1
        giaidau.save()
        return redirect('index')

    return render(request, 'tournament/JoinTournament.html',
                  {'giaidau': giaidau, 'userteams': userteams})


@login_required(login_url='/signin')
def deletetournament(request, pk):
    current_user = request.user
    if current_user.is_superuser:
        if request.method == 'GET':
            giaidau = GIAIDAU.objects.get(ma_giaidau=pk)
            doibong = DOIBONG.objects.filter(playin=pk)
            for db in doibong:
                db.playing = False
                db.playin = None
                db.save()
                giaidau.delete()
                redirect('index')
    else:
        return render(request, 'admin/DeleteTournamentNotGranted.html')

    return render(request, 'admin/DeleteTournament.html')


@login_required(login_url='/signin')
def createteam(request):
    if request.method == 'POST':
        current_user = request.user
        # user_id = current_user.id
        numofplayer = int(request.POST.get('numofplayer'))
        numofCoachOrSupport = int(request.POST.get('numofCoachOrSupport'))
        nameTeam = request.POST.get('nameTeam')
        colorHomeTeam = request.POST.get('colorHomeTeam')
        colorVisitTeam = request.POST.get('colorVisitTeam')
        doibong = DOIBONG(
            ten_doibong=nameTeam,
            mauao_chinh=colorHomeTeam,
            mauao_phu=colorVisitTeam,
            ten_taikhoan=current_user
        )
        doibong.save()
        for i in range(1, numofplayer+1):
            index = str(i)
            # player
            namePlayer = 'namePlayer'+index
            number = 'number'+index
            age = 'age'+index
            position = 'postition'+index
            # now get value
            namep = request.POST.get(namePlayer)
            numberp = request.POST.get(number)
            agep = request.POST.get(age)
            positionp = request.POST.get(position)

            if (positionp == 'ST'):
                positionp = "Tiền đạo"
            elif positionp == 'CM':
                positionp = "Tiền Vệ"
            elif positionp == 'CB':
                positionp = "Hậu vệ"
            else:
                positionp = "Thủ môn"

            cauthu = CAUTHU(  # create cauthu
                ten_cauthu=namep,
                dotuoi=agep,
                so_ao=numberp,
                vitri_thidau=positionp,
                ma_doibong=doibong,
            )
            cauthu.save()

        # now get value
        for i in range(1, numofCoachOrSupport+1):
            index = str(i)
            # coach or support
            name = 'nameCoachOrSupport'+index
            role = 'role'+index
            # now get value
            namec = request.POST.get(name)
            rolec = request.POST.get(role)

            if rolec == 'HLVT':
                rolec = 'HLV Trưởng'  # create hlv truong
                hlvt = HLVIEN(
                    ten_hlv=namec,
                    vaitro=rolec,
                    ma_doibong=doibong,
                )
                hlvt.save()
            elif rolec == 'HLVP':  # create hlv pho
                rolec = 'HLP Phó'
                hlvp = HLVIEN(
                    ten_hlv=namec,
                    vaitro=rolec,
                    ma_doibong=doibong,
                )
                hlvp.save()
            else:
                hc = HAUCAN(
                    ten_haucan=namec,
                    ma_doibong=doibong,
                )
                hc.save()

        redirect('myteam')

    return render(request, 'user/createteam.html')

@login_required(login_url='/signin')
def myteam(request):
    current_user = request.user
    team_info = []
    myteams = DOIBONG.objects.filter(ten_taikhoan=current_user)
    for team in myteams:
        info = []
        cauthu = CAUTHU.objects.filter(ma_doibong=team)
        so_cauthu = len(cauthu)
        hlv = HLVIEN.objects.filter(ma_doibong=team)
        haucan = HAUCAN.objects.filter(ma_doibong=team)
        so_hlv_hc = len(hlv)+len(haucan)

        hlv_truong = HLVIEN.objects.get(ma_doibong=team, vaitro='HLV Trưởng')
        info.append(team)
        info.append(so_cauthu)
        info.append(so_hlv_hc)
        info.append(hlv_truong)
        team_info.append(info)

    return render(request, 'user/myteam.html', {'team_info':team_info})

@login_required(login_url='/signin')
def match_arrange(request, pk):
    current_user = request.user
    giaidau = GIAIDAU.objects.get(ma_giaidau=pk)
    ds_thamdu = giaidau.get_ds_thamdu()
    if current_user.is_superuser:
        if giaidau.sodoi_hientai == giaidau.sodoi_thamdu:
            if giaidau.is_arranged is False:
                if request.method == 'POST':
                    giaidau.randomly_matches_gen()
                    giaidau.trangthai = 'Đang diễn ra'
                    giaidau.save()
                    return redirect('index')
            else:
                return HttpResponse('Giai dau da duoc sap xep roi')
        else:
            return HttpResponse('Chua du so doi tham du')
    else:
        return render(request, 'admin/MatchArrangeNotGranted.html')

    return render(request, 'admin/MatchArrange.html',
                  {'ds_thamdu': ds_thamdu, 'giaidau': giaidau})


def match_arrange_result(request, pk):
    trandau = TRANDAU.objects.filter(ma_giaidau=pk)
    print(trandau)
    return render(request, 'admin/MatchArrangeResult.html',
                  {'trandau': trandau, 'trandau': trandau})


@login_required(login_url='/login')
def matchupdate(request, tourpk, matchpk):
    current_user = request.user
    giaidau = GIAIDAU.objects.get(ma_giaidau=tourpk)
    chitiettrandau = CHITIETTRANDAU.objects.get(
        ma_giaidau=tourpk, ma_trandau=matchpk)
    doiA = chitiettrandau.ma_doiA
    doiB = chitiettrandau.ma_doiB
    xephang_A = XEPHANG.objects.get(
        ma_giaidau=tourpk, ma_doibong=doiA.ma_doibong)
    xephang_B = XEPHANG.objects.get(
        ma_giaidau=tourpk, ma_doibong=doiB.ma_doibong)

    if request.method == 'POST':
        banthang_A = int(request.POST.get('banthang_A'))
        banthang_B = int(request.POST.get('banthang_B'))
        thephat_A = int(request.POST.get('thephat_A'))
        thephat_B = int(request.POST.get('thephat_B'))
        ketqua = None
        if current_user.is_superuser:
            if chitiettrandau.tinhchat == '':

                xephang_A = XEPHANG.objects.get(
                    ma_giaidau=tourpk, ma_doibong=doiA.ma_doibong)
                xephang_B = XEPHANG.objects.get(
                    ma_giaidau=tourpk, ma_doibong=doiB.ma_doibong)

                if banthang_A > banthang_B:
                    ketqua = xephang_A.ma_doibong
                    xephang_A.so_diem += 3
                    xephang_A.so_diem += 0
                elif banthang_B > banthang_A:
                    ketqua = xephang_B.ma_doibong
                    xephang_A.so_diem += 0
                    xephang_B.so_diem += 3
                else:
                    xephang_A.so_diem += 1
                    xephang_B.so_diem += 1

            elif chitiettrandau.tinhchat:
                if giaidau.is_final():
                    if banthang_A > banthang_B:
                        ketqua = xephang_A.ma_doibong
                        # ketqua = kq1.ma_doibong
                    elif banthang_B > banthang_A:
                        ketqua = xephang_B.ma_doibong

                elif giaidau.is_semi():
                    if chitiettrandau.tinhchat == 'banket1':

                        if giaidau.sodoi_thamdu == 8:
                            xephang_A = XEPHANG.get_first(giaidau, 'A')
                            xephang_B = XEPHANG.get_second(giaidau, 'B')

                            if banthang_A > banthang_B:
                                ketqua = xephang_A.ma_doibong
                                # ketqua = kq1.ma_doibong
                            elif banthang_B > banthang_A:
                                ketqua = xephang_B.ma_doibong

                        elif giaidau.sodoi_thamdu == 16:

                            if banthang_A > banthang_B:
                                ketqua = xephang_A.ma_doibong
                            elif banthang_B > banthang_A:
                                ketqua = xephang_B.ma_doibong

                    elif chitiettrandau.tinhchat == 'banket2':
                        if giaidau.sodoi_thamdu == 8:
                            xephang_A = XEPHANG.get_first(giaidau, 'B')
                            xephang_B = XEPHANG.get_second(giaidau, 'A')

                            if banthang_A > banthang_B:
                                ketqua = xephang_A.ma_doibong
                            elif banthang_B > banthang_A:
                                ketqua = xephang_B.ma_doibong

                        elif giaidau.sodoi_thamdu == 16:
                            if banthang_A > banthang_B:
                                ketqua = xephang_A.ma_doibong
                            elif banthang_B > banthang_A:
                                ketqua = xephang_B.ma_doibong

                elif giaidau.is_quarter():
                    if chitiettrandau.tinhchat == 'tuket1':
                        xephang_A = XEPHANG.get_first(giaidau, 'A')
                        xephang_B = XEPHANG.get_second(giaidau, 'B')

                        if banthang_A > banthang_B:
                            ketqua = xephang_A.ma_doibong
                        elif banthang_B > banthang_A:
                            ketqua = xephang_B.ma_doibong

                    elif chitiettrandau.tinhchat == 'tuket2':
                        xephang_A = XEPHANG.get_first(giaidau, 'B')
                        xephang_B = XEPHANG.get_second(giaidau, 'A')

                        if banthang_A > banthang_B:
                            ketqua = xephang_A.ma_doibong
                        elif banthang_B > banthang_A:
                            ketqua = xephang_B.ma_doibong

                    elif chitiettrandau.tinhchat == 'tuket3':
                        xephang_A = XEPHANG.get_first(giaidau, 'C')
                        xephang_B = XEPHANG.get_second(giaidau, 'D')

                        if banthang_A > banthang_B:
                            ketqua = xephang_A.ma_doibong
                        elif banthang_B > banthang_A:
                            ketqua = xephang_B.ma_doibong

                    elif chitiettrandau.tinhchat == 'tuket4':
                        xephang_A = XEPHANG.get_first(giaidau, 'D')
                        xephang_B = XEPHANG.get_second(giaidau, 'C')

                        if banthang_A > banthang_B:
                            ketqua = xephang_A.ma_doibong
                        elif banthang_B > banthang_A:
                            ketqua = xephang_B.ma_doibong

                else:
                    return HttpResponse('Giải đấu chưa đến vòng đấu này!!')
        else:
            return render(request, 'admin/UpdateMatchNotGranted.html')

        xephang_A.so_tran += 1
        xephang_A.banthang += banthang_A
        xephang_A.thephat += thephat_A
        xephang_A.hieuso += (banthang_A-banthang_B)
        xephang_A.save()
        xephang_B.so_tran += 1
        xephang_B.banthang += banthang_B
        xephang_B.thephat += thephat_B
        xephang_B.hieuso += (banthang_B-banthang_A)
        xephang_B.save()

        chitiettrandau.banthang_A = banthang_A
        chitiettrandau.banthang_B = banthang_B
        chitiettrandau.thephat_A = thephat_A
        chitiettrandau.thephat_B = thephat_B
        chitiettrandau.ketqua = ketqua
        chitiettrandau.save()

        xephang_A.update_thuhang()
        giaidau.update_playoff()

        return redirect('index')

    return render(request, 'admin/UpdateMatch.html',
                  {'doiA': doiA, 'doiB': doiB, 'trandau': chitiettrandau})


def match(request, tourpk, matchpk):
    giaidau = GIAIDAU.objects.get(ma_giaidau=tourpk)
    chitiet = CHITIETTRANDAU.objects.get(ma_giaidau=tourpk, ma_trandau=matchpk)
    doiA = chitiet.ma_doiA
    doiB = chitiet.ma_doiB
    return render(request, 'tournament/ViewMatch.html', {
        'doiA': doiA,
        'doiB': doiB,
        'chitiet': chitiet,
    })

# ================================= Admin site ================================


@login_required(login_url='/admin_site/signin')
def admin_site(req, tabActive=None):
    if tabActive is None:
        tabActive = 1
    context = {}
    contextTabActive = CreateContextTabActive(tabActive)
    context.update(contextTabActive)

    if req.user.is_authenticated and req.user.username != "admin":
        auth.logout(req)
        return redirect('admin_signin')

    if req.method == "POST":
        keyword = req.POST.get('keyword')

        tournaments = GIAIDAU.objects.filter(ten_giaidau=keyword).exists()
        print(tournament)
        if GIAIDAU.objects.filter(ten_giaidau=keyword).exists():
            url = '/admin_site/1/search?keyword=' + keyword
            return redirect(url)
        else:
            messages.error(req, "Không tìm thấy giải đấu phù hợp")
            context['showMsg'] = True

    tournaments = GIAIDAU.objects.all()
    context['tournaments'] = tournaments
    users = User.objects.exclude(username="admin").order_by('id')
    context['users'] = users

    return render(req, 'admin_site/home.html', context)


def admin_signin(req):
    context = {
        'fail': False,
    }
    if req.user.is_authenticated:
        if req.user.username != "admin":
            auth.logout(req)
            return redirect('admin_signin')
        else:
            return redirect('/admin_site/1')

    if req.method == 'POST':
        username = req.POST.get('username')
        password = req.POST.get('password')

        user = authenticate(req, username=username, password=password)

        if user is not None and user.get_username() == "admin":
            auth.login(req, user)
            return redirect('/admin_site/1')

        else:
            messages.error(req, "Tên đăng nhập hoặc mật khẩu không đúng.")
            context['fail'] = True

    return render(req, 'admin_site/signin.html', context)


def admin_signout(req):
    if req.user.is_authenticated:
        auth.logout(req)
    return redirect('admin_signin')


@login_required(login_url='/admin_site/signin')
def admin_create_tournament(req):
    context = {}
    tabActive = 1
    contextTabActive = CreateContextTabActive(tabActive)
    context.update(contextTabActive)

    if req.method == 'POST':

        tengiaidau = req.POST.get('tournamentName')
        sodoithamdu = req.POST.get('numTeams')
        thethuc = req.POST.get('format')
        if thethuc == "1":
            thethuc = "Vòng loại 1 lượt"
        else:
            thethuc = "Vòng loại 2 lượt"
        luatuoi = req.POST.get('age')
        lephi = req.POST.get('fee')
        loaisan = req.POST.get('type')
        chedo = req.POST.get('viewMode')
        if chedo == "public":
            chedo_final = 1
        else:
            chedo_final = 0
        trangthai = "Chuẩn bị"

        giaidau = GIAIDAU(ten_giaidau=tengiaidau,
                          sodoi_thamdu=sodoithamdu,
                          thethuc=thethuc, luatuoi=luatuoi, lephi=lephi,
                          loaisan=loaisan, chedo=chedo_final,
                          trangthai=trangthai)
        if giaidau is not None:
            giaidau.save()
            return redirect('/admin_site/1')
        else:
            context['showMsg'] = True
            messages.error(req, "Tạo giải đấu không thành công")
    
    users = User.objects.exclude(username="admin").order_by('id')
    context['users'] = users

    return render(req, 'admin_site/create_tournament.html', context)


@login_required(login_url='/admin_site/signin')
def admin_create_tournament_back(req):
    return redirect('/admin_site/1')


@login_required(login_url='/admin_site/signin')
def admin_search(req):
    context = {}
    tabActive = 1
    contextTabActive = CreateContextTabActive(tabActive)
    context.update(contextTabActive)

    keyword = req.GET.get('keyword')

    tournaments = GIAIDAU.objects.filter(ten_giaidau=keyword)
    context['tournaments'] = tournaments
    context['count'] = tournaments.count()
    
    users = User.objects.exclude(username="admin").order_by('id')
    context['users'] = users

    return render(req, 'admin_site/search_result.html', context)

@login_required(login_url='/admin_site/signin')
def admin_view_tournament(req, pk):
    giaidau = GIAIDAU.objects.get(ma_giaidau=pk)
    teams = DOIBONG.objects.filter(playin=pk)
    bxh = []
    if giaidau.trangthai != "Chuẩn bị":
        bxh = giaidau.get_ranking().order_by('bangdau', 'thuhang')
    details = CHITIETTRANDAU.objects.filter(ma_giaidau=pk).order_by('ma_ct')

    doibong = []
    if bxh:
        for b in bxh:
            doibong.append(b.ma_doibong)
            
    context = {}
    tabActive = 1
    contextTabActive = CreateContextTabActive(tabActive)
    context.update(contextTabActive)
    context['tournament'] = giaidau
    context['teams'] = teams
    context['matches'] = details
    context['doibongs'] = doibong
    context['standings'] = bxh

    users = User.objects.exclude(username="admin").order_by('id')
    context['users'] = users

    return render(req, 'admin_site/view_tournament.html', context)

@login_required(login_url='/admin_site/signin')
def admin_update_tournament(req, pk):
    tournament = GIAIDAU.objects.get(ma_giaidau=pk)
    context = {}
    tabActive = 1
    contextTabActive = CreateContextTabActive(tabActive)
    context.update(contextTabActive)
    context['tournament'] = tournament
    try:
        if req.method == "POST":
            if tournament is not None:
                tengiaidau = req.POST.get('tournamentName')
                sodoithamdu = req.POST.get('numTeams')
                thethuc = req.POST.get('format')
                if thethuc == "1":
                    thethuc = "Vòng loại 1 lượt"
                else:
                    thethuc = "Vòng loại 2 lượt"
                luatuoi = req.POST.get('age')
                lephi = req.POST.get('fee')
                loaisan = req.POST.get('type')
                chedo = req.POST.get('viewMode')
                if chedo == "public":
                    chedo_final = 1
                else:
                    chedo_final = 0
                trangthai = req.POST.get('state')

                tournament.ten_giaidau = tengiaidau
                tournament.sodoi_thamdu = sodoithamdu
                tournament.thethuc = thethuc
                tournament.luatuoi = luatuoi
                tournament.lephi = lephi
                tournament.loaisan = loaisan
                tournament.chedo = chedo_final
                tournament.trangthai = trangthai

                tournament.save()
                url = '/admin_site/1/tournament/' + str(tournament.ma_giaidau)
                return redirect(url)
    except os.error:
        print(os.error)

    users = User.objects.exclude(username="admin").order_by('id')
    context['users'] = users

    return render(req, 'admin_site/update_tournament.html', context)

@login_required(login_url='/admin_site/signin')
def admin_update_tournament_back(req, pk):
    url = '/admin_site/1/tournament/' + str(pk)
    return redirect(url)


@login_required(login_url='/admin_site/signin')
def admin_delete_tournament(req, pk):
    try:
        giaidau = GIAIDAU.objects.get(ma_giaidau=pk)
        doibong = DOIBONG.objects.filter(playin=pk)
        for db in doibong:
            db.playing = False
            db.playin = None
            db.save()
        giaidau.delete()
    except os.error:
        print(os.error)

    return redirect('/admin_site/1')

@login_required(login_url='/admin_site/signin')
def admin_match_arrange(req, pk):
    
    giaidau = GIAIDAU.objects.get(ma_giaidau=pk)
    if giaidau.sodoi_hientai == giaidau.sodoi_thamdu:
        if giaidau.is_arranged is False:
            giaidau.randomly_matches_gen()
            giaidau.trangthai = 'Đang diễn ra'
            giaidau.save()
            url = '/admin_site/1/tournament/' + str(pk)
            return redirect(url)

    url = '/admin_site/1/tournament/' + str(pk)
    return redirect(url)

@login_required(login_url='/admin_site/signin')
def admin_match_update(req, tourpk, matchpk):
    giaidau = GIAIDAU.objects.get(ma_giaidau=tourpk)
    chitiettrandau = CHITIETTRANDAU.objects.get(
        ma_giaidau=tourpk, ma_trandau=matchpk)
    trandau = TRANDAU.objects.get(ma_trandau=matchpk)
    doiA = chitiettrandau.ma_doiA
    doiB = chitiettrandau.ma_doiB
    xephang_A = XEPHANG.objects.get(
        ma_giaidau=tourpk, ma_doibong=doiA.ma_doibong)
    xephang_B = XEPHANG.objects.get(
        ma_giaidau=tourpk, ma_doibong=doiB.ma_doibong)

    users = User.objects.exclude(username="admin").order_by('id')

    context = {
        'users': users
    }

    tabActive = 1
    contextTabActive = CreateContextTabActive(tabActive)
    context.update(contextTabActive)

    if req.method == 'POST':
        banthang_A = int(req.POST.get('banthang_A'))
        banthang_B = int(req.POST.get('banthang_B'))
        thephat_A = int(req.POST.get('thephat_A'))
        thephat_B = int(req.POST.get('thephat_B'))


        thoigian = req.POST.get('thoigian')
        diadiem = req.POST.get('diadiem')
        if thoigian and diadiem:
            trandau.thoigian = thoigian
            trandau.diadiem = diadiem
            trandau.save()
        elif thoigian:
            trandau.thoigian = thoigian
            trandau.save()
        elif diadiem:
            trandau.diadiem = diadiem
            trandau.save()

        ketqua = None
        if chitiettrandau.tinhchat == '':

            xephang_A = XEPHANG.objects.get(
                ma_giaidau=tourpk, ma_doibong=doiA.ma_doibong)
            xephang_B = XEPHANG.objects.get(
                ma_giaidau=tourpk, ma_doibong=doiB.ma_doibong)

            if banthang_A > banthang_B:
                ketqua = xephang_A.ma_doibong
                xephang_A.so_diem += 3
                xephang_A.so_diem += 0
            elif banthang_B > banthang_A:
                ketqua = xephang_B.ma_doibong
                xephang_A.so_diem += 0
                xephang_B.so_diem += 3
            else:
                xephang_A.so_diem += 1
                xephang_B.so_diem += 1

        elif chitiettrandau.tinhchat:
                if giaidau.is_final():
                    if banthang_A > banthang_B:
                        ketqua = xephang_A.ma_doibong
                        # ketqua = kq1.ma_doibong
                    elif banthang_B > banthang_A:
                        ketqua = xephang_B.ma_doibong

                elif giaidau.is_semi():
                    if chitiettrandau.tinhchat == 'banket1':

                        if giaidau.sodoi_thamdu == 8:
                            xephang_A = XEPHANG.get_first(giaidau, 'A')
                            xephang_B = XEPHANG.get_second(giaidau, 'B')

                            if banthang_A > banthang_B:
                                ketqua = xephang_A.ma_doibong
                                # ketqua = kq1.ma_doibong
                            elif banthang_B > banthang_A:
                                ketqua = xephang_B.ma_doibong

                        elif giaidau.sodoi_thamdu == 16:

                            if banthang_A > banthang_B:
                                ketqua = xephang_A.ma_doibong
                            elif banthang_B > banthang_A:
                                ketqua = xephang_B.ma_doibong

                    elif chitiettrandau.tinhchat == 'banket2':
                        if giaidau.sodoi_thamdu == 8:
                            xephang_A = XEPHANG.get_first(giaidau, 'B')
                            xephang_B = XEPHANG.get_second(giaidau, 'A')

                            if banthang_A > banthang_B:
                                ketqua = xephang_A.ma_doibong
                            elif banthang_B > banthang_A:
                                ketqua = xephang_B.ma_doibong

                        elif giaidau.sodoi_thamdu == 16:
                            if banthang_A > banthang_B:
                                ketqua = xephang_A.ma_doibong
                            elif banthang_B > banthang_A:
                                ketqua = xephang_B.ma_doibong

                elif giaidau.is_quarter():
                    if chitiettrandau.tinhchat == 'tuket1':
                        xephang_A = XEPHANG.get_first(giaidau, 'A')
                        xephang_B = XEPHANG.get_second(giaidau, 'B')

                        if banthang_A > banthang_B:
                            ketqua = xephang_A.ma_doibong
                        elif banthang_B > banthang_A:
                            ketqua = xephang_B.ma_doibong

                    elif chitiettrandau.tinhchat == 'tuket2':
                        xephang_A = XEPHANG.get_first(giaidau, 'B')
                        xephang_B = XEPHANG.get_second(giaidau, 'A')

                        if banthang_A > banthang_B:
                            ketqua = xephang_A.ma_doibong
                        elif banthang_B > banthang_A:
                            ketqua = xephang_B.ma_doibong

                    elif chitiettrandau.tinhchat == 'tuket3':
                        xephang_A = XEPHANG.get_first(giaidau, 'C')
                        xephang_B = XEPHANG.get_second(giaidau, 'D')

                        if banthang_A > banthang_B:
                            ketqua = xephang_A.ma_doibong
                        elif banthang_B > banthang_A:
                            ketqua = xephang_B.ma_doibong

                    elif chitiettrandau.tinhchat == 'tuket4':
                        xephang_A = XEPHANG.get_first(giaidau, 'D')
                        xephang_B = XEPHANG.get_second(giaidau, 'C')

                        if banthang_A > banthang_B:
                            ketqua = xephang_A.ma_doibong
                        elif banthang_B > banthang_A:
                            ketqua = xephang_B.ma_doibong

                else:
                    context = {
                        'msg': 'Giải đấu chưa đến vòng đấu này!!'
                    }
                    return render(req, 'admin_site/update_match.html', context)

        xephang_A.so_tran += 1
        xephang_A.banthang += banthang_A
        xephang_A.thephat += thephat_A
        xephang_A.hieuso += (banthang_A-banthang_B)
        xephang_A.save()
        xephang_B.so_tran += 1
        xephang_B.banthang += banthang_B
        xephang_B.thephat += thephat_B
        xephang_B.hieuso += (banthang_B-banthang_A)
        xephang_B.save()

        chitiettrandau.banthang_A = banthang_A
        chitiettrandau.banthang_B = banthang_B
        chitiettrandau.thephat_A = thephat_A
        chitiettrandau.thephat_B = thephat_B
        chitiettrandau.ketqua = ketqua
        chitiettrandau.save()



        xephang_A.update_thuhang()
        giaidau.update_playoff()

        url = '/admin_site/1/tournament/' + str(tourpk)
        return redirect(url)

    context['doiA'] = doiA
    context['doiB'] = doiB
    context['tournament'] = giaidau

    return render(req, 'admin_site/update_match.html', context)



@login_required(login_url='/admin_site/signin')
def admin_view_user(req, pk):

    # Xem thông tin người dùng

    
    return redirect('/admin_site/2')

@login_required(login_url='/admin_site/signin')
def admin_delete_user(req, pk):

    # Xoá người dùng

    
    return redirect('/admin_site/2')


# Tạo context tabActive
def CreateContextTabActive(tabActive):
    context = {}
    for i in range(3):
        if i + 1 == tabActive:
            tab = "tab" + str(i + 1)
            context[tab] = {
                "active": "active",
                "show": "show",
            }
        else:
            tab = "tab" + str(i + 1)
            context[tab] = {
                "active": "",
                "show": "",
            }
    return context
