FROM python:3.6
MAINTAINER Borodin Gregory <grihabor@mail.ru>

RUN pip3 install svgwrite==1.1.11

WORKDIR /project/src

CMD /bin/python3 run.py
