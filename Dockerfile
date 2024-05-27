# read the doc: https://huggingface.co/docs/hub/spaces-sdks-docker
# you will also find guides on how best to write your Dockerfile

FROM python:3.10

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt
RUN apt-get update \
&& apt-get install -y --no-install-recommends --no-install-suggests \
&& pip install --no-cache-dir --upgrade pip
RUN git clone https://github.com/z-mahmud22/Dlib_Windows_Python3.x.git
RUN python -m pip install dlib-19.22.99-cp310-cp310-win_amd64.whl
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y


COPY . .

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]
