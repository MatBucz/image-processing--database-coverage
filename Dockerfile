FROM jjanzic/docker-python3-opencv

COPY requirements.txt /requirements.txt

RUN pip install -r /requirements.txt
RUN apt-get update && apt-get install -y font-manager
RUN echo ttf-mscorefonts-installer msttcorefonts/accepted-mscorefonts-eula select true | debconf-set-selections


# ---------
RUN echo "deb http://httpredir.debian.org/debian buster main contrib non-free" > /etc/apt/sources.list \
    && echo "deb http://httpredir.debian.org/debian buster-updates main contrib non-free" >> /etc/apt/sources.list \
    && echo "deb http://security.debian.org/ buster/updates main contrib non-free" >> /etc/apt/sources.list \
    && echo "ttf-mscorefonts-installer msttcorefonts/accepted-mscorefonts-eula select true" | debconf-set-selections \
    && apt-get update \
    && apt-get install -y \
        ttf-mscorefonts-installer \
    && apt-get clean \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*
# ----------

RUN apt-get update -q \
    && apt-get install -qy build-essential wget libfontconfig1 \
    && rm -rf /var/lib/apt/lists/*

RUN apt-get update -q && apt-get install -y texlive dvipng ghostscript-x
RUN apt-get install -y dvipng texlive-latex-extra texlive-fonts-recommended  cm-super

RUN fc-cache -f -v

RUN rm /.cache/matplotlib -fr