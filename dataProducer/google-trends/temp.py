from confluent_kafka import Consumer, KafkaError
from confluent_kafka.avro import AvroConsumer
from confluent_kafka.avro.serializer import SerializerError

c = AvroConsumer({
    'bootstrap.servers': 'kafka:9092',
    'group.id': 'assets-price',
    'auto.offset.reset': 'earliest',
    'schema.registry.url': 'http://schema-registry:8081'  # replace <schema-registry-host> with your schema registry host
})

c.subscribe(['assets-price'])

while True:

    try:
        msg = c.poll(1.0)
    except SerializerError as e:
        print("Message deserialization failed: {}".format(e))
        break

    if msg is None:
        print('msg is None')
        continue
    if msg.error():
        print("Consumer error: {}".format(msg.error()))
        continue

    print('Received message: {}'.format(msg.value()))

c.close()
