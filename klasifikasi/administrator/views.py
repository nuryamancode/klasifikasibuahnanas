from django.shortcuts import render

# Create your views here.
def login(request):
    return render(request, 'auth/signin.html')

def inputdatananas(request):
    return render(request, 'page/ind-nanas.html')

def inputdatagejala(request):
    return render(request, 'page/ind-gejala.html')

def inputdatapenyakit(request):
    return render(request, 'page/ind-penyakit.html')

def prosesmpl(request):
    return render(request, 'page/proses-mpl.html')

def hasilklasifikasi(request):
    return render(request, 'page/hasil-klasifikasi.html')