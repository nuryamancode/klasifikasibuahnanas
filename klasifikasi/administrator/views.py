from django.shortcuts import render
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from django.contrib.auth.models import User
from .models import DataNanas, RiwayatKlasifikasi
from django.core.exceptions import ValidationError
import pandas as pd
import joblib
import numpy as np
from django.db.models import F, Func, Value, FloatField
import math
import cv2
from PIL import Image
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import joblib

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
    if request.method == 'POST':
        try:
            sample = int(request.POST.get('sample'))
            label = request.POST.get('label')
            gambar = request.FILES.get('gambar')

            # Baca gambar dan ekstrak warna tengah
            if gambar:
                img = Image.open(gambar)
                img = img.resize((100, 100))  # Resize untuk konsistensi
                img_np = np.array(img)

                if img_np.ndim == 3:  # Pastikan gambar memiliki saluran warna RGB
                    height, width, _ = img_np.shape
                    center_pixel = img_np[height // 2, width // 2]
                    red, green, blue = center_pixel
                else:
                    raise ValueError("Gambar harus memiliki 3 saluran warna (RGB).")
            else:
                raise ValueError("Gambar tidak ditemukan.")

            # Simpan data ke database
            data_nanas = DataNanas(
                sample=sample,
                red=red,
                green=green,
                blue=blue,
                label=label,
                gambar=gambar  # Simpan file gambar
            )
            data_nanas.save()
            messages.success(request, 'Data nanas berhasil ditambahkan!')
        except Exception as e:
            messages.error(request, f'Error: {e}')

        return redirect('inputdatananas')

    # Menampilkan data nanas
    data_nanas = DataNanas.objects.all()
    return render(request, 'page/ind-nanas.html', {'data_nanas': data_nanas})

@login_required
def import_data_nanas(request):
    if request.method == 'POST' and request.FILES['file']:
        xlsx_file = request.FILES['file']
        try:
            # Read the Excel file into a pandas DataFrame
            df = pd.read_excel(xlsx_file)

            for row in df.itertuples():
                DataNanas.objects.create(
                    sample=row.sample, red=row.red, green=row.green, blue=row.blue, label=row.label, gambar=row.gambar
                )

            messages.success(request, "Data berhasil diimpor!")

        except Exception as e:
            messages.error(request, f'Error importing data: {str(e)}')

        return redirect('inputdatananas')

    return render(request, 'input_datananas.html')

@login_required
def kosongkan_data_nanas(request):
    if request.method == "POST":
        try:
            DataNanas.objects.all().delete()
            messages.success(request, "Semua data berhasil dihapus!")
        except Exception as e:
            messages.error(request, f"Terjadi kesalahan: {str(e)}")
        return redirect("inputdatananas")
    return redirect('inputdatananas')

@login_required
def refresh_datalatih(request):
    if request.method == "POST":
        try:
            # Ambil data dari database
            data_nanas = DataNanas.objects.all()
            if not data_nanas:
                messages.error(request, "Tidak ada data latih yang tersedia.")
                return redirect('inputdatananas')

            # Konversi data ke pandas DataFrame
            data = pd.DataFrame.from_records(data_nanas.values('red', 'green', 'blue', 'label'))

            # Pisahkan fitur dan target
            X = data[['red', 'green', 'blue']]
            y = data['label']

            # Encode label (jika target berupa string)
            label_encoder = LabelEncoder()
            y = label_encoder.fit_transform(y)

            # Normalisasi fitur
            scaler = StandardScaler()
            X = scaler.fit_transform(X)

            # Bagi data menjadi training dan testing
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

            # Bangun model MLP
            mlp_model = MLPClassifier(hidden_layer_sizes=(10, 10), activation='relu', max_iter=1000, random_state=42)
            mlp_model.fit(X_train, y_train)

            # Evaluasi model
            y_pred = mlp_model.predict(X_test)
            accuracy = accuracy_score(y_test, y_pred)
            report = classification_report(y_test, y_pred)

            # Simpan model dan scaler
            joblib.dump(mlp_model, "mlp_model.pkl")
            joblib.dump(scaler, "scaler.pkl")

            # Berikan feedback ke pengguna
            messages.success(request, f"Model berhasil diperbarui! Akurasi: {accuracy:.2f}")

        except Exception as e:
            messages.error(request, f"Terjadi kesalahan saat memperbarui model: {str(e)}")

        return redirect('inputdatananas')

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
def riwayatklasifikasi(request):
    # Ambil semua data dari model RiwayatKlasifikasi
    riwayat_nanas = RiwayatKlasifikasi.objects.all().order_by('-created_at')  # Urutkan berdasarkan waktu terbaru

    # Kirim data ke template melalui context
    return render(request, 'page/riwayat-klasifikasi.html', {
        'riwayat_nanas': riwayat_nanas
    })

# Load model dan scaler
mlp_model = joblib.load("mlp_model3.pkl")
scaler = joblib.load("scaler3.pkl")

@login_required
def hasilklasifikasi(request):
    if request.method == 'GET':
        # Tampilkan halaman form
        return render(request, 'page/hasil-klasifikasi.html')

    if request.method == 'POST':
        try:
            # Ambil nilai RGB dari form atau gambar
            uploaded_file = request.FILES.get('image')
            if uploaded_file:
                img = Image.open(uploaded_file)
                img = np.array(img)

                if img is None:
                    raise ValueError("Gambar gagal dibaca!")

                # Resize gambar dan konversi ke RGB
                resized_img = cv2.resize(img, (100, 100))
                resized_img_rgb = cv2.cvtColor(resized_img, cv2.COLOR_BGR2RGB)

                # Ambil pixel tengah gambar
                height, width, _ = resized_img_rgb.shape
                center_pixel = resized_img_rgb[height // 2, width // 2]
                red, green, blue = center_pixel
            else:
                # Ambil nilai manual dari form
                red = float(request.POST.get('red', 0))
                green = float(request.POST.get('green', 0))
                blue = float(request.POST.get('blue', 0))

            # Preprocessing data
            input_data = np.array([[red, green, blue]])
            input_data_scaled = scaler.transform(input_data)  # Normalisasi data

            # Prediksi
            prediction = mlp_model.predict(input_data_scaled)
            label_map = {0: 'C', 1: 'B', 2: 'A'}
            hasil_klasifikasi = label_map[prediction[0]]

            # Cari data nanas yang nilainya paling dekat
            closest_match = DataNanas.objects.annotate(
                diff_red=F('red') - red,
                diff_green=F('green') - green,
                diff_blue=F('blue') - blue
            ).order_by(
                (F('diff_red')**2 + F('diff_green')**2 + F('diff_blue')**2).asc()
            ).first()

            # Kembalikan hasil prediksi ke halaman
            return render(request, 'page/hasil-klasifikasi.html', {
                'hasil': hasil_klasifikasi,
                'input': {
                    'red': red,
                    'green': green,
                    'blue': blue,
                },
                'gambar': closest_match.gambar if closest_match else None
            })
        except Exception as e:
            return render(request, 'page/hasil-klasifikasi.html', {'error': str(e)})
        
@login_required(login_url='login')
def simpan_klasifikasi(request):
    if request.method == 'POST':
        try:
            # Mengambil data dari form
            red = int(float(request.POST.get('red')))  # Konversi dari string float ke integer
            green = int(float(request.POST.get('green')))  # Konversi dari string float ke integer
            blue = int(float(request.POST.get('blue')))  # Konversi dari string float ke integer
            label = request.POST.get('label')
            gambar = request.POST.get('gambar')

            # Simpan data baru ke dalam tabel RiwayatKlasifikasi
            riwayat_baru = RiwayatKlasifikasi(
                red=red,
                green=green,
                blue=blue,
                label=label,
                gambar=gambar
            )
            riwayat_baru.save()

            # Redirect kembali ke halaman hasilklasifikasi dengan pesan sukses
            messages.success(request, 'Data nanas berhasil ditambahkan!')
            return redirect('hasilklasifikasi')

        except ValueError as e:
            # Tangani kesalahan jika terjadi error pada konversi tipe data
            messages.error(request, f"Terjadi kesalahan: {str(e)}")
            return redirect('hasilklasifikasi')

        except Exception as e:
            # Tangani error lain yang tidak terduga
            messages.error(request, f"Kesalahan tidak terduga: {str(e)}")
            return redirect('hasilklasifikasi')

    # Jika request bukan POST, kembalikan ke halaman hasilklasifikasi
    return redirect('hasilklasifikasi')