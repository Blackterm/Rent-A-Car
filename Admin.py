import sqlite3


class Araba():
    def __init__(self, model,plaka, Aldigi_kilometre,Verdigi_kilometre, Alidigi_tarih,Teslim_tarih,Teslim_ettigi_tarih,Kullanici_adi,araba_id):
        self.model = model
        self.plaka = plaka
        self.Aldigi_kilometre = Aldigi_kilometre
        self.Verdigi_kilometre = Verdigi_kilometre
        self.Alidigi_tarih = Alidigi_tarih
        self.Teslim_tarih = Teslim_tarih
        self.Teslim_ettigi_tarih =Teslim_ettigi_tarih
        self.Kullanici_adi = Kullanici_adi
        self.araba_id = araba_id


class Admin:

    def __init__(self):
        self.connection()

    def connection(self):
        self.baglanti = sqlite3.connect("Kiralama.db")
        self.cursor = self.baglanti.cursor()
        self.cursor.execute("Create Table If not exists Satis (Model TEXT ,Plaka TEXT,Aldigi_kilometre INT,Verdigi_kilometre INT,"
                            "Alidigi_tarih INT,Teslim_tarih INT,Teslim_ettigi_tarih INT,Kullanici_adi TEXT,Araba_id TEXT)")
        self.baglanti.commit()


    def user_sales(self,Model,Plaka,Aldigi_kilometre,Verdigi_kilometre,Alidigi_tarih,Teslim_tarih,Teslim_ettigi_tarih,Kullanici_adi,Araba_id):
        self.cursor.execute("Insert into Satis Values (?,?,?,?,?,?,?,?,?)",(Model,Plaka,Aldigi_kilometre,Verdigi_kilometre,Alidigi_tarih,Teslim_tarih,Teslim_ettigi_tarih,Kullanici_adi,Araba_id))
        self.baglanti.commit()

    def araba_kilometre_guncelleme(self,teslim_ettigi_tarih,kilometre,Araba_id):
        self.cursor.execute("UPDATE Satis SET Teslim_ettigi_tarih = ? where Araba_id = ?", (kilometre, Araba_id))
        self.cursor.execute("UPDATE Satis SET Verdigi_kilometre = ? where Araba_id = ?", (teslim_ettigi_tarih,Araba_id))
        self.baglanti.commit()

    def users_info(self):
        self.cursor.execute("Select * From Satis")
        alan = self.cursor.fetchall()
        for i in alan:
            print("Model:{} Plaka:{} \nAldığı kilometre:{} Teslim ettiği kilometre:{} \nAldığı tarih:{} Teslim tarihi:{} \nKullanıcı adı:{} ".format(i[0], i[1], i[2],i[3],i[4],i[5],i[6]))
