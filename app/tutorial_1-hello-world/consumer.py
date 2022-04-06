import pika, sys, os

class Consumer():
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


    def callback(self, ch, method, properties, body):
         # Setup the callback to be invoked when a new message is received
        print(f" [x] Received {body.decode()}")

    def consume(self):
        # Begin consuming messages from the queue. The second argument will tell
        # RabbitMQ to automatically consider the message acknowledged once received.
        self.channel.basic_consume(self.queuename, on_message_callback=self.callback, auto_ack=True)
        print(' [*] Waiting for messages. To exit press CTRL+C')
        self.channel.start_consuming()

if __name__ == '__main__':
    try:
        consumer_instance = Consumer('rabbitmq-getting-started_rabbitmq_1', 'hello')
        consumer_instance.declare_queue()
        consumer_instance.consume()

    except IOError as e:
        print(e)
    except TimeoutError as e:
        print(e)
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)


