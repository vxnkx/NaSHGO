import os
from telegram import Bot
from telegram.ext import Application
import asyncio
from .report import generate_html_report
import qrcode
from PIL import Image

class TelegramReporter:
    def __init__(self, config):
        self.bot = Bot(token=config['telegram_bot_token'])
        self.chat_id = config['telegram_chat_id']
    
    async def send_georeport(self, results, username):
        """Send interactive report to Telegram"""
        if not results:
            await self.bot.send_message(self.chat_id, "❌ No geolocated images found")
            return
        
        # Generate QR code to HTML report
        report_path = f"output/{username}_report.html"
        generate_html_report(results, report_path)
        
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(f"file://{os.path.abspath(report_path)}")
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color="black", back_color="white")
        qr_path = f"output/{username}_qr.png"
        qr_img.save(qr_path)
        
        # Send summary
        stats = f"📍 **{len(results)} Geolocated Images**\n"
        stats += f"🎯 Target: @{username}\n"
        stats += f"📈 Coverage: {len(set(r['location']['city'] for r in results))} cities"
        
        await self.bot.send_photo(
            self.chat_id, 
            photo=open(qr_path, 'rb'),
            caption=stats,
            parse_mode='Markdown'
        )
        
        # Send sample image + GPS popup
        sample = results[0]
        await self.bot.send_photo(
            self.chat_id,
            photo=sample['url'],
            caption=f"📍 {sample['location']['address']}\n🌐 lat:{sample['gps']['lat']:.6f}"
        )
