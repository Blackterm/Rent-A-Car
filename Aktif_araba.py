import sqlite3
class Araba():
    def __init__(self, model,plaka, Aldigi_kilometre, Alidigi_tarih,Teslim_tarih,Kullanici_adi,araba_id):
        self.model = model
        self.plaka = plaka
        self.Aldigi_kilometre = Aldigi_kilometre
        self.Alidigi_tarih = Alidigi_tarih
        self.Teslim_tarih = Teslim_tarih
        self.Kullanici_adi = Kullanici_adi
        self.araba_id = araba_id

class Aktif_araba:

    def __init__(self):
        self.connection()

    def connection(self):
        self.baglanti = sqlite3.connect("Kiralama.db")
        self.cursor = self.baglanti.cursor()
        self.cursor.execute("Create Table If not exists Aktif_araba (Model TEXT ,Plaka TEXT,Aldigi_kilometre INT,Alidigi_tarih INT,Teslim_tarih INT,Kullanici_adi TEXT,Araba_id TEXT)")
        self.baglanti.commit()

    def araba_ekle(self,Model,Plaka,Aldigi_kilometre,Alidigi_tarih,Teslim_tarih,Kullanici_adi,Araba_id):
        self.cursor.execute("Insert into Aktif_araba Values (?,?,?,?,?,?,?)",(Model,Plaka,Aldigi_kilometre,Alidigi_tarih,Teslim_tarih,Kullanici_adi,Araba_id))
        self.baglanti.commit()


    def araba_sorgu(self, plaka):
        self.cursor.execute("Select * From Aktif_araba where Plaka = ?", (plaka,))
        user = self.cursor.fetchone()
        return user

    def araba_cikar(self,Araba_id):
        self.cursor.execute("Delete From Aktif_araba where Araba_id = ? ", (Araba_id,))
        self.baglanti.commit()

    def kisi_araba_sorgu(self, kullanici_adi):
        self.cursor.execute("Select * From Aktif_araba where Kullanici_adi = ?", (kullanici_adi,))
        user = self.cursor.fetchone()
        user1 = Araba(model=user[0], plaka=user[1], Aldigi_kilometre=user[2], Alidigi_tarih=user[3],
                      Teslim_tarih=user[4],Kullanici_adi=user[5],araba_id=user[6])

        return user1

    def aktif_araba(self):
        self.cursor.execute("Select * From Aktif_araba")
        uye = self.cursor.fetchall()
        for i in uye:
            print("Model:{}\nPlaka:{}\nKilometre:{}\nAldığı tarih:{}\nTeslim tarihi:{}\nKullanıcı adı:{}\nAraba id:{}".format(i[0], i[1], i[2], i[3],
                                                                                                 i[4], i[5],i[6]))
            print("*********************")