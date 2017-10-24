FROM python:3.6

COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt
COPY . /smzdm-subscribe
WORKDIR /smzdm-subscribe

CMD python main.py