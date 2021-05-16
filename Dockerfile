# build
FROM node:15-alpine3.10 as build-vue
WORKDIR /app
ENV PATH /app/node_modules/.bin:$PATH
COPY ./front-ar-maps/package*.json ./
RUN npm update
RUN npm install -g @vue/cli
RUN npm install
RUN npm update
COPY ./front-ar-maps .
RUN npm run build

# production
FROM nginx:stable-alpine as production
WORKDIR /app
RUN apk update && apk add --no-cache python3 && \
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --upgrade pip setuptools && \
    if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi && \
    if [[ ! -e /usr/bin/python ]]; then ln -sf /usr/bin/python3 /usr/bin/python; fi && \
    rm -r /root/.cache
RUN apk add --no-cache gcc libc-dev geos-dev 
RUN apk update && apk add postgresql-dev gcc g++ python3-dev musl-dev jpeg-dev zlib-dev 
COPY --from=build-vue /app/dist /usr/share/nginx/html
COPY ./nginx/default.conf /etc/nginx/conf.d/default.conf
COPY ./back-ar-maps/requirements.txt .

# RUN apk --update add build-base libxslt-dev

# RUN apk add --virtual .build-deps \
#         --repository http://dl-cdn.alpinelinux.org/alpine/edge/testing \
#         --repository http://dl-cdn.alpinelinux.org/alpine/edge/main \
#         gcc libc-dev geos-dev geos && \
#     runDeps="$(scanelf --needed --nobanner --recursive /usr/local \
#     | awk '{ gsub(/,/, "\nso:", $2); print "so:" $2 }' \
#     | xargs -r apk info --installed \
#     | sort -u)" && \
#     apk add --virtual .rundeps $runDeps

# RUN geos-config --cflags
# RUN pip install geos
RUN pip install -r requirements.txt
RUN pip install gunicorn
COPY ./back-ar-maps .
CMD gunicorn -b 0.0.0.0:5000 app:app --daemon && \
      sed -i -e 's/$PORT/'"$PORT"'/g' /etc/nginx/conf.d/default.conf && \
      nginx -g 'daemon off;'
