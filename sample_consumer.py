import pika, sys, os
from common.logs.logger import logger

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# a callback called back for whenever our app receives a broker message
def process_the_task1(ch, method, properties, body):
    msg = body.decode('utf-8')
    logger.info(f"{msg}, {process_the_task1.__name__}")

    

def process_the_task2(ch, method, properties, body):
    msg = body.decode('utf-8')
    logger.info(f"{msg}, {process_the_task2.__name__}")
    


# first consumer
channel.exchange_declare(exchange='driver_created_fanout_exchange', exchange_type='fanout', durable=True )

channel.queue_declare( queue='sample_driver_created', durable=True)

channel.queue_bind(queue='sample_driver_created',
                   exchange='driver_created_fanout_exchange'
                   )

channel.basic_consume(
    queue='driver_created_fanout_exchange',
    auto_ack=True,
    on_message_callback=process_the_task1
    )

# second consumer

channel.exchange_declare(exchange='vehicle_created_fanout_exchange', exchange_type='fanout', durable=True )
channel.queue_declare( queue='sample_vehicle_created', durable=True)

channel.queue_bind(queue='sample_vehicle_created',
                   exchange='vehicle_created_fanout_exchange'
                   )

channel.basic_consume(
    queue='sample_vehicle_created',
    auto_ack=True,
    on_message_callback=process_the_task2
    )


if __name__ == '__main__':
    try:
        print(' [*] Waiting for messages. To exit press CTRL+C')
        channel.start_consuming()
        
    except KeyboardInterrupt:
        print('Interrupted')
        
        try:
            sys.exit(0)
            
        except SystemExit:
            os._exit(0)