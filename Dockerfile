FROM python:3

LABEL org.label-schema.license="GPL-3.0" \
      org.label-schema.vcs-url="https://github.com/Bullrich/Diario-Opositor-Bot" \
      org.label-schema.vendor="Diario-Opositor-Bot" \
      maintainer="Javier Bullrich <javierbullrich@gmail.com>"

RUN mkdir /etc/dob

COPY requirements.txt /etc/dob/

WORKDIR /etc/dob/

RUN pip install -r requirements.txt

COPY . /etc/dob/

CMD ["python", "DobServer.py"]