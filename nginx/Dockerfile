FROM nginx

WORKDIR /etc/nginx

RUN mkdir sites-available
RUN mkdir log

COPY ./sites-available /etc/nginx/sites-available
COPY ./nginx.conf /etc/nginx/nginx.conf
COPY ./datacluster /etc/nginx/datacluster

CMD ["ln -s /etc/nginx/sites-available/datacluster.conf /etc/nginx/conf.d/datacluster.conf"]

CMD ["nginx", "-g", "daemon off;"]
