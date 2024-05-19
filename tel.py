import sqlite3
import logging
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
import telegram
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
from datetime import datetime, timedelta
import random

# Configure logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Bot token
TOKEN = '6396781680:AAF-919EBE9TMpALWfl7R7Y5PfqhvoJBuvo'

# Constants for callback data
T_MOBILE_IP = 't_mobile_ip'
ATT_IP = 'att_ip'
SUBMIT_PAYMENT_PROOF = 'submit_payment_proof'

# Function to create database and tables if they don't exist
def setup_database():
    conn = sqlite3.connect('bot_data.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        chat_id INTEGER PRIMARY KEY,
        last_activity TIMESTAMP,
        last_ip_change TIMESTAMP,
        active INTEGER DEFAULT 1
    )
    ''')
    conn.commit()
    conn.close()

# Function to update user activity timestamp
def update_activity(chat_id):
    conn = sqlite3.connect('bot_data.db')
    cursor = conn.cursor()
    cursor.execute('INSERT OR IGNORE INTO users (chat_id, last_activity) VALUES (?, ?)', (chat_id, datetime.now()))
    cursor.execute('UPDATE users SET last_activity = ? WHERE chat_id = ?', (datetime.now(), chat_id))
    conn.commit()
    conn.close()

# Start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("Received /start command")
    keyboard = [
        [KeyboardButton("Subscribe to Earn (30 days)")],
        [KeyboardButton("Renew Subscription")],
        [KeyboardButton("SSN Finder")],
        [KeyboardButton("Account Create IP")],
        [KeyboardButton("T-Mobile USA Working IP")],
        [KeyboardButton("AT&T Working IP")],
        [KeyboardButton("Change IP")],
        [KeyboardButton("Class Video Link")],
        [KeyboardButton("Live Meeting Links")],
        [KeyboardButton("Daily IP")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text('Please choose an option:', reply_markup=reply_markup)
    update_activity(update.message.chat_id)

# Health check command handler
async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("Received /ping command")
    await update.message.reply_text("pong")

# Function to handle Account Create IP
async def account_create_ip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("Received /accountcreateip command")
    await update.message.reply_text("Here is your unique IP address for account creation: 192.168.1.1")
    update_activity(update.message.chat_id)

# Function to handle Daily IP
async def daily_ip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("Received /dailyip command")
    await update.message.reply_text("Here is your unique Daily IP address: 192.168.1.2")
    update_activity(update.message.chat_id)

# Button callback handler
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    logger.info(f"Button {query.data} pressed")

    response_text = {
        'subscribe': 'Subscription for 30 days via bkash. \n\n Payment Link: [Click Here](https://shop.bkash.com/survey-world-of-farhan--usa-su/paymentlink)',
        'renew': 'Renew your subscription.',
        'ssn_finder': 'SSN হচ্ছে USA এর একজন মানুষের তথ্য। এই তথ্য বের করতে হলে আপনাকে আপনের মোবাইল বা কম্পিউটার এর মধ্যে USA এর আইপি সেটাপ করে (truepeoplesearch.com) এই ওয়েবসাইট এ গিয়ে SSN নিতে পারবেন\n\n বিস্তারিত জানতে নিচের দেয়া ভিডিও তে ক্লিক করে দেখে আসতে পারেন: [ভিডিও লিঙ্ক](https://youtu.be/GoEFOcJ7YYE)',
        'account_create_ip': 'Account Create IP',
        T_MOBILE_IP: 'Choose a location:',
        ATT_IP: 'Choose a location:',
        'change_ip': 'Change IP service.',
        'class_video': 'Admin will share the class video link manually.',
        'live_meeting': 'Admin will share the live meeting links manually.',
        'daily_ip': 'Daily IP.'
    }

    # Get the response text based on the button pressed
    response = response_text.get(query.data)

    # Reply with the corresponding text
    if response:
        await query.message.reply_text(response, parse_mode='Markdown')
    else:
        await query.message.reply_text("Button pressed")

# Function to handle Change IP
async def change_ip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("Received /changeip command")
    chat_id = update.message.chat_id
    conn = sqlite3.connect('bot_data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT last_ip_change FROM users WHERE chat_id = ?', (chat_id,))
    last_ip_change = cursor.fetchone()
    conn.close()

    if last_ip_change is None or datetime.now() - datetime.fromisoformat(last_ip_change[0]) >= timedelta(days=1):
        sentences = [
            "This is a random sentence for IP change.",
            "Another random sentence for IP change.",
            "Yet another random sentence for IP change."
        ]
        random_sentence = random.choice(sentences)
        await update.message.reply_text(random_sentence)

        conn = sqlite3.connect('bot_data.db')
        cursor = conn.cursor()
        cursor.execute('UPDATE users SET last_ip_change = ? WHERE chat_id = ?', (datetime.now(), chat_id))
        conn.commit()
        conn.close()
    else:
        await update.message.reply_text("You can change IP once a day.")

# Function to handle SSN Finder
async def ssn_finder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("Received /ssnfinder command")
    ssn_guide = """SSN stands for Social Security Number. To obtain this information, you'll need to set up a USA IP on your mobile or computer and visit the website truepeoplesearch.com. For more detailed instructions, please watch the following video: [Video Link](https://youtu.be/GoEFOcJ7YYE)"""
    await update.message.reply_text(ssn_guide, parse_mode='Markdown')
    update_activity(update.message.chat_id)

async def subscribe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("Received subscription request")
    subscription_info = """সার্ভে কি? সার্ভে মূলর্ া এি ধরর্ের করকভউ টাইর্ের িাজ এখার্ে কিকভন্ন কিাম্পাকে ওর্েিসাইর্টর মাধযর্ম আমার্ের কি কের্ে প্রডাক্ট জকরে ির্র থার্ি USA সার্ভে িরর্ কি কি লাগর্ি? Residensial IP Original USA Address Mobile , Laptop Or Desktop (এিটা হর্লই হে) িযাকসি ইংকলশ জাের্ হর্ি। কেট ব্রাউজজং সম্পর্িে কমাটামুটট ধারণা থাির্ হর্ি। দেকেি ৩- ৫ ঘন্টা টাইম কের্ হর্ি।
আমার্ের আইকে এর মূলয ৭০০ টািা আর সার্থ কশোর িাউল কের্ হর্ল আরও ২০০ টািা যকে আইকে আর িাউল এির্ে কের্ চাে াহর্ল ৯০০ টািা কের্মন্ট িরর্ কের্চর কলঙ্ক এ কিি িরুণ কের্মন্ট ির্র অিশযই জিেশট সািকমট িরর্িে কের্মন্ট কলঙ্ক - [Payment Link](https://shop.bkash.com/survey-world-of-farhan--usa-su/paymentlink) 

অথবা,

💵💵 নগদ 💵💵- 01623636904

সেন্ড মানি (Send Money) করবেন

💵💵 রকেট 💵💵- 01623636904

সেন্ড মানি (Send Money) করবেন

ব্যাংক থেকে পাঠাতে চাইলে নিচের CITY BANK অ্যাকাউন্ট এ পাঠিয়ে Invoice শেয়ার করবেন

Bank Name  - City Bank
Bank Account Number - 1781580044245
Account Name : MD Monour Hossain

পেমেন্ট শেষ হলে Submit Payment Proof এ গিয়ে পেমেন্ট এর স্ক্রিনশট বা পেমেন্ট এর তথ্য জমা দিন।"""

    keyboard = [[InlineKeyboardButton("Submit Payment Proof", callback_data=SUBMIT_PAYMENT_PROOF)]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(subscription_info, parse_mode='Markdown', reply_markup=reply_markup)
    update_activity(update.message.chat_id)

# Function to handle Live Meeting Links
async def live_meeting_links(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("Received /livemeetinglinks command")
    await update.message.reply_text("Admin will share the live meeting links manually.")
    update_activity(update.message.chat_id)

# Function to handle T-Mobile USA Working IP
async def t_mobile_ip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("Received /t_mobile_ip command")
    keyboard = [
        [InlineKeyboardButton("New York", callback_data=f"{T_MOBILE_IP}_new_york")],
        [InlineKeyboardButton("Los Angeles", callback_data=f"{T_MOBILE_IP}_los_angeles")],
        [InlineKeyboardButton("Chicago", callback_data=f"{T_MOBILE_IP}_chicago")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Choose a location for T-Mobile IP:', reply_markup=reply_markup)
    update_activity(update.message.chat_id)

# Function to handle AT&T Working IP
async def att_ip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("Received /att_ip command")
    keyboard = [
        [InlineKeyboardButton("New York", callback_data=f"{ATT_IP}_new_york")],
        [InlineKeyboardButton("Los Angeles", callback_data=f"{ATT_IP}_los_angeles")],
        [InlineKeyboardButton("Chicago", callback_data=f"{ATT_IP}_chicago")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Choose a location for AT&T IP:', reply_markup=reply_markup)
    update_activity(update.message.chat_id)

# Function to handle Class Video Link
async def class_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("Received /class_video command")
    await update.message.reply_text("Admin will share the class video link manually.")
    update_activity(update.message.chat_id)

# Function to handle text messages
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    logger.info(f"Received message: {text}")
    
    if text == "Subscribe to Earn (30 days)":
        await subscribe(update, context)
    elif text == "Renew Subscription":
        await subscribe(update, context)  # Assuming renew subscription is similar to subscribe
    elif text == "SSN Finder":
        await ssn_finder(update, context)
    elif text == "Account Create IP":
        await account_create_ip(update, context)
    elif text == "T-Mobile USA Working IP":
        await t_mobile_ip(update, context)
    elif text == "AT&T Working IP":
        await att_ip(update, context)
    elif text == "Change IP":
        await change_ip(update, context)
    elif text == "Class Video Link":
        await class_video(update, context)
    elif text == "Live Meeting Links":
        await live_meeting_links(update, context)
    elif text == "Daily IP":
        await daily_ip(update, context)
    else:
        await update.message.reply_text("Sorry, I didn't understand that command.")

def main():
    # Setup the database
    setup_database()

    # Create the application
    application = Application.builder().token(TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("ping", ping))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    application.add_handler(CallbackQueryHandler(button))

    # Start the Bot
    application.run_polling()

if __name__ == '__main__':
    main()
