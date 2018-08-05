FROM python:3

MAINTAINER Javier Bullrich "javierbullrich@gmail.com"

RUN mkdir /etc/dob

COPY requirements.txt /etc/dob/

WORKDIR /etc/dob/

RUN pip install -r requirements.txt

COPY . /etc/dob/

CMD ["python", "DobServer.py"]