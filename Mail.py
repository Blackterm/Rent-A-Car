import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import sys
import sqlite3
import Kullanici
import time
import Rastgele_kod

class MAIL():

    def __init__(self):
        self.connection()

    def connection(self):
        self.baglanti = sqlite3.connect("Kiralama.db")
        self.cursor = self.baglanti.cursor()
        self.baglanti.commit()

    def Yeni_kullanici_mesaj(self, kullanici_adi):
        self.cursor.execute("Select * From Sistem where kullanici_adi = ? ", (kullanici_adi,))
        user = self.cursor.fetchone()
        user1 = Kullanici.KULLANICI(isim=user[0],soyisim=user[1],kullanici_adi=user[2],mail=user[3],sifre=user[4],dogum_tarih=user[5],ehliyet_tarih=user[6])
        indirim_kodu = Rastgele_kod.Rastgele().random_char()
        Rastgele_kod.KOD().indirim_kodu_tanimlama(indirim_kodu)
        mesaj = MIMEMultipart()

        mesaj["From"] = "Göndericinin mail adresi"

        mesaj["To"] = user1.mail

        mesaj["Subject"] = "HOŞGELDİN {} {}".format(user1.isim,user1.soyisim)

        yazi = """
        Sevgili {} {};\nUcuz ve kaliteli araba kiralama sistemine HOŞGELDİN!\nBizi tercih ettiğin için sana indirim kodu tanımladık.Güvenli sürüşler dileriz :)\nİndirim Kodun: {}
        """.format(user1.isim,user1.soyisim,indirim_kodu)

        mesaj_govdesi = MIMEText(yazi, "plain")

        mesaj.attach(mesaj_govdesi)

        try:
            mail = smtplib.SMTP("smtp.gmail.com",
                                587)

            mail.ehlo()

            mail.starttls()

            mail.login("Göndericinin mail adresi",
                       "Gönderici mail şifresi")

            mail.sendmail(mesaj["From"], mesaj["To"], mesaj.as_string())

            time.sleep(2)
            mail.close()

        except:
            sys.stderr.write(
                "Mail göndermesi başarısız oldu...")
            sys.stderr.flush()

    def kullanici_sifre_istek (self,):
       giris_hakki = 2
       while True:
            mail_adres = input("Mail adresiniz:")
            self.cursor.execute("Select * From Sistem where mail = ? ", (mail_adres,))
            user = self.cursor.fetchone()

            if user:
                user1 = Kullanici.KULLANICI(isim=user[0],soyisim=user[1],kullanici_adi=user[2],mail=user[3],sifre=user[4],
                          dogum_tarih=user[5],ehliyet_tarih=user[6])
                mesaj = MIMEMultipart()

                mesaj["From"] = "Göndericinin mail adresi"

                mesaj["To"] = user1.mail

                mesaj["Subject"] = "Sevgili {} şifreniz hakkında bilgilendirme.".format(user1.kullanici_adi)

                yazi = """
                Sevgili {} {};\nŞifreniz:{}.
                """.format(user1.isim,user1.soyisim,user1.sifre)

                mesaj_govdesi = MIMEText(yazi, "plain")

                mesaj.attach(mesaj_govdesi)

                try:
                    mail = smtplib.SMTP("smtp.gmail.com",
                                        587)

                    mail.ehlo()

                    mail.starttls()

                    mail.login("Göndericinin mail adresi",
                               "Gönderici mail şifresi")

                    mail.sendmail(mesaj["From"], mesaj["To"], mesaj.as_string())

                    mail.close()
                    time.sleep(2)
                    break
                except:
                    sys.stderr.write(
                        "Mail göndermesi başarısız oldu...")
                    sys.stderr.flush()
            elif giris_hakki == 0:
                print("Daha fazla giriş hakkınız kalmamıştır.")
                break
            else:
                print("Böyle bir kullanıcı bulunamadı.")
                giris_hakki -= 1
