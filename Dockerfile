FROM alpine:3.7

RUN apk add --update --no-cache --virtual=run-deps \
  python3 \
  build-base \
  py-lxml \
  ca-certificates \
  nginx \
  gettext

ENV SLEEP_SECONDS 60
ENV YIELD_TIME_SECONDS 5
ENV RANGE 5
ENV INDEX_FILE /opt/site/index.html
ENV LISTEN_PORT 80

WORKDIR /opt/app
CMD ["./run.sh"]

RUN mkdir -p /var/log/nginx && \
    mkdir -p /run/nginx && \
    ln -sf /dev/stdout /var/log/nginx/access.log && \
    ln -sf /dev/stdout /var/log/nginx/error.log && \
    mkdir -p /opt/site

COPY etc/nginx.conf /etc/nginx/conf.d/mysite.template
COPY etc/index.html /opt/site/

COPY run.sh /opt/app/
RUN chmod +x /opt/app/run.sh

COPY requirements.txt /opt/app/
RUN pip3 install --no-cache-dir -r /opt/app/requirements.txt

COPY app /opt/app/
