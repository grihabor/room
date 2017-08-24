FROM python:3.6
MAINTAINER Borodin Gregory <grihabor@mail.ru>

RUN pip3 install svgwrite==1.1.11

ADD src /project/src

WORKDIR /project/src

CMD python3 run.py
