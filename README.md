# Proyek Scraping Ulasan Tokopedia dan Analisis Sentimen

Proyek ini bertujuan untuk melakukan scraping ulasan dari halaman produk di Tokopedia, menyimpan data dalam format CSV, dan menganalisis sentimen dari ulasan tersebut menggunakan Orange. Proyek ini terdiri dari beberapa tahap utama: scraping data, preprocessing teks, analisis sentimen, dan visualisasi hasil.

## Struktur Proyek

### 1. **Scraping Data dengan Selenium dan BeautifulSoup**
   Kode Python menggunakan Selenium dan BeautifulSoup untuk mengumpulkan ulasan dari Tokopedia. Hasil scraping disimpan dalam file CSV untuk digunakan dalam analisis selanjutnya.

### 2. **Preprocessing Teks dan Analisis Sentimen di Orange**
   Data ulasan yang telah dikumpulkan diimpor ke Orange untuk tahap preprocessing teks, analisis sentimen, dan visualisasi.

### 3. **Visualisasi Data**
   Menggunakan widget visualisasi di Orange untuk memahami distribusi sentimen dan kata-kata yang sering muncul.

## Tahap 1: Scraping Data

### Kode Scraping

Berikut adalah skrip lengkap untuk melakukan scraping ulasan dari Tokopedia menggunakan Selenium dan BeautifulSoup:

```python
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import pandas as pd

# Meminta input URL toko Tokopedia
url = input("Masukkan URL toko: ")

if url:
    # Mengatur opsi driver Chrome
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    
    # Inisialisasi driver Chrome
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    
    data = []
    page = 1
    
    while True:
        print(f"Scraping halaman {page}...")
        
        # Tunggu hingga elemen kontainer ulasan muncul
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "article.css-ccpe8t"))
        )
        
        # Parsing halaman
        soup = BeautifulSoup(driver.page_source, "html.parser")
        containers = soup.findAll('article', attrs={'class': 'css-ccpe8t'})
        
        # Ekstraksi teks ulasan
        for container in containers:
            try:
                review = container.find('span', attrs={'data-testid': 'lblItemUlasan'}).text
                data.append(review)
            except AttributeError:
                continue  # Jika tidak ada ulasan, lewati
        
        # Cek apakah tombol "Laman berikutnya" ada
        try:
            next_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label^='Laman berikutnya']"))
            )
            next_button.click()
            page += 1
            time.sleep(3)  # Beri waktu halaman untuk memuat
        except:
            print("Tidak ada halaman berikutnya, scraping selesai.")
            break  # Keluar dari loop jika tidak ada tombol berikutnya
    
    # Simpan data ke dalam CSV
    df = pd.DataFrame(data, columns=["Ulasan"])
    df.to_csv("Tokopedia.csv", index=False, encoding='utf-8')
    print("Data ulasan telah disimpan ke Tokopedia.csv")
    
    # Tutup driver
    driver.quit()
else:
    print("URL toko tidak dimasukkan.")
```

### Cara Menjalankan Kode

1. Pastikan memiliki **Chromedriver** yang sesuai dengan versi Google Chrome Anda.
2. Instal pustaka yang dibutuhkan dengan perintah berikut:
   ```bash
   pip install beautifulsoup4 selenium pandas
   ```
3. Jalankan skrip, masukkan URL halaman ulasan Tokopedia yang ingin di-scrape, dan biarkan skrip berjalan hingga selesai.

### Output
- Hasil scraping akan disimpan dalam file **Tokopedia.csv** dengan kolom **Ulasan** yang berisi teks ulasan pelanggan.

---

## Tahap 2: Analisis Sentimen dan Visualisasi di Orange

Setelah mendapatkan file CSV dengan data ulasan, langkah berikutnya adalah melakukan preprocessing teks, analisis sentimen, dan visualisasi menggunakan **Orange**.
<img width="960" alt="{00CBBF02-F01E-4203-9CED-1535CF7C7C69}" src="https://github.com/user-attachments/assets/f32e2c03-8ae4-48ce-b26c-17868af9619a">


### a. Preprocessing Teks

1. **Corpus**:
   - Impor file **Tokopedia.csv** menggunakan widget **Corpus** untuk memuat data sebagai kumpulan teks.

2. **Preprocess Text**:
   - Sambungkan **Corpus** ke **Preprocess Text** dan atur pengaturan sebagai berikut:
     <img width="960" alt="{CD0DAF83-865D-4B74-B24D-661875766CA3}" src="https://github.com/user-attachments/assets/93c577fa-e570-4ae3-a845-d70507990f1c">

     - **Lowercase**: Centang untuk mengubah semua teks menjadi huruf kecil.
     - **Stopwords**: Pilih bahasa **Indonesian** untuk menghapus kata-kata umum yang tidak relevan dalam analisis sentimen.
     - **Tokenization**: Pilih opsi **Regexp** dengan pola `\w+` untuk membagi teks berdasarkan kata.
     - **Document Frequency**: Atur **Relative** dengan rentang `0.10 - 0.90` untuk menghapus kata yang terlalu jarang atau terlalu sering muncul.

### b. Analisis Sentimen

1. **Sentiment Analysis**:
   - Sambungkan **Preprocess Text** ke **Sentiment Analysis**.
   - Pilih metode **Multilingual sentiment** dengan bahasa **Indonesian** untuk menganalisis sentimen dari ulasan.
     <img width="242" alt="{CB3B96B3-3B48-4C8A-8695-513CDAA6534A}" src="https://github.com/user-attachments/assets/4052ff78-3bae-4d24-95a3-4afc12043afd">


2. **Data Table**:
   - Sambungkan **Sentiment Analysis** ke **Data Table** untuk melihat hasil analisis sentimen. Anda akan melihat kolom sentimen dengan skor untuk setiap ulasan.
    <img width="960" alt="{F5E8F93F-0C39-4961-9782-C2E9A6156F38}" src="https://github.com/user-attachments/assets/3cc83e8d-0184-48ad-88b3-3a146aff09bd">


### c. Visualisasi

1. **Distributions**:
   - Sambungkan **Sentiment Analysis** ke **Distributions** untuk melihat distribusi skor sentimen.
   
2. **Word Cloud**:
   - Sambungkan **Preprocess Text** ke **Word Cloud** untuk menampilkan kata-kata yang paling sering muncul dalam ulasan.
   
3. **Bar Plot dan Heat Map**:
   - Gunakan **Bar Plot** dan **Heat Map** untuk mendapatkan pandangan lebih dalam tentang distribusi dan pola dalam data ulasan.

### Hasil Visualisasi

- **Distributions**: Menampilkan frekuensi skor sentimen dalam bentuk histogram.
  <img width="960" alt="{96DAE521-A72E-40F7-A5C7-70D5985508DD}" src="https://github.com/user-attachments/assets/05d7f6ce-41bc-4382-9a72-d239afe90105">

- **Word Cloud**: Memvisualisasikan kata-kata umum dalam ulasan.
  <img width="960" alt="{42FAC1F9-1AF3-4D19-89ED-60D6163789B6}" src="https://github.com/user-attachments/assets/eff88584-b73e-4955-a3d2-45b0b3892069">

- **Bar Plot dan Heat Map**: Menyediakan wawasan visual tentang distribusi sentimen dan keterkaitan antar kata.
<img width="960" alt="{7AADE070-969A-4A6A-9CCE-FC62A24D3A92}" src="https://github.com/user-attachments/assets/14067bd1-4338-41e7-bebd-04182bc29c29">

<img width="960" alt="{CD617172-F4BB-43BA-AB80-E6D406E878FB}" src="https://github.com/user-attachments/assets/24a9c1c9-9d32-4281-81be-4fe318ced1b2">

<img width="960" alt="{7BEF6475-9A9D-4636-A8A7-1C334308FE89}" src="https://github.com/user-attachments/assets/f2a54c3f-dbca-48b0-accd-f2421d1669fd">

## Penjelasan File dan Struktur Folder

- **Tokopedia.csv**: File CSV berisi data ulasan dari proses scraping.
- **Orange Project File (.ows)**: Simpan alur analisis di Orange jika ingin menyimpan proses dan pengaturan.

## Kebutuhan Teknis

- **Selenium WebDriver**: Pastikan ChromeDriver sesuai dengan versi Chrome yang Anda gunakan.
- **Orange Data Mining**: Digunakan untuk preprocessing teks, analisis sentimen, dan visualisasi.
- **Python 3.x**: Untuk menjalankan skrip scraping.

## Catatan

- Analisis sentimen berbasis Multilingual Sentiment di Orange mungkin tidak sempurna untuk bahasa Indonesia. Jika Anda memerlukan akurasi lebih tinggi, pertimbangkan untuk menggunakan model seperti IndoBERT di Python.
- Pastikan untuk mengonfirmasi kebijakan penggunaan data Tokopedia dan menggunakan data secara etis.

---

README ini memberikan panduan lengkap mulai dari scraping data ulasan di Tokopedia hingga analisis sentimen dan visualisasi di Orange.
