import Kullanici
import Mail
import Satis
import Aktif_araba
import time


print("""*************************************\nHoşgeldiniz..\nÜye olmak için "1"\nÜye girişi için "2"\nŞifrenizi unuttuysanız "3" \nÇıkmak için "q" \nBasınız....\n*************************************""")
giris_hakki = 2
while True:
    giris_deger = input("Lütfen değer giriniz:")

    if giris_deger == "1":
        Kullanici.Data().yeni_kullanici()
        break
    elif giris_deger == "2":
        giris = Kullanici.Data().kullanici_giris()
        if giris == 2 :
            print("Daha fazla giriş hakkınız kalmamıştır.")
            break
        if giris == 1:
            print("Hoşgeldin admin.")
            Aktif_araba.Aktif_araba().aktif_araba()
            time.sleep(30)
        else:
            giris_deger1 = input("""Araba kiralamak için "1"\nAraba teslim etmek için "2"\nBasınız... """)
            if giris_deger1 == "1":
                Satis.Satis(giris.kullanici_adi)
            elif giris_deger1 == "2":
                Satis.araba_teslim(giris.kullanici_adi)
            else:
                print("Lütfen geçerli bir değer giriniz...")
        break
    elif giris_deger == "3":
        Mail.MAIL().kullanici_sifre_istek()
    elif giris_deger == "q":
        break
    elif giris_hakki == 0:
        print("Giriş hakkınız kalmamıştır.")
        break
    else:
        giris_hakki -= 1
        print("Lütfen geçerli bir değer giriniz...")
