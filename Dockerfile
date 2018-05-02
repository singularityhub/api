FROM continuumio/miniconda3
MAINTAINER vsochat@stanford.edu

# docker build -t vanessa/container-api .

# GOOGLE_APPLICATION_CREDENTIALS should be exported
# docker run -e GOOGLE_APPLICATION_CREDENTIALS vanessa/container-api

ENV DEBIAN_FRONTEND noninteractive
ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8

RUN apt-get update 
RUN apt-get -y install build-essential automake
RUN apt-get -y install apt-utils cmake wget unzip libffi-dev libssl-dev \
                       libtool autotools-dev automake autoconf git \
                       libarchive-dev squashfs-tools uuid-dev \
                       vim jq aria2 nginx

ENV PATH /opt/conda/bin:$PATH

# Install singularity 2.5
RUN git clone https://github.com/singularityware/singularity.git \
    && cd singularity && ./autogen.sh && ./configure --prefix=/usr/local \
    && make && make install

# Install google python storage client
RUN /opt/conda/bin/pip install --upgrade pip && \
    /opt/conda/bin/pip install --upgrade google-cloud-storage && \
    /opt/conda/bin/pip install spython==0.0.32

# Install container-diff and singularity container-diff
RUN curl -LO https://storage.googleapis.com/container-diff/latest/container-diff-linux-amd64 && \
    chmod +x container-diff-linux-amd64 && mv container-diff-linux-amd64 /usr/local/bin/container-diff && \
    curl -LO https://raw.githubusercontent.com/singularityhub/container-diff/master/analyze-singularity.sh && \
    chmod +x analyze-singularity.sh && mv analyze-singularity.sh /usr/local/bin/analyze-singularity.sh
  
ADD . /code
WORKDIR /code
RUN mkdir -p /data

# Clean up
RUN apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# These will be provided at runtime, do not exist in container!
ENV GOOGLE_APPLICATION_CREDENTIALS /credentials.json

ENTRYPOINT ["/opt/conda/bin/python", "/code/generate.py"]
