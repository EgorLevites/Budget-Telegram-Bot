import sqlite3
import telebot
from telebot import types

# Connect to the SQLite database
conn = sqlite3.connect('expenses.db', check_same_thread=False)
cursor = conn.cursor()

# Create the table with an additional field 'is_closed' if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS budget (
        id INTEGER PRIMARY KEY,
        month TEXT NOT NULL,
        total_budget REAL NOT NULL,
        remaining_budget REAL NOT NULL,
        is_closed INTEGER DEFAULT 0
    )
''')

# Initialize the bot using the token
bot = telebot.TeleBot('YOUR_TOKEN')

# Global variable to store data about the month
user_data = {}

# Function to create the keyboard
def create_keyboard():
    cursor.execute('SELECT month FROM budget WHERE is_closed = 0 ORDER BY id DESC LIMIT 1')
    current_month = cursor.fetchone()

    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    
    if not current_month:
        start_button = types.KeyboardButton('Start New Month')
        keyboard.add(start_button)
    else:
        spend_button = types.KeyboardButton('Purchase')
        end_month_button = types.KeyboardButton('End Month')
        keyboard.add(spend_button, end_month_button)
    
    # The "Show All Months" button is always added
    show_months_button = types.KeyboardButton('Show All Months')
    keyboard.add(show_months_button)

    return keyboard

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 'Hello! I am here to help you manage your grocery expenses.', reply_markup=create_keyboard())

@bot.message_handler(func=lambda message: message.text == 'Start New Month')
def start_new_month(message):
    msg = bot.reply_to(message, 'Please specify the name of the month:')
    bot.register_next_step_handler(msg, ask_for_budget)

def ask_for_budget(message):
    month = message.text
    user_data[message.chat.id] = {'month': month}  # Save the month in the global variable
    msg = bot.reply_to(message, f'Please enter the budget for {month}:')
    bot.register_next_step_handler(msg, save_budget)

def save_budget(message):
    try:
        budget = float(message.text)
        month = user_data[message.chat.id]['month']
        cursor.execute('INSERT INTO budget (month, total_budget, remaining_budget) VALUES (?, ?, ?)', 
                       (month, budget, budget))  # Set the remaining budget equal to the total
        conn.commit()
        bot.reply_to(message, f'The budget for {month} has been successfully saved. Remaining balance: {budget} NIS.', reply_markup=create_keyboard())
    except ValueError:
        bot.reply_to(message, 'Please enter a valid amount.', reply_markup=create_keyboard())

@bot.message_handler(func=lambda message: message.text == 'Purchase')
def spend(message):
    cursor.execute('SELECT month FROM budget WHERE is_closed = 0 ORDER BY id DESC LIMIT 1')
    current_month = cursor.fetchone()
    if not current_month:
        bot.reply_to(message, 'No new month has been started. Please start a new month first.', reply_markup=create_keyboard())
        return

    msg = bot.reply_to(message, 'Please enter the purchase amount:')
    bot.register_next_step_handler(msg, process_spend)

def process_spend(message):
    try:
        amount = float(message.text)
        cursor.execute('SELECT remaining_budget FROM budget WHERE is_closed = 0 ORDER BY id DESC LIMIT 1')
        remaining_budget = cursor.fetchone()[0]
        new_remaining_budget = remaining_budget - amount

        cursor.execute('UPDATE budget SET remaining_budget = ? WHERE id = (SELECT MAX(id) FROM budget)', 
                       (new_remaining_budget,))
        conn.commit()

        bot.reply_to(message, f'You spent {amount} NIS. Remaining balance: {new_remaining_budget} NIS.', reply_markup=create_keyboard())
    except ValueError:
        bot.reply_to(message, 'Please enter a valid amount.', reply_markup=create_keyboard())

@bot.message_handler(func=lambda message: message.text == 'End Month')
def end_month(message):
    cursor.execute('SELECT id, month FROM budget WHERE is_closed = 0 ORDER BY id DESC LIMIT 1')
    current_month = cursor.fetchone()
    if not current_month:
        bot.reply_to(message, 'No active month to end.', reply_markup=create_keyboard())
        return

    # Update the status of the month as completed
    cursor.execute('UPDATE budget SET is_closed = 1 WHERE id = ?', (current_month[0],))
    conn.commit()

    bot.reply_to(message, f'The month of {current_month[1]} has been successfully ended.', reply_markup=create_keyboard())
    bot.send_message(message.chat.id, 'A new month can now be started.', reply_markup=create_keyboard())

@bot.message_handler(func=lambda message: message.text == 'Show All Months')
def show_months(message):
    cursor.execute('SELECT month, remaining_budget FROM budget WHERE is_closed = 1')
    months = cursor.fetchall()
    if months:
        response = "All months:\n"
        for month in months:
            response += f'Month: {month[0]}, Remaining balance: {month[1]} NIS\n'
    else:
        response = "No months found."
    bot.reply_to(message, response, reply_markup=create_keyboard())

# Function to run the bot
def main():
    bot.infinity_polling()

if __name__ == '__main__':
    main()
