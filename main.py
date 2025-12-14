import requests
import time
import sys
import urllib3

# 1. Config Dosyası Kontrolü
# Kullanıcı config.py dosyasını oluşturmamışsa uyar ve kapat.
try:
    import config
except ImportError:
    print("HATA: 'config.py' dosyası bulunamadı!")
    print("Lütfen 'config.py.example' dosyasının adını 'config.py' yapın ve bilgilerinizi girin.")
    sys.exit(1)

# SSL Sertifika Hatalarını Sustur (KYK Sertifikası güvenilmez olduğu için)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ================= AYARLAR =================
# Bilgileri config.py dosyasından çekiyoruz
KULLANICI_ADI = config.USERNAME
SIFRE         = config.PASSWORD
# ===========================================

# Sabit Adresler
BASE_URL  = "https://wifi.gsb.gov.tr"
LOGIN_URL = f"{BASE_URL}/j_spring_security_check"
# Google'ın Captive Portal kontrol adresi (En hızlı yanıt veren test)
TEST_URL  = "http://clients3.google.com/generate_204"

# Tarayıcı Taklidi Yapan Başlıklar
HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Referer": BASE_URL,
    "Origin": BASE_URL
}

def internet_var_mi():
    """
    Basit bağlantı kontrolü.
    Google sunucusuna ping atar, yanıt alamazsa internet yok sayar.
    """
    try:
        # Timeout 3 saniye. Yanıt gelmezse internet yok demektir.
        requests.get(TEST_URL, timeout=3)
        return True
    except requests.RequestException:
        return False

def baglan():
    """
    GSB WiFi ağına giriş isteği gönderir.
    """
    print(f"\n[!] Bağlantı koptu! {KULLANICI_ADI} kullanıcısı için giriş deneniyor...")
    
    # Form verileri (Spring Security standardı)
    payload = {
        "j_username": KULLANICI_ADI,
        "j_password": SIFRE,
        "submit": "Giriş"
    }
    
    try:
        # Oturum nesnesi oluştur (Cookie yönetimi için)
        session = requests.Session()
        
        # Giriş isteğini gönder (Verify=False ile SSL hatasını yoksay)
        # allow_redirects=True: Giriş başarılı olursa yönlendirmeyi takip et
        response = session.post(
            LOGIN_URL, 
            data=payload, 
            headers=HEADERS, 
            timeout=10, 
            verify=False, 
            allow_redirects=True
        )
        
        # Basit durum kontrolü
        if "error" in response.url:
            print("[-] GİRİŞ BAŞARISIZ! Kullanıcı adı veya şifre yanlış olabilir.")
        elif response.status_code == 200 or response.status_code == 302:
            print("[+] Giriş isteği gönderildi. Bağlantı kontrol ediliyor...")
            
            # 1 saniye bekle ve kontrol et
            time.sleep(1)
            if internet_var_mi():
                print(">>> İNTERNET BAŞARIYLA GELDİ! <<<")
            else:
                print("[-] İstek gitti ama internet henüz gelmedi. (DNS veya Lag sorunu olabilir)")
        else:
            print(f"[-] Bilinmeyen sunucu cevabı: {response.status_code}")

    except Exception as e:
        # DNS hatası, Timeout vs. burada yakalanır
        print(f"[-] Bağlantı hatası oluştu: {e}")

def main():
    print(f"--- GSB WiFi Auto Login Daemon Başlatıldı ---")
    print(f"Kullanıcı: {KULLANICI_ADI}")
    print("Durum: İnternet bağlantısı izleniyor...")
    
    # Sonsuz döngü (Daemon mantığı)
    while True:
        if internet_var_mi():
            # İnternet varsa ekrana nokta basıp bekle (Sistemi yormamak için)
            sys.stdout.write(".")
            sys.stdout.flush()
            time.sleep(10) # 10 saniyede bir kontrol et
        else:
            # İnternet yoksa bağlanmayı dene
            baglan()
            time.sleep(5) # Hata alırsa 5 saniye bekle ve tekrar dene

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nScript kullanıcı tarafından durduruldu.")