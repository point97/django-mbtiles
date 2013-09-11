FROM makinacorpus/pythonbox
MAINTAINER Mathieu Leplatre "mathieu.leplatre@makina-corpus.com"

RUN apt-get install -y git nginx

ADD . /opt/apps/livembtiles
RUN mkdir -p /opt/apps/livembtiles/static

RUN mkdir -p /data/makinacorpus
ENV MBTILES_ROOT /data/makinacorpus

RUN (cd /opt/apps/livembtiles && git remote rm origin)
RUN (cd /opt/apps/livembtiles && git remote add origin https://github.com/makinacorpus/django-mbtiles.git)
RUN (cd /opt/apps/livembtiles && make install deploy)
RUN /opt/apps/livembtiles/bin/pip install uwsgi

ADD .docker/run.sh /usr/local/bin/run

ADD .docker/nginx.conf /etc/nginx/nginx.conf
ADD .docker/livembtiles.conf /etc/nginx/sites-available/default
RUN mkdir -p /var/tmp/nginx
RUN mkdir -p /var/cache/nginx

#
#  Run !
#...
EXPOSE 80
CMD ["/bin/sh", "-e", "/usr/local/bin/run"]