import pika, sys, os
import time


class Consumer():
    def __init__(self, hostname=None, queue='', routing_key='', queue_name='', exchange='', exchange_type='fanout', body='Hello World'):
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
        # tell RabbitMQ not to give more than one message to a worker at a time.
        # or don't dispatch a new message to a worker until it has processed and acknowledged the previous one
        self.channel.basic_qos(prefetch_count=1)

    def declare_exchange(self):
        self.channel.exchange_declare(
                            exchange=self.exchange,
                            exchange_type=self.exchange_type
                            )

    def declare_queue(self):
        # Create and connect to the queue. The arguments, in order, are:
        # queue - Name of the queue we are connecting on
        # durable - If true, RabbitMQ will write messages to disk
        # exclusive - If true, only this connection may connect to the queue
        # autoDelete - If true, the queue will be deleted when it is no longer in use
        # The final argument takes a Map of additional optional arguments
        return self.channel.queue_declare(
                        queue=self.queue, # empty queue parameter means the server choose a random queue name for us
                        durable=False, 
                        exclusive=True,  # once the consumer connection is closed, the queue should be deleted
                        auto_delete=False
                    )
        self.queue_name = result.method.queue

    def bind_queue(self):
        """
        We've already created a fanout exchange and a queue. 
        Now we need to tell the exchange to send messages to our queue. 
        That relationship between exchange and a queue is called a binding.

        """
        severities = ["info", "warning", "error"]

        ## When publish routing key is "run, run" the queue won't have that message
        for severity in severities:
            self.channel.queue_bind(
                            exchange=self.exchange,
                            queue=self.queue_name,
                            routing_key=severity
                            )


    def callback(self, ch, method, properties, body):
         # Setup the callback to be invoked when a new message is received
        print(f" [x] Received {method.routing_key}: {body.decode()}")
        time.sleep(1)
        # remove auto_ack=True flag and send a proper acknowledgment from the worker, once we're done with a task.
        ch.basic_ack(delivery_tag = method.delivery_tag)

    def consume(self):
        # Begin consuming messages from the queue. The second argument will tell
        # RabbitMQ to automatically consider the message acknowledged once received.
        # remove auto_ack=True flag 
        self.channel.basic_consume(queue=self.queue_name, on_message_callback=self.callback)
        print(' [*] Waiting for messages. To exit press CTRL+C')
        self.channel.start_consuming()

    def close_connection(self):
        self.connection.close()

if __name__ == '__main__':
    while True:
        try:
            consumer_instance = Consumer(hostname='rabbitmq-getting-started_rabbitmq_1', queue='', routing_key='', queue_name='', exchange='direct_logs', exchange_type='direct')
            consumer_instance.declare_exchange()
            consumer_instance.declare_queue()
            consumer_instance.bind_queue()
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
            
        


