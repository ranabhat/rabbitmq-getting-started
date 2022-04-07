import pika
import time
import uuid

# exchange_type
# fanout : broadcast message to all queues
# direct
# topic
# headers
# default

class Emitter():
    def __init__(self, hostname=None, queue='', routing_key='', queue_name='', exchange='', exchange_type='fanout',body='Hello World'):
        self.hostname = hostname
        self.queue = queue
        self.routing_key = routing_key
        self.queue_name = queue_name
        self.exchange = exchange
        self.exchange_type = exchange_type
        self.body = body
        # Connect to the RabbitMQ server
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.hostname))
        # Create a channel without any arguments
        self.channel = self.connection.channel()

    def declare_exchange(self):
        self.channel.exchange_declare(
                            exchange=self.exchange,
                            exchange_type=self.exchange_type
                            )

    def send_message_to_queue(self):
        #Send Message to the queue
        new_message=''.join([self.body, ' ', str(uuid.uuid4())])

        #mark our messages as persistent - 
        # by supplying a delivery_mode property with the value of pika.spec.PERSISTENT_DELIVERY_MODE
        self.channel.basic_publish(
            exchange=self.exchange, 
            routing_key=self.routing_key, # for fanout exchanges routing_key is ignored
            body=new_message
        )
        print(f"Sent {new_message}")
    
    def close_connection(self):
        self.connection.close()

if __name__ == '__main__':
    while True:
        try:
            emitter_instance = Emitter(hostname='rabbitmq-getting-started_rabbitmq_1', queue='', routing_key='', queue_name='', exchange='logs', exchange_type='fanout')
            emitter_instance.declare_exchange()
            while True:
                emitter_instance.send_message_to_queue()
                time.sleep(1)
        except IOError as e:
            print(f"i/o error")
            time.sleep(2)
            continue
        except TimeoutError as e:
            print(f"time out error")
            time.sleep(2)
            continue
        except KeyboardInterrupt as e:
            print(f"control c pressed connection to be closed {e}")
            emitter_instance.close_connection()
            break
        except pika.exceptions.StreamLostError as e:
            print(f"connection reset by server {e}")
            time.sleep(2)
            continue
        except pika.exceptions.AMQPConnectionError as e:
            print(f" connection lost to broker {e}")
            time.sleep(2)
            continue



