import pika
import time

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
        #self.channel.queue_declare(self.queuename, False, False, False, None)
        self.channel.queue_declare(queue=self.queuename, durable=False, exclusive=False, auto_delete=False)

    def send_message_to_queue(self):
        #Send Message to the queue
        self.channel.basic_publish('', routing_key=self.queuename, body=self.body)
        print(f"Sent {self.body}")
    
    def close_connection(self):
        self.connection.close()

try:
    emitter_instance = Emitter('rabbitmq-getting-started_rabbitmq_1', 'hello')
    emitter_instance.declare_queue()
    while True:
        emitter_instance.send_message_to_queue()
        time.sleep(1)
except IOError as e:
    print(e)
except TimeoutError as e:
    print(e)
except KeyboardInterrupt as e:
    print(f"control c pressed connection to be closed {e}")
    emitter_instance.close_connection()


