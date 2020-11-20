FROM ubuntu:18.04

ENV TZ=Asia/Seoul
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN cp /etc/apt/sources.list /etc/apt/sources.list~
RUN sed -Ei 's/^# deb-src /deb-src /' /etc/apt/sources.list
RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get build-dep -y python2.7 hexedit
RUN apt-get update
RUN apt-get install -y wget git-all build-essential unzip tar vim git python-pip \
    python-setuptools sudo apt-utils autoconf autoconf-archive \
    libpqxx-dev libboost-regex-dev libsqlite3-dev --no-install-recommends --assume-yes

WORKDIR /code

COPY . . 
CMD ["python", "compare-perf.py"]
