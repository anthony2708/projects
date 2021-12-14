from django.shortcuts import render, redirect
import random
from .forms import CreateUserForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages, auth
from fsm_admin.models import GIAIDAU
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
            user = User.objects.create_user(username=username, password=password, email=email)
            user.save()
            return redirect('/signin')

    return render(req, 'registration/signup.html', context)

def signout(req):
    auth.logout(req)
    return redirect('index')

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

        if user is not None:
            auth.login(req, user)
            print(rememberme)
            if rememberme != False:
                req.session.set_expiry(2629746) # 1 tháng
            return redirect('/home')
        else:
            messages.error(req, "Tên đăng nhập hoặc mật khẩu không đúng.")
            context['fail'] = True 

    return render(req, 'registration/signin.html', context)

def createtournaments(request):
    if request.method == 'POST':
        magiaidau = str(random.randint(1, 10000))
        tengiaidau = request.POST['ten_giaidau']
        sodoithamdu = request.POST['sodoi_thamdu']
        thethuc = request.POST['thethuc']
        luatuoi = request.POST['luatuoi']
        lephi = request.POST['lephi']
        loaisan = request.POST['loaisan']
        chedo = request.POST['chedo']
        chedo_final = 0
        trangthai = request.POST['trangthai']

        # ins = GIAIDAU(ma_giaidau, tengiaidau, sodoithamdu, thethuc, luatuoi,
        # lephi,
        # loaisan, chedo, trangthai)
        # ins.save()
        if chedo == 'Cong khai':
            chedo_final = 1

        while GIAIDAU.objects.filter(ma_giaidau=magiaidau) is True:
            magiaidau = str(random.randint(1, 10000))

        st = GIAIDAU(ma_giaidau=magiaidau, ten_giaidau=tengiaidau,
                     sodoi_thamdu=sodoithamdu, thethuc=thethuc,
                     luatuoi=luatuoi, lephi=lephi, loaisan=loaisan,
                     chedo=chedo_final, trangthai=trangthai)
        st.save()

        return redirect('index')

    return render(request, "tournament/createtournament.html")


def tournament(request, pk):
    giaidau = GIAIDAU.objects.get(ma_giaidau=pk)

    return render(request, 'tournament/viewtournament.html',
                  {'tournament': giaidau})


def search(request):
    if request.method == 'GET':
        if request.GET.get('query'):
            query = request.GET.get('query')
            return tournament(request, query)

    return render(request, 'tournament/search.html')


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

        while GIAIDAU.objects.filter(ma_giaidau=magiaidau) is True:
            magiaidau = str(random.randint(1, 10000))

        giaidau.save()

        return redirect('index')

    return render(request, 'tournament/EditTournament.html',
                  {'tournament': giaidau})
