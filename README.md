# GSB WiFi Auto Login (Linux Daemon)

KYK/GSB WiFi ağlarında yaşanan bağlantı kopması, sürekli giriş yapma zorunluluğu ve DNS problemlerini çözen; arka planda çalışan otomatik Python scripti.

## 📋 İçindekiler

- [🚀 Özellikler](#özellikler)
- [🧠 Çalışma Mantığı](#🧠-çalışma-mantığı---neden-daha-hızlı)
- [🛠️ Kurulum](#kurulum)
- [⚙️ Servis Olarak Çalıştırma (Daemon)](#servis-olarak-çalıştırma-önerilen)
- [🚑 Sorun Giderme (DNS Hatası)](#🚑-sorun-giderme-name-resolution-error-dns-hatası)
- [📝 Logları İzleme](#📝-logları-izleme)
- [⚠️ Yasal Uyarı](#⚠️-yasal-uyarı)

---

## Özellikler
* 🚀 **Otomatik Bağlanma:** İnternet koptuğu an tekrar giriş yapar.
* 🛡️ **Session Yönetimi:** Gereksiz istek atmaz, sadece ihtiyaç duyulduğunda çalışır.
* 🐧 **Systemd Desteği:** Linux açılışında otomatik başlar (Daemon).
* 🔧 **DNS Fix:** GSB ağındaki DNS çözümleme hatalarını bypass eder. 

## 🧠 Çalışma Mantığı - Neden Daha Hızlı? 

Standart bir kullanıcı, tarayıcıdan giriş yapmaya çalıştığında şu sancılı süreci bekler:
1. `wifi.gsb.gov.tr` adresine gitmeye çalışır.
2. DNS sunucusu cevap vermez veya geç verir (Timeout).
3. Tarayıcı HTML, CSS ve JavaScript dosyalarını (Login Ekranı) indirmeye çalışır.
4. Ağ yoğunluğundan dolayı sayfa yüklenmez veya yarım kalır.

**Bu Script İse Şunu Yapar:**
* **Arayüz Yok:** HTML veya CSS indirmez. Sadece sunucunun anlayacağı 1 KB'lık saf veri paketi (POST Request) gönderir.
* **DNS Derdi Yok:** Eğer `hosts` dosyasını ayarladıysanız, DNS sunucusuna soru sormaz. Doğrudan hedef IP'ye "Ben geldim, kapıyı aç" der.
* **Captive Portal Beklemez:** İşletim sisteminin "Ağda oturum açmanız gerekiyor" uyarısını beklemeden, arka kapıdan (API Endpoint) kimlik doğrulamasını yapar.

Sonuç: Tarayıcıda dakikalarca veya saatlerce dönen o ekranı beklemezsiniz, script milisaniyeler içinde "Session" alır ve interneti açar.

## Kurulum

1. Repoyu klonlayın:
   ```bash
   git clone [https://github.com/reverx99/gsb-wifi-autologin.git](https://github.com/reverx99/gsb-wifi-autologin.git)
   cd gsb-wifi-autologin
   ```
2. Gerekli kütüphaneleri kurun:
   ```bash
   pip install -r requirements.txt
   ```
3. Ayar dosyasını düzenleyin:
   ```bash
   cp config.py.example config.py
   nano config.py
   # TC Kimlik ve Şifrenizi girin
   ```
4. Scripti test edin:
   ```bash
   python3 main.py
   ```

## Servis Olarak Çalıştırma (Önerilen)

Bilgisayar açıldığında otomatik çalışması için kyk-wifi.service dosyasını düzenleyip /etc/systemd/system/ altına kopyalayın.
   ```bash
sudo cp kyk-wifi.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable kyk-wifi.service
sudo systemctl start kyk-wifi.service
   ```

## 🚑 Sorun Giderme: "Name Resolution Error" (DNS Hatası)

Eğer script çalışırken `Temporary failure in name resolution` hatası alıyorsanız, KYK güvenlik duvarı DNS sorgularını engelliyor demektir. Bunu aşmanın en sağlam yolu, site adresini bilgisayarınıza "elle" tanıtmaktır.

1. **Sitenin IP Adresini Bulun:**
   Terminalde şu komutu çalıştırıp parantez içindeki IP'yi not edin (Örn: `10.x.x.x`):
   ```bash
   ping -c 1 wifi.gsb.gov.tr
   ```
2. Hosts Dosyasını Düzenleyin:
   ```bash
   sudo nano /etc/hosts
   ```
3. IP'yi Ekleyin: Dosyanın en altına inin ve bulduğunuz IP adresini şu formatta ekleyin:
   ```bash
   10.1.54.12  wifi.gsb.gov.tr
   (Not: 10.1.54.12 örnektir, kendi bulduğunuz IP'yi yazın!)
   ```
Kaydedip çıktıktan (CTRL+O, Enter, CTRL+X) sonra script DNS sunucusuna ihtiyaç duymadan direkt çalışacaktır.

## 📝 Logları Izleme

Script arka planda (Daemon olarak) çalışırken ne yaptığını, hata alıp almadığını canlı izlemek için:

```bash
journalctl -u kyk-net.service -f
```

## ⚠️ Yasal Uyarı

Bu proje sadece eğitim amaçlıdır ve KYK ağındaki bağlantı stabilitesini artırmak için geliştirilmiştir. Sorumluluk kullanıcıya aittir.