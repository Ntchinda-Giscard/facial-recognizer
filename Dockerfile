# read the doc: https://huggingface.co/docs/hub/spaces-sdks-docker
# you will also find guides on how best to write your Dockerfile

FROM python:3.10

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt
RUN apt-get update \
&& apt-get install -y --no-install-recommends --no-install-suggests \
&& pip install --no-cache-dir --upgrade pip

RUN apt-get install -y --fix-missing \
    build-essential \
    cmake \
    gfortran \
    git \
    wget \
    curl \
    graphicsmagick \
    libgraphicsmagick1-dev \
    libatlas-base-dev \
    libavcodec-dev \
    libavformat-dev \
    libgtk2.0-dev \
    libjpeg-dev \
    liblapack-dev \
    libswscale-dev \
    pkg-config \
    python3-dev \
    python3-numpy \
    software-properties-common \
    zip \
    && apt-get clean && rm -rf /tmp/* /var/tmp/*

RUN cd ~ && \
    mkdir -p dlib && \
    git clone -b 'v19.9' --single-branch https://github.com/davisking/dlib.git dlib/ && \
    cd  dlib/ && \
    python3 setup.py install --yes USE_AVX_INSTRUCTIONS

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y


# Create the directories and set permissions
RUN mkdir /code/facedata /code/UPLOAD /code/FIND && chmod -R 777 /code/facedata /code/UPLOAD /code/FIND

# Create a non-root user and group
RUN groupadd -r appgroup && useradd -r -g appgroup -d /code -s /sbin/nologin appuser

# Change ownership of the /code directory and the newly created directories
RUN chown -R appuser:appgroup /code /code/facedata /code/UPLOAD /code/FIND


COPY . .

CMD ["python", "app.py"]
