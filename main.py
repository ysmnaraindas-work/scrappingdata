# Import package untuk scraping, manipulasi data, dan analisis statistik
from selenium import webdriver  # Untuk membuka browser dan mengakses halaman web
from bs4 import BeautifulSoup  # Untuk mem-parsing HTML
import pandas as pd  # Untuk manipulasi data dan analisis statistik
import numpy as np  # Untuk manipulasi data numerik
import time  # Untuk menambahkan delay antar request agar tidak terlalu cepat

# tempat menyimpan data yang akan di get
listNames = []
listPrices = []
listSellers = []
listCities = []
listSales = []
listRatings = []

# buka browser dari selenium
driver = webdriver.Chrome()

# for loop untuk membaca 10 halaman 
for page in range(1, 11):  # loop untuk halaman 1 sampai 11 (11 nggak di baca karena di jadikan pagar)
    # get akses driver URL Tokopedia dengan page tertentu
    driver.get(f"https://www.tokopedia.com/search?navsource=&page={page}&q=seblak&srp_component_id=02.01.00.00&srp_page_id=&srp_page_title=&st=")
    
    # memberi jeda agar halaman dapat get data dengan perlahan
    time.sleep(2)
    
    # get halaman HTML
    html = driver.page_source
    
    # get halaman HTML parser dengan BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")
    
    # get semua produk dalam class tertentu
    products = soup.find_all('div', class_='bYD8FcVCFyOBiVyITwDj1Q==') 
    
    # for loop untuk mengambil data di setiap page
    for product in products:
        # get nama produk
        name = product.find('div', class_='_6+OpBPVGAgqnmycna+bWIw==')  
        listNames.append(name.get_text(strip=True) if name else None)

        # get harga produk
        price = product.find('div', class_='_67d6E1xDKIzw+i2D2L0tjw==') 
        listPrices.append(price.get_text(strip=True) if price else None)

        # get nama seller
        seller_info = product.find('span', class_='T0rpy-LEwYNQifsgB-3SQw==')  
        listSellers.append(seller_info.get_text(strip=True) if seller_info else None)

        # get nama kota sller
        city_info = product.find('span', class_='pC8DMVkBZGW7-egObcWMFQ== flip') 
        listCities.append(city_info.get_text(strip=True) if city_info else None)

        # get laku barang yang terjual
        sold_info = product.find('span', class_='se8WAnkjbVXZNA8mT+Veuw==')  
        if sold_info:
            sold_text = sold_info.get_text(strip=True)
            # Mengambil angka dari teks 
            sold_number = ''.join(filter(str.isdigit, sold_text))
            listSales.append(int(sold_number) if sold_number else None)
        else:
            listSales.append(None)

        # get rating produk
        rating_info = product.find('span', class_='_9jWGz3C-GX7Myq-32zWG9w==')  
        listRatings.append(rating_info.get_text(strip=True) if rating_info else None)

# setelah scan dari semua halaman, dibuatlah dataframe
df = pd.DataFrame({
    'Nama Produk': listNames,
    'Harga Produk': listPrices,
    'Penjual': listSellers,
    'Kota Toko': listCities,
    'Banyaknya Terjual': listSales,
    'Rating Produk': listRatings
})

# print data atas untuk pengecekan
print(df.head())

# save data ke file CSV jika diperlukan
df.to_csv('seblak_tokopedia.csv', index=False)

# close browser setelah selesai
driver.quit()
