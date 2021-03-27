import sqlite3


class Araba():
    def __init__(self, model, renk, kilometre,plaka,ucret,kullanim_yasi,kullanim_gun):
        self.model = model
        self.renk = renk
        self.kilometre = kilometre
        self.plaka = plaka
        self.ucret = ucret
        self.kullanim_yasi = kullanim_yasi
        self.kullanim_gun = kullanim_gun

class Data():

    def __init__(self):
        self.connection()

    def connection(self):
        self.baglanti = sqlite3.connect("Kiralama.db")
        self.cursor = self.baglanti.cursor()
        sorgu = "Create Table If not exists Arabalar (model TEXT,renk TEXT,kilometre INT,plaka TEXT,ucret INT,Kullanim_yasi INT,Kullanim_gun)"
        self.cursor.execute(sorgu)
        self.baglanti.commit()

    def yeni_araba(self, araba):
        self.cursor.execute("Insert into Sistem Values(?,?,?,?,?,?,?)",
                            (araba.model, araba.renk,araba.kilometre, araba.plaka, araba.ucret,araba.kullanim_yasi,araba.kullanim_gun))
        self.baglanti.commit()

    def araba_sorgu(self, plaka):
        self.cursor.execute("Select * From Arabalar where plaka = ? ", (plaka,))
        user = self.cursor.fetchone()

        if user:
            user1 = Araba(model=user[0], renk=user[1], kilometre=user[2], plaka=user[3], ucret=user[4],kullanim_yasi=user[5],kullanim_gun=user[6])
            return user1
        else:
            return 1

    def araba_kilometre_guncelleme(self, kilometre, plaka):
        self.cursor.execute("UPDATE Arabalar SET kilometre = ? where plaka = ?", (kilometre, plaka))
        self.baglanti.commit()

    def arabalar_bilgi(self):
        self.cursor.execute("Select * From Arabalar  ")
        uye = self.cursor.fetchall()
        for i in uye:
            print("Model:{}\nRenk:{}\nKilometre:{}\nPlaka:{}\nÜcret:{}\nKullanım Yaşı:{}".format(i[0],i[1],i[2],i[3],i[4],i[5]))
            print("*********************")
