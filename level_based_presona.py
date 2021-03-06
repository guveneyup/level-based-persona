import pandas as pd

user = pd.read_csv("dataset/users.csv")
ph = pd.read_csv("dataset/purchases.csv")
df = ph.merge(user, how="left", on="uid")

# Kategorik degiskenler kiriliminda toplam fiyat
df.groupby(["country", "device", "gender", "age"]).agg({"price": "sum"})

# Kategorik degiskenlerin kiriliminda toplam fiyat hesaplanip, iki degisken olacak formata getirelim
agg_df = df.groupby(["country", "device", "gender", "age"]).agg({"price": "sum"}).sort_values("price", ascending=False)
agg_df.reset_index(inplace=True)
agg_df.head()

# Yas degiskeni goz onunde bulundurup, uzerinden yeni kategorik bir degisken olusturalim
agg_df["age_cat"] = pd.cut(agg_df["age"],
                           bins=[0, 19, 24, 31, 41, agg_df["age"].max()],
                           labels=["0_18", "19_23",
                                   "24_30", "31_41",
                                   "41_" + str(agg_df["age"].max())])
agg_df.head()

# Tum kategorik degiskenleri tek bir degiskende birlestirelim
dff = agg_df[["country", "device", "gender", "age_cat"]]

agg_df["customers_level_based"] = [i[0].upper() + "_" + i[1].upper() + "_" + i[2] + "_" + i[3].upper() for i in
                                   dff.values]

agg_df.head()

# Tekrar eden deger var mi?
agg_df.shape[0] - agg_df["customers_level_based"].nunique()
# customers_level_based kiriliminda fiyatin ortalamasini alalim
agg_df = agg_df.groupby("customers_level_based").agg({"price": "mean"})
agg_df = agg_df.reset_index()
# Kontrol et
agg_df.shape[0] - agg_df["customers_level_based"].nunique()

# Veri setinin ilk 5 gozlemi
agg_df.head()

# Segmentlere Ayiralim
agg_df["segment"] = pd.qcut(agg_df["price"], 4, labels=["D", "C", "B", "A"])
agg_df.head()

# Segment kiriliminda fiyat ortalamasi
agg_df.groupby("segment").agg({"price": "mean"})


# Yeni bir musteri geldi. Turkiyeden, IOS ile siteye giris yapmis, kadin ve 42 yasinda.
# Acaba ortalama birakacagi para ve segmenti ne olur?

new_user = "TUR_IOS_F_41_75"
agg_df[agg_df["customers_level_based"] == new_user]




