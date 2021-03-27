import sqlite3
import time
import Rastgele_kod
import Mail
import locale
import datetime
an = datetime.datetime.now()
locale.setlocale(locale.LC_ALL, '')


class KULLANICI():
    def __init__(self, isim, soyisim, kullanici_adi,mail, sifre, dogum_tarih, ehliyet_tarih):
        self.isim = isim
        self.soyisim = soyisim
        self.kullanici_adi = kullanici_adi
        self.mail = mail
        self.sifre = sifre
        self.dogum_tarih = dogum_tarih
        self.ehliyet_tarih = ehliyet_tarih


class Data():

    def __init__(self):
        self.connection()

    def connection(self):
        self.baglanti = sqlite3.connect("Kiralama.db")
        self.cursor = self.baglanti.cursor()
        sorgu = "Create Table If not exists Sistem (isim TEXT,soyisim TEXT,kullanici_adi TEXT,mail TEXT,sifre TEXT,dogum_tarih TEXT,ehliyet_tarih TEXT)"
        self.cursor.execute(sorgu)
        self.baglanti.commit()

    def uye_giris(self, kullanici):
        self.cursor.execute("Insert into Sistem Values(?,?,?,?,?,?,?)",
                            (kullanici.isim, kullanici.soyisim,kullanici.kullanici_adi, kullanici.mail, kullanici.sifre, kullanici.dogum_tarih, kullanici.ehliyet_tarih))
        self.baglanti.commit()

    def kullanici_cekme(self, kullanici_adi):
        self.cursor.execute("Select * From Sistem where kullanici_adi = ? ", (kullanici_adi,))
        user = self.cursor.fetchone()
        user1 = KULLANICI(isim=user[0],soyisim=user[1],kullanici_adi=user[2],mail=user[3],sifre=user[4],
                          dogum_tarih=user[5],ehliyet_tarih=user[6])
        return user1
    def kullanici_adi(self, kullanici_adi):
        self.cursor.execute("Select * From Sistem where kullanici_adi= ?", (kullanici_adi,))
        user = self.cursor.fetchone()
        return user

    def kullanici_mail(self, mail):
        self.cursor.execute("Select * From Sistem where mail= ?", (mail,))
        user = self.cursor.fetchone()
        return user

    def yeni_kullanici(self):
        while True:
            isim = input("Adınız:")
            if isim:
                break
            else:
                print("Lütfen adınızı giriniz..")
        while True:
            soyisim = input("Soyadınız:")
            if soyisim:
                break
            else:
                print("Lütfen soyadınızı giriniz..")
        while True:
            kullanici_adi = input("Kullanıcı adınız:")
            kullanici_mail = Data().kullanici_adi(kullanici_adi)
            if kullanici_mail:
                print("Böyle bir kullanıcı adı zaten mevcut...")
            else:
                break

        while True:
            mail = input("Mailiniz:")
            kullanici_mail = Data().kullanici_mail(mail)
            mail_kontrol = mail.find("@")
            if kullanici_mail:
                print("Böyle bir mail zaten mevcut...")
            elif mail_kontrol == -1:
                print("Lütfen geçerli bir mail giriniz.")
            else:
                break
        while True:
            sifre = input("Şifreniz en az 6 haneli olmalıdır.\nŞifreniz:")
            if 5 >= len(sifre):
                print("Şifreniz en az 6 haneli olmalıdır.")
            else:
                break
        while True:
            dogum_tarih = input("Doğum Tarhiniz\nÖrn 02 02 2000:")
            bu_gun = datetime.datetime.strftime(an, '%d %m %Y')

            date_format = "%d %m %Y"
            dogumtarih = datetime.datetime.strptime(dogum_tarih, date_format)
            bugun = datetime.datetime.strptime(bu_gun, date_format)
            fark = bugun - dogumtarih
            if 6574 > fark.days:
                print("Yaşınız 18'den küçük kayıt olamazsınız...")
            else:
                break
        ehliyet_tarih = input("Ehliyet Tarihi:")
        yeni_kullanici = KULLANICI(isim,soyisim,kullanici_adi,mail,sifre,dogum_tarih,ehliyet_tarih)
        mail_verfy = Rastgele_kod.Rastgele().kod_kontrol(yeni_kullanici.mail)
        #Şayet kullanıcıya gelen kod doğru girilmişse bir üstteki kod 1 dönderiyor.
        if mail_verfy == 1:
            Data().uye_giris(yeni_kullanici)
            # Mail gönderebilmesi için süre konulması.
            time.sleep(10)
            print("Doğrulama tamamlandı..")
            Mail.MAIL().Yeni_kullanici_mesaj(yeni_kullanici.kullanici_adi)
            time.sleep(2)
            print("Ucuz ve kaliteli araba kiralama sistemine HOŞGELDİN! {} {} :)".format(yeni_kullanici.isim,yeni_kullanici.soyisim))
        else:
            print("Invalid transaction....")

    def kullanici_giris(self):
        giris_hakki = 2
        while True:
            kullanici_adi = input("Kullanıcı adınız:")
            kullanici_sifre = input("Şifreniz:")
            self.cursor.execute("Select * From Sistem where kullanici_adi= ? and sifre = ?", (kullanici_adi, kullanici_sifre))
            user = self.cursor.fetchone()
            if user:
                if user[2] == "admin":
                    return 1
                else:
                    user1 = KULLANICI(isim=user[0],soyisim=user[1],kullanici_adi=user[2],mail=user[3],sifre=user[4],
                          dogum_tarih=user[5],ehliyet_tarih=user[6])
                    return user1
            elif giris_hakki == 0:
                return 2
            else:
                print("Mailiniz ve şifreniz yanlış:")
                giris_hakki -= 1
