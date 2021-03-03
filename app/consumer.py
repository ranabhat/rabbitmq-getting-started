import pika

QUEUE_NAME = "hello"
# Connect to the RabbitMQ server
try:    
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    # Create a channel without any arguments
    channel = connection.channel()

    channel.queue_declare(QUEUE_NAME, False, False, False, None)

    # Setup the callback to be invoked when a new message is received
    def callback(ch, method, properties, body):
        print(f" [x] Received {body}")
    # Begin consuming messages from the queue. The second argument will tell
    # RabbitMQ to automatically consider the message acknowledged once received.

    channel.basic_consume(QUEUE_NAME, on_message_callback=callback, auto_ack=True)
    channel.start_consuming()

except IOError as e:
    print(e)
except TimeoutError as e:
    print(e)


