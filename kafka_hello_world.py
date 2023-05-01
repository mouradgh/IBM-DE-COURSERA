from kafka import KafkaAdminClient, KafkaProducer, KafkaConsumer
from kafka.admin import NewTopic, ConfigResource, ConfigResourceType
import json


# To use KafkaAdminClient, we first need to define and create a KafkaAdminClient object
admin_client = KafkaAdminClient(bootstrap_servers="localhost:9092", client_id='test')

# We first need to define an empty topic list
topic_list = []

# Then we use the NewTopic class to create a topic
new_topic = NewTopic(name="bankbranch3", num_partitions=2, replication_factor=1)
topic_list.append(new_topic)

# We can use create_topics(...) method to create new topics
admin_client.create_topics(new_topics=topic_list)

# The above code is the equivalent to this CLI command
# "kafka-topics.sh --bootstrap-server localhost:9092 --create --topic bankbranch  --partitions 2 --replication_factor 1"

# we can check the created topics configuration details using describe_configs()
configs = admin_client.describe_configs(
    config_resources=[ConfigResource(ConfigResourceType.TOPIC, "bankbranch3")])

# The above code is the equivalent to this CLI command
# kafka-topics.sh --bootstrap-server localhost:9092 --describe --topic bankbranch

# Create a producer and use it to produce 2 transactions
print("we're here producer")
producer = KafkaProducer(value_serializer=lambda v: json.dumps(v).encode('utf-8'))
producer.send("bankbranch3", {'atmid':1, 'transid':100})
producer.send("bankbranch3", {'atmid':2, 'transid':101})

# The above code is the equivalent to this CLI command
# kafka-console-producer.sh --bootstrap-server localhost:9092 --topic bankbranch

# Create a consumer
print("we're here consumer")
consumer = KafkaConsumer('bankbranch3')

# Print the received messages
for msg in consumer:
    print("test")
    print(msg.value.decode("utf-8"))
