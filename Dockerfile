FROM python:3.11-slim
# Recibir build arguments
ARG BUILD_DATE
ARG VCS_REF
ARG VERSION

WORKDIR /code

ENV FLASK_APP=app/app.py \
  FLASK_RUN_HOST=0.0.0.0\
  APP_VERSION=${VERSION} \
  GIT_SHA=${VCS_REF} \
  BUILD_DATE=${BUILD_DATE}

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["flask", "run", "--debug"]