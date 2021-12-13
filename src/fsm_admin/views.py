from django.shortcuts import render, redirect
import random
from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from fsm_admin.models import GIAIDAU
# Create your views here.


def index(req):
    tournaments = GIAIDAU.objects.all()
    return render(req, 'home.html', {'tournaments': tournaments})


def signup(req):
    if req.user.is_authenticated:
        return redirect('index')
    if req.method == 'POST':
        email = req.POST['email']
        username = req.POST['username']
        password = req.POST['password']

        user = User.objects.create_user(
            username=username, password=password, email=email)
        user.save()
        return redirect('index')

    return render(req, 'registration/signup.html')


def signin(req):
    if req.method == 'POST':
        uname = req.POST['username']
        pword = req.POST['password']
        user = auth.authenticate(username=uname, password=pword)
        # print(user)
        if user is not None:
            auth.login(req, user)
            return redirect('index')

        else:
            messages.error(req, 'Username or Password is incorrect')

    return render(req, 'registration/signin.html')


def signout(req):
    auth.logout(req)
    return redirect('index')


@login_required(login_url='/signin')
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

        if chedo == 'Cong khai':
            chedo_final = 1

        while GIAIDAU.objects.filter(ma_giaidau=magiaidau) is True:
            magiaidau = str(random.randint(1, 10000))

        st = GIAIDAU(ma_giaidau=magiaidau, ten_giaidau=tengiaidau,
                     sodoi_thamdu=sodoithamdu,
                     thethuc=thethuc, luatuoi=luatuoi, lephi=lephi,
                     loaisan=loaisan, chedo=chedo_final, trangthai=trangthai)
        st.save()

        return redirect('index')

    return render(request, "tournament/createtournament.html")


@login_required(login_url='/signin')
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

        while GIAIDAU.objects.filter(ma_giaidau=magiaidau) is True:
            magiaidau = str(random.randint(1, 10000))

        giaidau.save()

        return redirect('index')

    return render(request, 'tournament/EditTournament.html',
                  {'tournament': giaidau})


@login_required(login_url='/signin')
def createteam(request):
    return render(request, 'user/createteam.html')
