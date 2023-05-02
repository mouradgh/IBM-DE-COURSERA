wget https://archive.apache.org/dist/kafka/2.8.0/kafka_2.12-2.8.0.tgz
tar -xzf kafka_2.12-2.8.0.tgz
start_mysql
mysql --host=127.0.0.1 --port=3306 --user=root --password=
create database tolldata;
use tolldata;
create table livetolldata(timestamp datetime,vehicle_id int,vehicle_type char(15),toll_plaza_id smallint);
exit

python3 -m pip install kafka-python
python3 -m pip install mysql-connector-python==8.0.31


##ZooKeeper is required for Kafka to work##
bin/zookeeper-server-start.sh config/zookeeper.properties

New terminal :
cd kafka_2.12-2.8.0
bin/kafka-server-start.sh config/server.properties


You need to create a topic before you can start to post messages.
To create a topic named `news`, start a new terminal and run the command below.
New terminal :
cd kafka_2.12-2.8.0
bin/kafka-topics.sh --create --topic toll --bootstrap-server localhost:9092



You need a producer to send messages to Kafka. Run the command below to start a producer.
bin/kafka-console-producer.sh --topic news --bootstrap-server localhost:9092


Once the producer starts, and you get the ‘>’ prompt, type any text message and press enter. Or you can copy the text below and paste. The below text sends three messages to kafka.
Good morning
Good day
Enjoy the Kafka lab



You need a consumer to read messages from kafka.
Open a new terminal.
Run the command below to listen to the messages in the topic `news`
cd kafka_2.12-2.8.0
bin/kafka-console-consumer.sh --topic news --from-beginning --bootstrap-server localhost:9092


List all topics :
bin/kafka-topics.sh --bootstrap-server localhost:9092 --list

To see the details of a topic :
bin/kafka-topics.sh --bootstrap-server localhost:9092 --describe --topic news