import string
import random
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import sys
import time
import sqlite3

class KOD():

    def __init__(self):
        self.connection()

    def connection(self):
        self.baglanti = sqlite3.connect("Kiralama.db")
        self.cursor = self.baglanti.cursor()
        sorgu = "Create Table If not exists Kod (KOD TEXT,Kullanim INT)"
        self.cursor.execute(sorgu)
        self.baglanti.commit()
    def indirim_kod_sorgu(self,Kod):
        self.cursor.execute("Select * From Kod where KOD = ? ", (Kod,))
        user = self.cursor.fetchone()
        if user[1] == 0:
            return 1
        elif user[1] == 1:
            return 2


    def indirim_kodu_tanimlama(self, Kod):
        self.cursor.execute("Insert into Kod Values(?,?)", (Kod, 0))
        self.baglanti.commit()

    def indirim_kodu_kayit(self, Kod):
        self.cursor.execute("Insert into Kod Values(?,?)", (Kod, 1))
        self.baglanti.commit()

    def kod_giris(self, Kod):
            self.cursor.execute("UPDATE Kod SET Kullanim = ? where KOD = ?", (1,Kod))
            self.baglanti.commit()


class Rastgele():

    def random_char(self):
        return ''.join(random.choice(string.ascii_letters) for x in range(5))


    def kod_kontrol(self,kullanici_mail):

        random_key = Rastgele().random_char()



        mesaj = MIMEMultipart()

        mesaj["From"] = "Göndericinin mail adresi"

        mesaj["To"] = kullanici_mail

        mesaj["Subject"] = "Mail doğrulama"

        yazi = """
                        Doğrulma kodunuz: {}\nBizi seçtiğiniz için teşekküler.
                        """.format(random_key)

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

        giris_hakki = 2
        while True:
            input_key = input("Lütfen mailinize gelen kodu giriniz:")
            if input_key == random_key:
                KOD().indirim_kodu_kayit(random_key)
                return 1
            elif giris_hakki == 0:
                print("Giriş hakkınız kalmamıştır.")
            else:
                giris_hakki -= 1
                print("Lütfen geçerli bir kod giriniz.")
