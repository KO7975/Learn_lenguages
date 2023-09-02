FROM python:3.10.5
WORKDIR /bot
COPY . /bot/
RUN pip install --upgrade pip
RUN pip3 install -r ./requirements.txt

EXPOSE 5000

CMD [ "python", "lang_bot.py", "0.0.0.0:5000" ]

 
