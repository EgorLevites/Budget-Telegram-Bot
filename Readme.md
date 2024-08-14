
# Telegram Budget Management Bot

This is a Telegram bot designed to help you manage your budget for groceries. The bot allows you to start a new month, set a budget, track your expenses, and view your remaining balance. It also provides the option to view all past months with their respective budgets and remaining balances.

## Features

- **Start New Month:** Begin a new month and set a budget.
- **Record Purchases:** Log your purchases, and the bot will deduct them from your remaining budget.
- **End Month:** Finish the current month and save the remaining balance.
- **View All Months:** Display a list of all months with their budgets and remaining balances.

## Commands and Functionalities

- **/start:** Start the bot and display the main menu.
- **Start New Month:** Start a new month by providing the month name and setting a budget.
- **Record Purchase:** Enter the amount spent, and it will be deducted from your remaining budget.
- **End Month:** Mark the current month as completed and save the final balance.
- **Show All Months:** View a list of all completed months with their budgets and remaining balances.

## Installation and Deployment

### Prerequisites

- Python 3.x
- `pyTelegramBotAPI` library
- `sqlite3` for database management

### Installation Steps

1. **Clone the repository:**

    ```bash
    git clone https://github.com/your-repo/telegram-budget-bot.git
    cd telegram-budget-bot
    ```

2. **Install required dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

3. **Set up your bot token:**

    Replace `'YOUR_BOT_TOKEN'` in the bot code with your actual Telegram bot token.

4. **Run the bot locally:**

    ```bash
    python main.py
    ```

5. **Deploy to Heroku:**

    - Install the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli).
    - Log in to Heroku using `heroku login`.
    - Create a new Heroku app using `heroku create`.
    - Push your code to Heroku using `git push heroku master`.
    - Scale your bot using `heroku ps:scale worker=1`.

## Usage

1. Start the bot by typing `/start`.
2. Use the on-screen buttons to manage your budget.
3. Track your expenses, and view past months' summaries.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.
