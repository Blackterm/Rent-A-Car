import Kullanici
import datetime
import locale
import Aktif_araba
import Arabalar
import Rastgele_kod
import Admin
import time

an = datetime.datetime.now()
locale.setlocale(locale.LC_ALL, '')




def Satis (kullanici_adi):
    kod = Rastgele_kod.Rastgele().random_char()
    user = Kullanici.Data().kullanici_cekme(kullanici_adi)
    bu_gun = datetime.datetime.strftime(an, '%d %m %Y')

    date_format = "%d %m %Y"
    a = datetime.datetime.strptime(user.ehliyet_tarih, date_format)
    b = datetime.datetime.strptime(bu_gun, date_format)

    fark = b - a
    while True:
        Value = input("""{}\nKiralamak istediğiniz arabanın plakası\nÖRN"38CAN38":""".format(Arabalar.Data().arabalar_bilgi()))
        araba_varmi=Arabalar.Data().araba_sorgu(Value)
        if araba_varmi == 1:
            print("Böyle bir araba mevcut değil.")
        elif araba_varmi.kullanim_gun >= fark.days :
             print("Yeterli bir ehliyete sahip değilsiniz.")
        else:
            break

    gun = int(input("Kaç günlük kiralamak istersiniz:"))
    araba = Arabalar.Data().araba_sorgu(Value)
    araba_aktif = Aktif_araba.Aktif_araba().araba_sorgu(Value)
    #Tarih denetleme
    bugun = datetime.datetime.today()
    ileri = datetime.timedelta(days=gun)
    teslim_ileri = bugun + ileri
    teslim_tarih = teslim_ileri.strftime('%d %m %Y')
    while True:
        if araba_aktif:
            print("Araba kullanımda")
            break
        else:
            while True:


                indirim_kod = input("""İndirim kodunuz var ise giriniz.\nİndirim kodunuz yok ise "Devam" yazınız:""")
                if indirim_kod == "Devam":
                    araba_ucret = gun * araba.ucret
                    print("Toplam ücretiniz:{}".format(araba_ucret))
                    break
                kod_sorgu = Rastgele_kod.KOD().indirim_kod_sorgu(indirim_kod)
                if kod_sorgu == 2:
                    print("Bu kod zaten kullanılmış.")

                elif kod_sorgu == None :
                    print("Lütfen geçerli bir kod giriniz.")

                elif kod_sorgu == 1:
                    araba_ucret = gun * araba.ucret
                    araba_toplam = araba_ucret - araba_ucret*(20 / 100)
                    Rastgele_kod.KOD().kod_giris(indirim_kod)
                    print("Toplam ücretiniz:{}".format(araba_toplam))
                    break

        Rastgele_kod.KOD().indirim_kodu_kayit(kod)
        Aktif_araba.Aktif_araba().araba_ekle(araba.model,araba.plaka,araba.kilometre,bugun.strftime('%c'),
                                             teslim_tarih,user.kullanici_adi,kod)
        Admin.Admin().user_sales(araba.model,araba.plaka,araba.kilometre,0,bugun.strftime('%c'),
                                 teslim_tarih,0,user.kullanici_adi,kod)
        break



def araba_teslim(kullanici_adi):
    kisi = Kullanici.Data().kullanici_cekme(kullanici_adi)
    sorgu = Aktif_araba.Aktif_araba().kisi_araba_sorgu(kisi.kullanici_adi)
    araba = Arabalar.Data().araba_sorgu(sorgu.plaka)
    print("Sayın {} Teslim etmek istediğiniz araba \nModel:{}\nPlaka:{}\nAldığınız Kilometre:{}\nTeslim Tarihin:{}".format(kisi.isim,sorgu.model,sorgu.plaka,
                                                                            sorgu.Aldigi_kilometre,sorgu.Teslim_tarih))

    bu_gun = datetime.datetime.strftime(an, '%d %m %Y')

    date_format = "%d %m %Y"
    a = datetime.datetime.strptime(sorgu.Teslim_tarih, date_format)
    b = datetime.datetime.strptime(bu_gun, date_format)

    fark = b - a


    fiyat = fark.days*araba.ucret
    kilometre_bilgi = input("Arabanın kilometresi.")
    if fiyat > 0:
        print("Ekstra gün için ödeyeceğiniz miktar:{}TL".format(fiyat))

    else:
        print("İşleminiz başarıyla tamamlanmıştır.")

    Arabalar.Data().araba_kilometre_guncelleme(kilometre_bilgi,sorgu.plaka)
    Admin.Admin().araba_kilometre_guncelleme(kilometre_bilgi,bu_gun,sorgu.araba_id)
    time.sleep(2)
    Aktif_araba.Aktif_araba().araba_cikar(sorgu.araba_id)
