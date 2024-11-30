from django.shortcuts import render
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from django.contrib.auth.models import User

# Create your views here.
def user_not_authenticated(user):
    return not user.is_authenticated


@user_passes_test(user_not_authenticated, login_url='inputdatananas')
def v_login(request):
    return render(request, 'auth/signin.html')

@user_passes_test(user_not_authenticated, login_url='inputdatananas')
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        is_valid = True
        if not username or not password:
            messages.error(request, 'Masukkan username dan password')
            is_valid = False
        if not is_valid:
            return redirect('login')
        if not User.objects.filter(username=username).exists():
            messages.error(request, 'Username tidak ditemukan')
            return redirect('login')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('inputdatananas')
        else:
            messages.error(request, 'Password salah')
            return redirect('login')

    return render(request, 'auth/signin.html')

def logout(request):
    auth_logout(request)
    return redirect('login')

# def login(request):
#     return render(request, 'auth/signin.html')

@login_required
def inputdatananas(request):
    return render(request, 'page/ind-nanas.html')

@login_required
def inputdatagejala(request):
    return render(request, 'page/ind-gejala.html')

@login_required
def inputdatapenyakit(request):
    return render(request, 'page/ind-penyakit.html')

@login_required
def prosesmpl(request):
    return render(request, 'page/proses-mpl.html')

@login_required
def hasilklasifikasi(request):
    return render(request, 'page/hasil-klasifikasi.html')