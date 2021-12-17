from django.http.response import HttpResponse
from django.shortcuts import render, redirect
import random

from .forms import CreateUserForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from fsm_admin.models import CAUTHU, CHITIETTRANDAU, DOIBONG, GIAIDAU, HAUCAN, HLVIEN, TAIKHOAN, TRANDAU, XEPHANG
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

        if user is not None:
            auth.login(req, user)
            print(rememberme)
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

def editprofile(request):
    current_user=request.user
    if request.method == 'POST':
        hoten = request.POST.get('hoten')
        ngaysinh = request.POST.get('ngaysinh')
        gioitinh = request.POST.get('gioitinh')
        diachi = request.POST.get('diachi')
        so_dienthoai = request.POST.get('so_dienthoai')
        print(gioitinh)

        if gioitinh=='male': gioitinh="Nam"
        elif gioitinh=='female': gioitinh="Nữ"

        taikhoan = TAIKHOAN(
            ma_taikhoan=current_user,
            hoten = hoten,
            ngaysinh=ngaysinh,
            gioitinh=gioitinh,
            diachi=diachi,
            so_dienthoai=so_dienthoai,
        )

        taikhoan.save()
        return redirect('index')

    return render(request, 'account/UpdateInfo.html', {'taikhoan':current_user})

def search(request):
    if request.method == 'POST':
        # if request.GET.get('query'):
        #     query = request.GET.get('query')
        #     checklist = request.GET.getlist('search')
        query = request.POST.get('nameOrId')
        agecond = request.POST.get('age')
        numofteamcond = request.POST.get('numOfTeam')
        giaidau = GIAIDAU.objects.filter(ten_giaidau=query)
        # redirect('index')
        if agecond=='' and numofteamcond=='':
            if giaidau is not None:
                return render(request, 'tournament/SearchResult.html', {'giaidau':giaidau})
            else:
                return render(request, 'tournament/TournamentNotExists.html')
        elif agecond=='' and numofteamcond:
            giaidaus=[]
            if giaidau is not None:
                for g in giaidau:
                    if g.sodoi_thamdu == int(numofteamcond):
                        giaidaus.append(g)
            if len(giaidaus)!=0:
                return render(request, 'tournament/SearchResult.html', {'giaidau':giaidaus})
            else:
                return render(request, 'tournament/TournamentNotExist.html')
        elif agecond!='' and numofteamcond=='':
            giaidaus=[]
            if giaidau is not None:
                for g in giaidau:
                    if g.luatuoi == int(agecond):
                        giaidaus.append(g)
                return render(request, 'tournament/SearchResult.html', {'giaidau':giaidaus})
            else:
                return render(request, 'tournament/TournamentNotExist.html')
        elif agecond!='' and numofteamcond!='':
            giaidaus=[]
            if giaidau is not None:
                for g in giaidau:
                    if g.luatuoi == int(agecond) and g.sodoi_thamdu == int(numofteamcond):
                        giaidaus.append(g)
                return render(request, 'tournament/SearchResult.html', {'giaidau':giaidaus})
            else:
                return render(request, 'tournament/TournamentNotExist.html')

        # if cond == 'name':
        #     if GIAIDAU.objects.filter(ten_giaidau=query):
        #         giaidau = GIAIDAU.objects.filter(ten_giaidau=query)
        #         return render(request, 'tournament/SearchResult.html', {'giaidau':giaidau})
        #     else:
        #         return render(request, 'tournament/TournamentNotExist.html')
        # elif cond=='pk':
        #     if GIAIDAU.objects.filter(ma_giaidau=query):
        #         return tournament(request, query)
        #     else:
        #         return render(request, 'tournament/TournamentNotExist.html')

    return render(request, 'tournament/search.html')


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
                        loaisan=loaisan, chedo=chedo_final, trangthai=trangthai)
            giaidau.save()

            return redirect('index')
    else:
        return render(request,'admin/createtournamentNotGranted.html')

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
    current_user=request.user
    userteams = DOIBONG.objects.filter(ten_taikhoan=current_user.id)
    giaidau = GIAIDAU.objects.get(ma_giaidau=pk)
    if request.method == 'POST':
        teampk = request.POST.get('teamchoice')
        doibong = DOIBONG.objects.get(ma_doibong=teampk)
        doibong.playing = True
        doibong.playin = giaidau
        doibong.save()
        giaidau.sodoi_hientai+=1
        giaidau.save()
        return redirect('index')

    return render(request, 'tournament/JoinTournament.html', {'giaidau':giaidau,'userteams':userteams})

@login_required(login_url='/signin')
def deletetournament(request, pk):
    current_user = request.user
    if current_user.is_superuser:
        if request.method == 'GET':
            giaidau = GIAIDAU.objects.get(ma_giaidau=pk)
            giaidau.delete()
            doibong = DOIBONG.objects.filter(playin=pk)
            doibong.playing = False
            doibong.save()
            redirect('index')
    else:
        return render(request, 'admin/DeleteTournamentNotGranted.html')

    return render(request, 'admin/DeleteTournament.html')

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
                ma_doibong=doibong,
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

@login_required(login_url='/login')
def match_arrange(request, pk):
    current_user = request.user
    giaidau = GIAIDAU.objects.get(ma_giaidau=pk)
    ds_thamdu = giaidau.get_ds_thamdu()
    # print('views')
    # print(ds_thamdu)
    if current_user.is_superuser:
        if giaidau.sodoi_hientai == giaidau.sodoi_thamdu:
            if giaidau.is_arranged == False:
                if request.method == 'POST':
                    giaidau.randomly_matches_gen()
                    return redirect('index')
            else:
                return HttpResponse('Giai dau da duoc sap xep roi')
        else:
            return HttpResponse('Chua du so doi tham du')
    else:
        return render(request, 'admin/MatchArrangeNotGranted.html')

    return render(request, 'admin/MatchArrange.html', {'ds_thamdu':ds_thamdu,'giaidau':giaidau})

def match_arrange_result(request, pk):
    trandau = TRANDAU.objects.filter(ma_giaidau=pk)
    print(trandau)

    return render(request, 'admin/MatchArrangeResult.html',{'trandau':trandau, 'trandau':trandau})
@login_required(login_url='/login')
def matchupdate(request, tourpk, matchpk):
    current_user = request.user
    #giaidau = GIAIDAU.objects.get(ma_giaidau=tourpk)
    #trandau = TRANDAU,object.get(ma_giadau=tourpk, ma_trandau=matchpk)
    chitiettrandau = CHITIETTRANDAU.objects.get(ma_giaidau=tourpk, ma_trandau=matchpk)
    doiA = chitiettrandau.ma_doiA #DOIBONG.objects.get(ma_doibong=chitiettrandau.ma_doiA) 
    doiB = chitiettrandau.ma_doiB #DOIBONG.objects.get(ma_doibong=chitiettrandau.ma_doiB) 
    
    if request.method == 'POST':
        if current_user.is_superuser:
            #chitiettrandau = CHITIETTRANDAU.objects.get(ma_giaidau=tourpk, ma_trandau=matchpk)
            xephang_A = XEPHANG.objects.get(ma_giaidau=tourpk,ma_doibong=doiA.ma_doibong)
            xephang_B = XEPHANG.objects.get(ma_giaidau=tourpk,ma_doibong=doiB.ma_doibong)

            banthang_A = int(request.POST.get('banthang_A'))
            banthang_B = int(request.POST.get('banthang_B'))
            thephat_A = int(request.POST.get('thephat_A'))
            thephat_B = int(request.POST.get('thephat_B'))
            ketqua = None

            if banthang_A > banthang_B:
                ketqua=xephang_A.ma_doibong
                xephang_A.so_diem+=3
                xephang_A.so_diem+=0
            elif banthang_B > banthang_A:
                ketqua=xephang_B.madoibong
                xephang_A.so_diem+=0
                xephang_B.so_diem+=3
            else:
                xephang_A.so_diem+=1
                xephang_B.so_diem+=1

            xephang_A.so_tran+=1
            xephang_A.banthang+=banthang_A
            xephang_A.thephat+=thephat_A
            xephang_A.hieuso+=(banthang_A-banthang_B)
            xephang_A.save()
            xephang_B.so_tran+=1
            xephang_B.banthang+=banthang_B
            xephang_B.thephat+=thephat_B
            xephang_B.hieuso+=(banthang_B-banthang_A)
            xephang_B.save()
            xephang_A.update_thuhang()
            xephang_B.update_thuhang()

            chitiettrandau.banthang_A = banthang_A
            chitiettrandau.banthang_B = banthang_B
            chitiettrandau.thephat_A = thephat_A
            chitiettrandau.thephat_B = thephat_B
            chitiettrandau.ketqua = ketqua
            chitiettrandau.save()

            
            return redirect('index')
        else:
            return render(request, 'admin/UpdateMatchNotGranted.html')

    return render(request, 'admin/UpdateMatch.html',{'doiA':doiA, 'doiB':doiB, 'trandau':chitiettrandau})
