from api_client import get_series
import pandas as pd

# USD
usd = get_series(
    "TP.DK.USD.A",
    "01-01-2024",
    "31-12-2024"
)

# EUR
eur = get_series(
    "TP.DK.EUR.A",
    "01-01-2024",
    "31-12-2024"
)

# CHF
chf = get_series(
    "TP.DK.CHF.A",
    "01-01-2024",
    "31-12-2024"
)

# Kolon isimlerini düzenle
usd = usd.rename(columns={"TP_DK_USD_A": "USD"})
eur = eur.rename(columns={"TP_DK_EUR_A": "EUR"})
chf = chf.rename(columns={"TP_DK_CHF_A": "CHF"})

# USD ile EUR'u birleştir
df = pd.merge(
    usd[["Tarih", "USD"]],
    eur[["Tarih", "EUR"]],
    on="Tarih"
)

# CHF'yi ekle
df = pd.merge(
    df,
    chf[["Tarih", "CHF"]],
    on="Tarih"
)

# Sonucu göster

df["Tarih"] = pd.to_datetime(df["Tarih"], format="%d-%m-%Y")

df["USD"] = pd.to_numeric(df["USD"])
df["EUR"] = pd.to_numeric(df["EUR"])
df["CHF"] = pd.to_numeric(df["CHF"])


print("\nİlk 5 Satır")
print(df.head())

print("\nSon 5 Satır")
print(df.tail())

print("\nBoyut")
print(df.shape)

print("\nKolonlar")
print(df.columns)

print("\nEksik Veriler")
print(df.isnull().sum())

print(df.describe())

#Eksik verilerimizi siliyoruz burda genelde hafta sonları kur açıklanmadığı için sildik 
df = df.dropna()

print(df.shape)
print(df.isnull().sum())


#Burada diff fonksiyonu ıle her satırı önceki satır ile karşılaştırıyoruz
df["USD_Gunluk_Degisim"] = df["USD"].diff()

df["EUR_Gunluk_Degisim"] = df["EUR"].diff()

df["CHF_Gunluk_Degisim"] = df["CHF"].diff()

#Tekrarlayan satırlarımızı burada buluyoruz
print("Tekrarlayan Satır Sayısı:")
print(df.duplicated().sum())

#Burda tarihlrimizin düzgün bir sıralamada olup olmadığını görüyurz
print("Tarih sıralı mı?")
print(df["Tarih"].is_monotonic_increasing)

#Tarih kısımını düzenliyoruz 
df["Ay"] = df["Tarih"].dt.month
df["Yıl"] = df["Tarih"].dt.year
df["Gün"] = df["Tarih"].dt.day
df["Haftanın_Günü"] = df["Tarih"].dt.day_name()

gold = get_series(
    "TP.MK.KUL.YTL",
    "01-01-2024",
    "31-12-2024"
)


# Altın kolonununu düzenliyoruz
gold = gold.rename(columns={
    "TP_MK_KUL_YTL": "Gram_Altin"
})

# Altın tarihini datetime yapıyoruz
gold["Tarih"] = pd.to_datetime(
    gold["Tarih"],
    format="%Y-%m"
)

# Altın fiyatını sayısal tipe çeviriyoruz
gold["Gram_Altin"] = pd.to_numeric(
    gold["Gram_Altin"],
    errors="coerce"
)

print("\nAltın Veri Tipleri")
print(gold.dtypes)

print("\nAltın Verisi")
print(gold.head())
print("\nAltın Veri Tipleri")
print(gold.dtypes)

print("\nAltın Veri Boyutu")
print(gold.shape)

print("\nAltın Eksik Veriler")
print(gold.isnull().sum())

#Altının aylık değişimi
gold["Gram_Altin_Degisim"] = gold["Gram_Altin"].diff()

# Altının aylık yüzdesel değişimi
gold["Gram_Altin_Getiri"] = gold["Gram_Altin"].pct_change() * 100

print("\nGüncellenmiş Altın Verisi")
print(gold.head())


# ==========================================
# ANALİZ BÖLÜMÜ
# ==========================================


# ==========================================
# SORU 1 -Günlük Getiri İstatistikleri
# ==========================================

df["USD_Getiri"] = df["USD"].pct_change() * 100
df["EUR_Getiri"] = df["EUR"].pct_change() * 100
df["CHF_Getiri"] = df["CHF"].pct_change() * 100


print("\nGünlük Getiri İstatistikleri")

getiri_ozet = df[
    ["USD_Getiri", "EUR_Getiri", "CHF_Getiri"]
].describe()

print(getiri_ozet)


# ==========================================
# SORU 2 - EN YÜKSEK GÜNLÜK GETİRİ
#YORUM:
#2024 yılı içerisinde en yüksek tek günlük pozitif hareket CHF'de gerçekleşmiştir. CHF'nin %3.06'lık yükselişi,
#EUR'nin %1.75'lik ve USD'nin %1.00'lık maksimum günlük yükselişinden daha yüksektir. 
#Ayrıca EUR ve CHF'nin maksimum günlük yükselişlerinin aynı tarihte, 6 Ağustos 2024'te gerçekleşmesi dikkat çekmektedir.
# ==========================================

print("\nEn Yüksek Günlük Getiriler")

usd_max = df.loc[df["USD_Getiri"].idxmax(),
                 ["Tarih", "USD", "USD_Getiri"]]

eur_max = df.loc[df["EUR_Getiri"].idxmax(),
                 ["Tarih", "EUR", "EUR_Getiri"]]

chf_max = df.loc[df["CHF_Getiri"].idxmax(),
                 ["Tarih", "CHF", "CHF_Getiri"]]

print("\nUSD:")
print(usd_max)

print("\nEUR:")
print(eur_max)

print("\nCHF:")
print(chf_max)

## ==========================================
# SORU 3 - EN BÜYÜK GÜNLÜK DÜŞÜŞ
#YORUM:
#2024 yılı içerisindeki en büyük günlük düşüşün üç para biriminde de 25 Mart 2024 tarihinde gerçekleştiği görülmektedir.
#CHF %2,07 ile en yüksek düşüşü yaşarken,EUR %1,94 ve USD %1,06 oranında gerilemiştir.
#Aynı tarihte üç para biriminde de negatif hareket görülmesi, bu tarihin döviz piyasası açısından dikkat çekici bir gün olduğunu göstermektedir.
# ==========================================

print("\nEn Düşük Günlük Getiriler")

usd_min = df.loc[df["USD_Getiri"].idxmin(),["Tarih","USD","USD_Getiri"]]

eur_min = df.loc[df["EUR_Getiri"].idxmin(),["Tarih","EUR","EUR_Getiri"]]

chf_min = df.loc[df["CHF_Getiri"].idxmin(),["Tarih","CHF","CHF_Getiri"]]

print("\nUSD:")
print(usd_min)

print("\nEUR:")
print(eur_min)

print("\nCHF:")
print(chf_min)

# ==========================================
# SORU 4 - YIL BOYUNCA TOPLAM DEĞİŞİM
#YORUM:
#2024 yılı başlangıç ve bitiş değerleri karşılaştırıldığında USD %19,65 ile en yüksek toplam artışı göstermiştir. USD'yi %12,80 ile EUR ve %11,39 ile CHF takip etmektedir.
#Bu sonuç, incelenen üç para birimi içerisinde 2024 yılı boyunca başlangıç ve bitiş değerleri arasındaki en yüksek artışın USD'de gerçekleştiğini göstermektedir.
# ==========================================

print("\nYıl Boyunca Toplam Değişim")

ilk_usd = df["USD"].iloc[0]
son_usd = df["USD"].iloc[-1]

ilk_eur = df["EUR"].iloc[0]
son_eur = df["EUR"].iloc[-1]

ilk_chf = df["CHF"].iloc[0]
son_chf = df["CHF"].iloc[-1]

usd_toplam = (son_usd - ilk_usd) / ilk_usd * 100
eur_toplam = (son_eur - ilk_eur) / ilk_eur * 100
chf_toplam = (son_chf - ilk_chf) / ilk_chf * 100

print(f"USD: %{usd_toplam:.2f}")
print(f"EUR: %{eur_toplam:.2f}")
print(f"CHF: %{chf_toplam:.2f}")

# ==========================================
# SORU 5 - AYLIK DÖVİZ GETİRİLERİ
#YORUM:
#2024 aylık verileri karşılaştırıldığında altının özellikle Mart ayında %14,83'lük getiriyle diğer varlıklardan belirgin şekilde ayrıştığı görülmektedir
#Nisan, Temmuz, Eylül ve Ekim aylarında da altın, incelenen dövizlerin üzerinde aylık getiri sağlamıştır. Ağustos ayında ise CHF %8,06 ile altının %6,58'lik getirisini aşmıştır.
#Bu sonuçlar, aylık bazda altın ve döviz getirilerinin dönemlere göre farklılaştığını göstermektedir.
# ==========================================

# Günlük döviz verisini aylık son değerlere çeviriyoruz
aylik_df = (
    df.set_index("Tarih")[["USD", "EUR", "CHF"]]
    .resample("ME")
    .last()
    .reset_index()
)

# Aylık yüzdesel değişimleri hesaplıyoruz
aylik_df["USD_Getiri"] = aylik_df["USD"].pct_change() * 100
aylik_df["EUR_Getiri"] = aylik_df["EUR"].pct_change() * 100
aylik_df["CHF_Getiri"] = aylik_df["CHF"].pct_change() * 100

print("\nAylık Döviz Getirileri")
print(
    aylik_df[
        [
            "Tarih",
            "USD_Getiri",
            "EUR_Getiri",
            "CHF_Getiri"
        ]
    ]
)


# Altın tarihini ay sonuna çeviriyoruz
gold_aylik = gold[["Tarih", "Gram_Altin_Getiri"]].copy()

gold_aylik["Tarih"] = gold_aylik["Tarih"] + pd.offsets.MonthEnd(0)

# Döviz ve altın verilerini birleştiriyoruz
karsilastirma = pd.merge(
    aylik_df[
        ["Tarih", "USD_Getiri", "EUR_Getiri", "CHF_Getiri"]
    ],
    gold_aylik[
        ["Tarih", "Gram_Altin_Getiri"]
    ],
    on="Tarih",
    how="inner"
)

print("\nAylık Döviz - Altın Getiri Karşılaştırması")
print(karsilastirma)

# ==========================================
# SORU 6 - ALTININ EN YÜKSEK VE EN DÜŞÜK AYI
#YORUM:
#Altının 2024 yılındaki en yüksek aylık getirisi Mart ayında %14,83 olarak gerçekleşirken,
#en düşük aylık getirisi Mayıs ayında -%2,91 olmuştur. Mart ayındaki yükseliş, altının yıl içerisindeki en belirgin aylık hareketi olarak öne çıkmaktadır.
# ==========================================

en_yuksek_altin = gold.loc[
    gold["Gram_Altin_Getiri"].idxmax(),
    ["Tarih", "Gram_Altin", "Gram_Altin_Getiri"]
]

en_dusuk_altin = gold.loc[
    gold["Gram_Altin_Getiri"].idxmin(),
    ["Tarih", "Gram_Altin", "Gram_Altin_Getiri"]
]

print("\nAltının En Yüksek Aylık Getirisi")
print(en_yuksek_altin)

print("\nAltının En Düşük Aylık Getirisi")
print(en_dusuk_altin)

# ==========================================
# SORU 7 - ALTININ DÖVİZLERİ GEÇTİĞİ AYLAR
#YORUM:
#2024 yılında altın, incelenen üç dövizden daha yüksek aylık getiri sağladığı 5 ay bulunmaktadır.
#En belirgin fark Mart ayında görülmüş ve altın %14,83 getiriyle dövizlerin tamamından daha yüksek performans göstermiştir.
# ==========================================

altin_one_gecen = karsilastirma[
    (karsilastirma["Gram_Altin_Getiri"] > karsilastirma["USD_Getiri"]) &
    (karsilastirma["Gram_Altin_Getiri"] > karsilastirma["EUR_Getiri"]) &
    (karsilastirma["Gram_Altin_Getiri"] > karsilastirma["CHF_Getiri"])
]

print("\nAltının Üç Dövizi de Geçtiği Aylar")
print(
    altin_one_gecen[
        ["Tarih", "USD_Getiri", "EUR_Getiri", "CHF_Getiri", "Gram_Altin_Getiri"]
    ]
)

# ==========================================
# SORU 8 - DÖVİZLER ARASINDAKİ İLİŞKİ
#YORUM:
#Döviz getirileri arasındaki ilişki incelendiğinde en yüksek ilişki EUR ve CHF arasında görülmüştür (0,783). USD ile CHF arasındaki ilişki 0,526, USD ile EUR arasındaki ilişki ise 0,453 olarak hesaplanmıştır.
#Buna göre incelenen dönemde EUR ve CHF getirileri diğer döviz çiftlerine göre daha fazla birlikte hareket etmiştir.
# ==========================================

korelasyon = df[
    ["USD_Getiri", "EUR_Getiri", "CHF_Getiri"]
].corr()

print("\nDöviz Getirileri Arasındaki İlişki")
print(korelasyon)

# ==========================================
# SORU 9 - DÖVİZLERİN DALGALANMA KARŞILAŞTIRMASI
#YORUM:
#2024 yılı günlük getirileri incelendiğinde en yüksek dalgalanma CHF'de (0,492) görülürken, EUR 0,392 ve USD 0,223 değerleriyle daha düşük dalgalanma göstermiştir.
#Buna göre incelenen üç döviz arasında CHF'nin günlük getirileri en değişken, USD'nin ise en istikrarlı seyri gösterdiği görülmektedir.
# ==========================================

dalgalanma = df[
    ["USD_Getiri", "EUR_Getiri", "CHF_Getiri"]
].std().sort_values(ascending=False)

print("\nDövizlerin Günlük Getiri Dalgalanması")
print(dalgalanma)

# ==========================================
# SORU 10 - AYLIK PİYASA HAREKETLİLİĞİ
# ==========================================

df["USD_Hareket"] = df["USD_Getiri"].abs()
df["EUR_Hareket"] = df["EUR_Getiri"].abs()
df["CHF_Hareket"] = df["CHF_Getiri"].abs()

aylik_hareketlilik = df.groupby(
    df["Tarih"].dt.to_period("M")
)[
    ["USD_Hareket", "EUR_Hareket", "CHF_Hareket"]
].mean()

print("\nAylık Döviz Hareketliliği")
print(aylik_hareketlilik)

# ==========================================
# SORU 11 - AYLIK GETİRİ DALGALANMASI
#YORUM:
#Aylık getiri dalgalanması incelendiğinde altının 5,05 ile incelenen varlıklar arasında en yüksek dalgalanmaya sahip olduğu görülmektedir.
#CHF 2,71, EUR 2,33 ve USD 1,28 değerleriyle daha düşük dalgalanma göstermiştir.
#Bu sonuç, 2024 yılında altının aylık getirilerinin diğer üç dövize göre daha fazla değiştiğini göstermektedir.
# ==========================================

aylik_dalgalanma = karsilastirma[
    [
        "USD_Getiri",
        "EUR_Getiri",
        "CHF_Getiri",
        "Gram_Altin_Getiri"
    ]
].std().sort_values(ascending=False)

print("\nAltın ve Dövizlerin Aylık Getiri Dalgalanması")
print(aylik_dalgalanma)

# ==========================================
# SORU 12 - YILLIK TOPLAM DEĞİŞİM
#YORUM:
#2024 yılı başlangıç ve bitiş değerleri karşılaştırıldığında en yüksek toplam değişim %46,94 ile altında gerçekleşmiştir. USD %19,65, EUR %12,80 ve CHF %11,39 oranında artış göstermiştir.
#Bu sonuçlara göre incelenen varlıklar arasında altın, yıl boyunca en yüksek toplam değer artışını göstermiştir.
# ==========================================

yillik_degisim = pd.Series({
    "USD": ((df["USD"].iloc[-1] / df["USD"].iloc[0]) - 1) * 100,
    "EUR": ((df["EUR"].iloc[-1] / df["EUR"].iloc[0]) - 1) * 100,
    "CHF": ((df["CHF"].iloc[-1] / df["CHF"].iloc[0]) - 1) * 100,
    "Altın": ((gold["Gram_Altin"].iloc[-1] / gold["Gram_Altin"].iloc[0]) - 1) * 100
}).sort_values(ascending=False)

print("\n2024 Yıllık Toplam Değişim")
print(yillik_degisim)

# ==========================================
# CSV DOSYASI
# ==========================================

# 1. Döviz tablosuna Yıl-Ay kolonu ekliyoruz
df["Yil_Ay"] = df["Tarih"].dt.to_period("M")
gold["Yil_Ay"] = gold["Tarih"].dt.to_period("M")

sql_veri = pd.merge(
    df[["Tarih", "USD", "EUR", "CHF", "Yil_Ay"]],
    gold[["Yil_Ay", "Gram_Altin"]],
    on="Yil_Ay",
    how="left"
).drop(columns=["Yil_Ay"])

# 3. Eğer ilk ayda eksik kalan varsa tamamla
sql_veri["Gram_Altin"] = sql_veri["Gram_Altin"].bfill().ffill()

# 4. CSV Olarak Kaydediyoruz 
sql_veri.to_csv("doviz_altin_2024.csv", index=False, encoding="utf-8-sig")

print("\nSQL için CSV dosyası sıfır hatayla güncellendi!")
print(sql_veri.head(10))