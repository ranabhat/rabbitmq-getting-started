import pika
import time
import uuid

class Emitter():
    def __init__(self, hostname=None, queuename=None, body='Hello World'):
        self.hostname = hostname
        self.queuename = queuename
        self.body = body
        # Connect to the RabbitMQ server
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.hostname))
        # Create a channel without any arguments
        self.channel = self.connection.channel()

    def declare_queue(self):
        # Create and connect to the queue. The arguments, in order, are:
        # queue - Name of the queue we are connecting on
        # durable - If true, RabbitMQ will write messages to disk
        # exclusive - If true, only this connection may connect to the queue
        # autoDelete - If true, the queue will be deleted when it is no longer in use
        # The final argument takes a Map of additional optional arguments
        self.channel.queue_declare(
                        queue=self.queuename,
                        durable=True, 
                        exclusive=False, 
                        auto_delete=False
                    )

    def send_message_to_queue(self):
        #Send Message to the queue
        new_message=''.join([self.body, ' ', str(uuid.uuid4())])

        #mark our messages as persistent - 
        # by supplying a delivery_mode property with the value of pika.spec.PERSISTENT_DELIVERY_MODE
        self.channel.basic_publish(
            '', 
            routing_key=self.queuename, 
            body=new_message,
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            )
        )
        print(f"Sent {new_message}")
    
    def close_connection(self):
        self.connection.close()

if __name__ == '__main__':
    while True:
        try:
            emitter_instance = Emitter('rabbitmq-getting-started_rabbitmq_1', 'task_queue')
            emitter_instance.declare_queue()
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



