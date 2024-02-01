# English Learning Project

This web project and Telegram bot were created to help multilingual teachers give access to different types of materials to students. You can find web demo [here](https://nayalang.onrender.com)

## Installation and Set-up

To use the web project and Telegram bot, follow these steps:

1. Clone or download the repository.
2. Install Docker and Docker Compose.
3. Run the command `docker-compose up`. Docker will create 3 containers: web, bot, and db.
   - To use the web admin page, create a superuser account. Follow these steps:
     - Enter the command `docker ps` to get the container ID.
     - Enter the command `docker exec -it (container id) /bin/bash` to enter the container.
     - Inside the container, run `python manage.py createsuperuser` and follow the instructions to create a superuser.

4. To configure the bot, change the host data in `create_bot.py`:
    ```python
    bot = Bot(your_token)
    host = "your_web_host"
    my_admin = "https://t.me/your_admin_profile"
    ```

    - Create a Telegram chat and a Telegram bot from BotFather.
    - Make the Telegram bot an admin of the created chat.
    - Copy the Telegram token and paste it into `create_bot.py` as `bot=Bot(token)`.
    - Make changes in `mysql_con.py` to fill all the needed columns for connecting to the database.
    - Run the project's Python file `lang_bot.py`.

5. Change the data in `english_learning.settings.py` to your needs:
    ```python
    ALLOWED_HOSTS = []
    DATABASES = []
    ```

6. Create a `.env` file and fill in the data:
    ```
    DB_NAME=example_databasename
    DB_PASS=example_password
    DB_USER=example_databaseuser
    EMAIL=example@gmail.com   # Email address from which updated passwords will be sent to users if they forget it
    EMAIL_PASS=example_password  # Special email password for accessing your email account from the API, provided by your email provider
    ```

## Usage

Once the installation and set-up are completed, users can start using the functionality provided.
First, add the bot to a chat. If the bot doesn't write a message automatically, write the command `/start` or send any message to the bot in a private chat.
After that, follow the instructions of the bot. The bot will show you buttons.

## Credits

The English Learning Project was developed by Oleksandr Kiosia. This project was developed with the help of the following technologies:

- Python
- Django
- MySQL
- aiogram 
- HTML and CSS
- Bootstrap
- JavaScript
- Docker 
- Docker Compose



