FROM redis:5.0.6-alpine3.10

RUN cd /tmp && \
    wget http://download.redis.io/redis-stable/redis.conf && \
    mkdir -p /etc/redis && \
    cp redis.conf /etc/redis/ && \
    touch /etc/redis/run.sh && \
    echo "sed -i 's,bind 127.0.0.1,bind 0.0.0.0,g' /etc/redis/redis.conf" >> /etc/redis/run.sh && \
    echo "sed -i '/^bind 0.0.0.0$/aslaveof '"\$REDIS_MASTER_SERVICE_HOST"' '"\$REDIS_MASTER_SERVICE_PORT"'' /etc/redis/redis.conf" >> /etc/redis/run.sh && \
    echo "redis-server /etc/redis/redis.conf" >> /etc/redis/run.sh && \
    chmod 755 /etc/redis/run.sh && \
    chown -R redis:redis /etc/redis

EXPOSE 6379/tcp

CMD ["/etc/redis/run.sh"]
