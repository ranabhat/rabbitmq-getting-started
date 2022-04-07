# Publish/Subscribe

1. Producer: user application that sends messages
2. Queue: buffer that stores messages
3. Consumer: a user application that receives messages

#### Core Idea
--------------

######  The core idea in messaging model in RabbitMQ is that the producer never sends any messages directly to a queue.

> 1. Producer can only send messages to an exchange. 
> 2. An exchange receives messages from producers and the other side it pushes them to queues.
> 3. Exchange type guides exchanges what exchange should do with the messages. Depending on the exchange type: it can append message to a particular queue, or it can append message to many queues or discard the messages at all

#### Exchange Type
------------------

> 1. fanout : broadcasts all the messages it receives to all the queues it knows
> 2. direct: a message goes to the queues whose binding key exactly matches the routing key of the message.
> 3. topic
> 4. headers
> 5. default: nameless exchange: which we identify by the empty string (""). (messages are routed to the queue with the name specified by routing_key, if it exists)

###### Routing key is ignored for fanout exchanges

CLI command to list exchanges `sudo rabbitmqctl list_exchanges`

#### Bindings
-------------

Through bindings we tell the exchange to send messages to our queue


CLI command to list bindings `rabbitmqctl list_bindings`