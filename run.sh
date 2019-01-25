#!/bin/sh

python3 -u archillect.py &

envsubst < /etc/nginx/conf.d/mysite.template > /etc/nginx/conf.d/default.conf

nginx -g 'daemon off;'
