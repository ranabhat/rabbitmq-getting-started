import pika, sys, os
import time

class Consumer():
    def __init__(self, hostname=None, queuename=None, body='Hello World'):
        self.hostname = hostname
        self.queuename = queuename
        self.body = body
        # Connect to the RabbitMQ server
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.hostname))
        # Create a channel without any arguments
        self.channel = self.connection.channel()
        # tell RabbitMQ not to give more than one message to a worker at a time.
        # or don't dispatch a new message to a worker until it has processed and acknowledged the previous one
        self.channel.basic_qos(prefetch_count=1)

    def declare_queue(self):
        # Create and connect to the queue. The arguments, in order, are:
        # queue - Name of the queue we are connecting on
        # durable - If true, RabbitMQ will write messages to disk
        # exclusive - If true, only this connection may connect to the queue
        # autoDelete - If true, the queue will be deleted when it is no longer in use
        # The final argument takes a Map of additional optional arguments
        #self.channel.queue_declare(self.queuename, False, False, False, None)
        self.channel.queue_declare(
                        queue=self.queuename,
                        durable=True, 
                        exclusive=False, 
                        auto_delete=False
                    )

    def callback(self, ch, method, properties, body):
         # Setup the callback to be invoked when a new message is received
        print(f" [x] Received {body.decode()}")
        time.sleep(1)
        # remove auto_ack=True flag and send a proper acknowledgment from the worker, once we're done with a task.
        ch.basic_ack(delivery_tag = method.delivery_tag)

    def consume(self):
        # Begin consuming messages from the queue. The second argument will tell
        # RabbitMQ to automatically consider the message acknowledged once received.
        # remove auto_ack=True flag 
        self.channel.basic_consume(self.queuename, on_message_callback=self.callback)
        print(' [*] Waiting for messages. To exit press CTRL+C')
        self.channel.start_consuming()

    def close_connection(self):
        self.connection.close()

if __name__ == '__main__':
    while True:
        try:
            consumer_instance = Consumer('rabbitmq-getting-started_rabbitmq_1', 'task_queue')
            consumer_instance.declare_queue()
            consumer_instance.consume()

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
            consumer_instance.close_connection()
            break
        except pika.exceptions.AMQPConnectionError as e:
            print(f" connection lost to broker {e}")
            time.sleep(2)
            continue
            
        


