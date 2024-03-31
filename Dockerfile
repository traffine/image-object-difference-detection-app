FROM public.ecr.aws/lambda/python:3.10

WORKDIR /app

COPY poetry.lock pyproject.toml ./

RUN yum -y install mesa-libGL && \
  pip install --upgrade pip && \
  pip install poetry && \
  poetry config virtualenvs.create false && \
  poetry install --no-dev

COPY credentials.json efficientnet_v2_imagenet21k_l_feature_vector_2.onnx u2net.pth ./
COPY ./app ./app

ENV PYTHONPATH app
ENV DEBUG False
ENV GOOGLE_APPLICATION_CREDENTIALS credentials.json

CMD [ "main.handler" ]
