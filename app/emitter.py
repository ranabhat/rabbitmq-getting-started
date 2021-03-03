import pika
import time

QUEUE_NAME = "hello"
# Connect to the RabbitMQ server
try:    
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    # Create a channel without any arguments
    channel = connection.channel()
    # Create and connect to the queue. The arguments, in order, are:
    # queue - Name of the queue we are connecting on
    # durable - If true, RabbitMQ will write messages to disk
    # exclusive - If true, only this connection may connect to the queue
    # autoDelete - If true, the queue will be deleted when it is no longer in use
    # The final argument takes a Map of additional optional arguments
    channel.queue_declare(QUEUE_NAME, False, False, False, None)
    while True:
        #Send Message to the queue
        channel.basic_publish('', routing_key=QUEUE_NAME, body='Hello World')
        print(f"Sent 'Hello World'")
        time.sleep(1)

except IOError as e:
    print(e)
except TimeoutError as e:
    print(e)





