"""
Borsa Istanbul Telegram Bot - Configuration
Tüm ayarları ve sabitler burada tanımlı
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ============================================
# TELEGRAM BOT SETTINGS
# ============================================

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '')

if not TELEGRAM_BOT_TOKEN:
    raise ValueError("❌ TELEGRAM_BOT_TOKEN ortam değişkeni ayarlanmamış!")

BOT_NAME = "TeksasBorsaBOT"
BOT_USERNAME = "TeksasBorsaBOT"

# ============================================
# BORSA (BIST) STOCKS
# ============================================

DEFAULT_STOCKS = [
    'GARAN.IS',  # Garanti Bankası
    'ASELS.IS',  # Aselsan
    'THYAO.IS',  # Turkish Airlines
    'AKBNK.IS',  # Akbank
    'TUPRS.IS',  # Tüpraş
    'MCARD.IS',  # Mastercard Turkey
    'KRDMD.IS',  # Kardemir
    'ISCTR.IS',  # Iscitrix
    'GOLTS.IS',  # Goldspot
    'NTHOL.IS',  # Net Holding
]

# ============================================
# API SETTINGS
# ============================================

YFINANCE_TIMEOUT = 10  # seconds
UPDATE_INTERVAL = 900  # 15 minutes

# ============================================
# DATA STORAGE
# ============================================

DATABASE_FILE = 'user_portfolios.json'

# ============================================
# MESSAGE TEMPLATES
# ============================================

MESSAGES = {
    'welcome': """
👋 Borsa Istanbul Bot'a Hoş Geldiniz!

📊 Bu bot ile gerçek zamanlı hisse fiyatlarını takip edebilirsiniz.
Komutlar için /help yazın.
    """,
    
    'help': """
🤖 **Borsa Bot - Komutlar**

/start - Botu başlat
/help - Bu yardım mesajını gör
/fiyat - Tüm hisselerin fiyatlarını gör
/ekle - Portföye hisse ekle
/sil - Portföyden hisse çıkar
/portfoy - Senin portföyünü gör
/tum_hisseler - Tüm takip edilen hisseleri gör

💡 Örnek: /ekle GARAN.IS
    """,
    
    'error': """
❌ Bir hata oluştu.
Lütfen tekrar deneyin veya @TalhaBorsa ile iletişime geçin.
    """,
    
    'portfolio_empty': """
📭 Portföyünüz boş.

Hisse eklemek için: /ekle GARAN.IS
    """,
}

# ============================================
# LOGGING
# ============================================

LOG_LEVEL = 'INFO'
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_FILE = 'bot.log'
