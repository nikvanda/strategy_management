import redis
import pika
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_caching import Cache

db = SQLAlchemy()
jwt = JWTManager()

cache = Cache()
redis_client = redis.Redis(host='redis', port=6379, db=0)

connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
channel = connection.channel()

channel.queue_declare(queue='strategy_changed')
