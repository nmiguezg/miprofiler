FROM ubuntu:18.04 
ARG DEBIAN_FRONTEND=noninteractive

ENV TZ=Europe/Madrid
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN printf '#!/bin/sh\nexit 0' > /usr/sbin/policy-rc.d

RUN apt-get update && \
    apt-get install -y python2.7
RUN apt-get update && \
    apt-get install -y python
RUN apt-get update && \
#   # apt-get install -y python2.7 && \
#   # apt-get install -y py27parsing && \
	apt-get install -y wget build-essential libxml2-dev libxslt-dev libsm6 libxrender1 libfontconfig1 libicu-dev libhunspell-dev && \
	apt-get clean

RUN wget https://repo.anaconda.com/miniconda/Miniconda2-4.3.14-Linux-x86_64.sh && \
    chmod +x Miniconda2-4.3.14-Linux-x86_64.sh && \
    ./Miniconda2-4.3.14-Linux-x86_64.sh -b && echo 'PATH=/root/miniconda2/bin:$PATH' >> /etc/bash.bashrc && \
    rm /usr/bin/python && ln -s /root/miniconda2/bin/python /usr/bin/python
RUN /root/miniconda2/bin/conda install -y \
  pip \
  numpy \
  pandas \
  scikit-learn \
  nltk \
  h5py \
  matplotlib \
  lxml

RUN python -c "import nltk; nltk.download('stopwords'); nltk.download('punkt'); nltk.download('wordnet')" 
RUN ln -s /root/miniconda2/bin/pip /usr/bin/pip
RUN pip install hunspell
RUN pip install pytest
RUN pip install pytest-pep8
RUN pip install beautifulsoup4
RUN pip install simplejson
RUN pip install pandas_confusion
RUN pip install regex==2015.06.02
RUN pip install xgboost
RUN apt-get install -f -y python3-pip
RUN pip install polyglot 
RUN pip3 install polyglot
RUN pip install pyyaml tictacs==0.0.1  beautifulsoup textblob

WORKDIR /var/www
RUN mkdir -p /root/hunspell
ADD . .
RUN pip install -e .

ADD https://cgit.freedesktop.org/libreoffice/dictionaries/plain/nl_NL/nl_NL.aff  /root/hunspell/nl_NL.aff
ADD https://cgit.freedesktop.org/libreoffice/dictionaries/plain/nl_NL/nl_NL.dic /root/hunspell/nl_NL.dic
ADD https://cgit.freedesktop.org/libreoffice/dictionaries/plain/en/en_US.aff /root/hunspell/en_US.aff
ADD https://cgit.freedesktop.org/libreoffice/dictionaries/plain/en/en_US.dic /root/hunspell/en_US.dic
ADD https://cgit.freedesktop.org/libreoffice/dictionaries/plain/es/es_ES.dic /root/hunspell/es_ANY.dic
ADD https://cgit.freedesktop.org/libreoffice/dictionaries/plain/es/es_ES.aff /root/hunspell/es_ANY.aff
RUN apt-get install -y libgl1-mesa-glx
RUN pip install flask gunicorn

EXPOSE 5000