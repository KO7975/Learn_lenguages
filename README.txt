This web progect and telegram_bot created for halping multi-lenguage teacher give acces to different type of materials to students.

## Installation and Set-up
To use the WEB Project and telegram_bot, complete the following steps:

1. Clone or download the repository
2. For instaletion you wil need Docker and Docker Compose
3. Write command: 'docker-compose up'. Docker will create 3 containers web, bot and db.
    -for using web admin page, you need create superuser account, for this yo need come in 
    working web container:  enter command: docker ps 
                            then copy container id
                            and enter next command:  docker exec -it (container id) /bin/bash
                            inside the container next command: python manage.py createsuperuser
                            and following the instractions you will create superuser
                            use superuser data for ligin on web page.

4. For proper work you will need to change Host data in create_bot.py :
bot = Bot(your_token)
host= "your_web_host"
my_admin= "https://t.me/your_admin_profile"

- Create telegram chat and telegram bot from BotFather in telegram. 
- Make telegram-bot admin of created chat.
- Copy telegram token and past to create_bot.py bot=Bot(token)
- Make changes in mysql_con.py fill all neded columns for connacting to db
-  Run the project's Python lang_bot.py file
5. Also you will need to change data in english_learning.settings.py on that what you need: 
    ALLOWED_HOSTS=[]
    DATABASES=[]
6. Create .env and fill data:
    DB_NAME=example_databasename
    DB_PASS=example_password
    DB_USER=example_databaseuser
    EMAIL=example@gmail.com   -   email adress from what will be sending updated pasword to users if thay forget it
    EMAIL_PASS=example_password - specil email password for giving acces to your email accaunt from API, from your email provider

## Usage
Once the installation and set-up is completed, users can start using the functionality provided.
First added to chat, if bot dosn't write massage automaticly write command '/start' or write to bot any massage in ptivat chat.
After that  folow the instractions of bot , bot show you buttons .
 

## Credits
The ENGLISH_LEARNING Project was developed by Oleksandr Kiosia. This project was developed with the help of the following

- Python
- MySQL
- aiogram 
- Django web framework
- HTML and CSS
- Bootstrap
- JS
- Docker 
- Docker-compose


