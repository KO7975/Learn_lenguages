FROM python:3.10.5
WORKDIR /english_learning
COPY . /english_learning/
RUN pip install --upgrade pip
RUN pip3 install -r ./requirements.txt

CMD [ "python", "manage.py", "runserver" ]

 
