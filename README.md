# GSB WiFi Auto Login (Linux Daemon)

KYK/GSB WiFi ağlarında yaşanan bağlantı kopması, sürekli giriş yapma zorunluluğu ve DNS problemlerini çözen; arka planda çalışan otomatik Python scripti.

## Özellikler
* 🚀 **Otomatik Bağlanma:** İnternet koptuğu an tekrar giriş yapar.
* 🛡️ **Session Yönetimi:** Gereksiz istek atmaz, sadece ihtiyaç duyulduğunda çalışır.
* 🐧 **Systemd Desteği:** Linux açılışında otomatik başlar (Daemon).
* 🔧 **DNS Fix:** GSB ağındaki DNS çözümleme hatalarını bypass eder. 

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
## Yasal Uyarı

Bu proje sadece eğitim amaçlıdır ve KYK ağındaki bağlantı stabilitesini artırmak için geliştirilmiştir. Sorumluluk kullanıcıya aittir.