from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import pandas as pd

url = input("Masukkan URL toko: ")

if url:
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
