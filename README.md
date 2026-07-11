# Borsa Istanbul Telegram Bot

📊 Telegram Bot - Gerçek zamanlı Borsa Istanbul hisse fiyatlarını takip edin!

## 🚀 Özellikler

- ✅ Gerçek zamanlı hisse fiyatları
- ✅ Kişisel portföy yönetimi
- ✅ Hisse ekle/çıkar
- ✅ Tüm hisseleri görüntüle
- ✅ Hisse detayları

## 📋 Kurulum

### 1. Gereksinimler
- Python 3.11+
- Telegram Bot Token (BotFather'dan)

### 2. Kurulumu Tamamla

```bash
# Virtual Environment oluştur
python -m venv venv

# Virtual Environment'ı aktif et
# Windows:
venv\Scripts\Activate.ps1

# Kütüphaneleri yükle
pip install -r requirements.txt
```

### 3. Bot Token Ayarı

`.env` dosyasını aç ve token'ı gir:
```
TELEGRAM_BOT_TOKEN=YOUR_TOKEN_HERE
```

### 4. Botu Çalıştır

```bash
python main.py
```

## 🎮 Bot Komutları

| Komut | Açıklama |
|-------|----------|
| `/start` | Botu başlat |
| `/help` | Yardım ve komutları gör |
| `/fiyat` | Tüm hisselerin fiyatlarını gör |
| `/ekle GARAN.IS` | Portföye hisse ekle |
| `/sil GARAN.IS` | Portföyden hisse çıkar |
| `/portfoy` | Senin portföyünü gör |
| `/tum_hisseler` | Tüm takip edilen hisseleri gör |

## 📊 Desteklenen Hisseler

- GARAN.IS - Garanti Bank
- ASELS.IS - Aselsan
- THYAO.IS - Turkish Airlines
- AKBNK.IS - Akbank
- TUPRS.IS - Tüpraş
- MCARD.IS - Mastercard Turkey
- ve daha fazlası...

## 📁 Dosya Yapısı

```
borsa-telegram-bot/
├── main.py              # Ana bot kodu
├── config.py            # Ayarlar
├── .env                 # Token ve gizli bilgiler
├── requirements.txt     # Python kütüphaneleri
├── README.md           # Bu dosya
└── user_portfolios.json # Kullanıcı portföyleri (otomatik oluşur)
```

## 🔐 Güvenlik

- ⚠️ `.env` dosyasını asla GitHub'a yükleme
- ⚠️ Token'ı gizli tut
- ⚠️ `.env` dosyasını `.gitignore`'a ekle

## 🤝 Katkı

Sorunlar ve öneriler için GitHub Issues açın!

## 📄 Lisans

MIT License

## 👨‍💻 Geliştirici

**Talha Borsa** - [@TalhaBorsa](https://github.com/TalhaBorsa)

---

Made with ❤️ for Borsa Istanbul Traders
