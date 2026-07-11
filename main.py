#!/usr/bin/env python3
"""
Borsa Istanbul Telegram Bot
Gerçek zamanlı hisse fiyatlarını takip edin
"""

import logging
import json
import os
from datetime import datetime
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, ConversationHandler
from telegram.constants import ChatAction
import yfinance as yf
import pandas as pd
from config import *

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# User data storage
USER_DATA_FILE = 'user_portfolios.json'

def load_user_data():
    """Load user portfolios from JSON file"""
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_user_data(data):
    """Save user portfolios to JSON file"""
    with open(USER_DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def get_stock_price(symbol):
    """Get current stock price from yfinance"""
    try:
        stock = yf.Ticker(symbol)
        hist = stock.history(period='1d')
        
        if hist.empty:
            return None
        
        current_price = hist['Close'].iloc[-1]
        return float(current_price)
    except Exception as e:
        logger.error(f"Error fetching price for {symbol}: {e}")
        return None

def format_price_message(symbol, price):
    """Format price message with emoji"""
    if price is None:
        return f"❌ {symbol} - Veri alınamadı"
    
    return f"📊 {symbol}: ₺{price:.2f}"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start command handler"""
    user = update.effective_user
    user_data = load_user_data()
    
    if str(user.id) not in user_data:
        user_data[str(user.id)] = {
            'username': user.username or user.first_name,
            'portfolio': [],
            'created_at': datetime.now().isoformat()
        }
        save_user_data(user_data)
    
    welcome_msg = f"""
👋 Merhaba {user.first_name}!

Borsa Istanbul Telegram Bot'a Hoş Geldiniz! 🚀

📊 Bu bot ile gerçek zamanlı hisse fiyatlarını takip edebilirsiniz.

Komutlar için /help yazın.
    """
    await update.message.reply_text(welcome_msg)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Help command handler"""
    help_text = """
🤖 **Mevcut Komutlar:**

/start - Botu başlat
/help - Bu yardım mesajını gör
/fiyat - Tüm hisselerin fiyatlarını gör
/ekle - Portföye hisse ekle
/sil - Portföyden hisse çıkar
/portfoy - Senin portföyünü gör
/tum_hisseler - Tüm takip edilen hisseleri gör

📈 **Örnek Hisse Kodları:**
• GARAN.IS - Garanti Bank
• ASELS.IS - Aselsan
• THYAO.IS - Turkish Airlines
• AKBNK.IS - Akbank
• TUPRS.IS - Tüpraş

Herhangi bir sorun için @TalhaBorsa ile iletişime geçin.
    """
    await update.message.reply_text(help_text)

async def get_prices(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Get all monitored stock prices"""
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
    
    message = "📊 **Borsa Istanbul - Hisse Fiyatları**\n\n"
    
    for symbol in DEFAULT_STOCKS:
        price = get_stock_price(symbol)
        message += format_price_message(symbol, price) + "\n"
    
    message += f"\n⏰ Son güncelleme: {datetime.now().strftime('%H:%M:%S')}"
    
    await update.message.reply_text(message, parse_mode='Markdown')

async def add_to_portfolio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Add stock to user portfolio"""
    user_id = str(update.effective_user.id)
    user_data = load_user_data()
    
    if not context.args:
        await update.message.reply_text(
            "❌ Lütfen hisse kodu yazın.\n"
            "Örnek: /ekle GARAN.IS"
        )
        return
    
    symbol = context.args[0].upper()
    
    if user_id not in user_data:
        user_data[user_id] = {
            'username': update.effective_user.username or update.effective_user.first_name,
            'portfolio': [],
            'created_at': datetime.now().isoformat()
        }
    
    if symbol not in user_data[user_id]['portfolio']:
        user_data[user_id]['portfolio'].append(symbol)
        save_user_data(user_data)
        await update.message.reply_text(f"✅ {symbol} portföyünüze eklendi!")
    else:
        await update.message.reply_text(f"ℹ️ {symbol} zaten portföyünüzde var.")

async def remove_from_portfolio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Remove stock from user portfolio"""
    user_id = str(update.effective_user.id)
    user_data = load_user_data()
    
    if not context.args:
        await update.message.reply_text(
            "❌ Lütfen hisse kodu yazın.\n"
            "Örnek: /sil GARAN.IS"
        )
        return
    
    symbol = context.args[0].upper()
    
    if user_id in user_data and symbol in user_data[user_id]['portfolio']:
        user_data[user_id]['portfolio'].remove(symbol)
        save_user_data(user_data)
        await update.message.reply_text(f"✅ {symbol} portföyünüzden çıkarıldı!")
    else:
        await update.message.reply_text(f"❌ {symbol} portföyünüzde bulunamadı.")

async def view_portfolio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """View user portfolio"""
    user_id = str(update.effective_user.id)
    user_data = load_user_data()
    
    if user_id not in user_data or not user_data[user_id]['portfolio']:
        await update.message.reply_text(
            "📭 Portföyünüz boş.\n"
            "Hisse eklemek için /ekle GARAN.IS yazın."
        )
        return
    
    portfolio = user_data[user_id]['portfolio']
    message = "📈 **Senin Portföyün**\n\n"
    
    for symbol in portfolio:
        price = get_stock_price(symbol)
        message += format_price_message(symbol, price) + "\n"
    
    message += f"\n⏰ Son güncelleme: {datetime.now().strftime('%H:%M:%S')}"
    
    await update.message.reply_text(message, parse_mode='Markdown')

async def list_all_stocks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """List all available stocks"""
    message = "📊 **Takip Edilen Tüm Hisseler:**\n\n"
    
    for i, symbol in enumerate(DEFAULT_STOCKS, 1):
        message += f"{i}. {symbol}\n"
    
    message += f"\n💡 Portföyünüze eklemek için: /ekle GARAN.IS"
    
    await update.message.reply_text(message, parse_mode='Markdown')

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Error handler"""
    logger.error(f"Update {update} caused error {context.error}")
    await update.message.reply_text(
        MESSAGES['error'] + "\n\nLütfen daha sonra tekrar deneyin."
    )

def main():
    """Start the bot"""
    # Create the Application
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    
    # Add command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("fiyat", get_prices))
    application.add_handler(CommandHandler("ekle", add_to_portfolio))
    application.add_handler(CommandHandler("sil", remove_from_portfolio))
    application.add_handler(CommandHandler("portfoy", view_portfolio))
    application.add_handler(CommandHandler("tum_hisseler", list_all_stocks))
    
    # Add error handler
    application.add_error_handler(error_handler)
    
    # Start the bot
    logger.info("Bot başladı! 🚀")
    print("🤖 Borsa Istanbul Bot çalışıyor... (Durdurmak için Ctrl+C)")
    
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
