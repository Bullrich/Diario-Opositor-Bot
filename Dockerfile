FROM python:2

RUN mkdir /etc/dob

COPY requirements.txt /etc/dob/

WORKDIR /etc/dob/

RUN pip install -r requirements.txt

COPY . /etc/dob/

CMD ["python", "diario_opositor_bot.py"]