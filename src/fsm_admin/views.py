from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
import random

from .forms import CreateUserForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from fsm_admin.models import CAUTHU, DOIBONG, GIAIDAU, HAUCAN, HLVIEN
# Create your views here.


def index(req):
    tournaments = GIAIDAU.objects.all()
    return render(req, 'home.html', {'tournaments': tournaments})


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
            return redirect('/home')
        else:
            messages.error(req, "Tên đăng nhập hoặc mật khẩu không đúng.")
            context['fail'] = True

    return render(req, 'registration/signin.html', context)


def signout(req):
    auth.logout(req)
    return redirect('/home')


@login_required(login_url='/signin')
def createtournaments(request):
    if request.method == 'POST':
        tengiaidau = request.POST['ten_giaidau']
        sodoithamdu = request.POST['sodoi_thamdu']
        thethuc = request.POST['thethuc']
        luatuoi = request.POST['luatuoi']
        lephi = request.POST['lephi']
        loaisan = request.POST['loaisan']
        chedo = request.POST['chedo']
        chedo_final = 0
        trangthai = request.POST['trangthai']

        if chedo == 'Cong khai':
            chedo_final = 1

        giaidau = GIAIDAU(ten_giaidau=tengiaidau,
                          sodoi_thamdu=sodoithamdu,
                          thethuc=thethuc, luatuoi=luatuoi, lephi=lephi,
                          loaisan=loaisan, chedo=chedo_final,
                          trangthai=trangthai)
        giaidau.save()

        return redirect('index')

    return render(request, "tournament/createtournament.html")


# Get all tournaments from the database
def allTournaments(request):
    giaidau = GIAIDAU.objects.all()
    return render(request, 'tournament/viewtournament.html',
                  {'tournament': giaidau})


# Get tournament base on key
def tournament(request, pk):
    giaidau = GIAIDAU.objects.get(ma_giaidau=pk)
    return render(request, 'tournament/viewtournament.html',
                  {'tournament': giaidau})


def search(request):
    if request.method == 'GET':
        # if request.GET.get('query'):
        #     query = request.GET.get('query')
        #     checklist = request.GET.getlist('search')
        query = request.GET.get('query')
        cond = request.GET.get('search')
        if cond == 'name':
            giaidau = GIAIDAU.objects.filter(ten_giaidau=query)
            return render(request, 'tournament/SearchResult.html',
                          {'giaidau': giaidau})
        else:
            if GIAIDAU.objects.filter(ma_giaidau=query):
                return tournament(request, query)
            # else:
            #     return render(request, 'tournament/TournamentNotExist.html')

    return render(request, 'tournament/search.html')


@login_required(login_url='/signin')
def edittournament(request, pk):
    giaidau = GIAIDAU.objects.get(ma_giaidau=pk)

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

    return render(request, 'tournament/EditTournament.html',
                  {'tournament': giaidau})


@login_required(login_url='/signin')
def createteam(request):
    if request.method == 'POST':
        current_user = request.user
        # user_id = current_user.id
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
        for i in range(1, 4):
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
                ma_doibong=doibong
            )
            cauthu.save()

        # now get value
        namec = request.POST.get('nameCoachOrSupport1')
        rolec = request.POST.get('role1')
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

        redirect('index')

    return render(request, 'user/createteam.html')


@login_required(login_url='/signin')
def jointournament(request, pk):
    current_user = request.user
    userteams = DOIBONG.objects.filter(ten_taikhoan=current_user.id)
    giaidau = GIAIDAU.objects.get(ma_giaidau=pk)
    if request.method == 'POST':
        teampk = request.POST.get('teamchoice')
        doibong = DOIBONG.objects.get(ma_doibong=teampk)
        doibong.playing = True
        doibong.save()
        giaidau.sodoi_hientai += 1
        giaidau.save()
        return redirect('index')

    return render(request, 'tournament/JoinTournament.html',
                  {'giaidau': giaidau, 'userteams': userteams})



# ================================ Admin site ===================================================

@login_required(login_url='/admin_site/signin')
def admin_site(req, tab=None):
    if tab == None:
        tab = 1
    context = {}
    for i in range(4):
        if i + 1 == tab:
            tabActive = "tab" + str(i + 1)
            context[tabActive] = {
                "active": "active",
                "show": "show",
            }
        else:
            tabActive = "tab" + str(i + 1)
            context[tabActive] = {
                "active": "",
                "show": "",
            }

    if req.user.is_authenticated and req.user.username != "admin":
        auth.logout(req)
        return redirect('admin_signin')
    
    tournaments = GIAIDAU.objects.all()

    context['tournaments'] = tournaments

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
    auth.logout(req)
    return redirect('admin_signin')

@login_required(login_url='/admin_site/signin')
def admin_create_tournament(req):
    context = {}
    tabActive = 1
    for i in range(4):
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

    if req.method == 'POST':

        tengiaidau = req.POST.get('tournamentName')
        sodoithamdu = req.POST.get('numTeams')
        thethuc = req.POST.get('format')
        if thethuc == 1:
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
        trangthai = "Đang diễn ra"


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
            messages.error("Tạo giải đấu không thành công")

    return render(req, 'admin_site/create_tournament.html', context)

@login_required(login_url='/admin_site/signin')
def admin_create_tournament_back(req):
    return redirect('/admin_site/1')
