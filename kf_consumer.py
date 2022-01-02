from confluent_kafka import Consumer, Producer
try:
   from queue import PriorityQueue
except ImportError:
   from Queue import PriorityQueue
from datetime import datetime
import json, time, os, pytz
from dateutil import parser


BROKER = os.environ.get('BROKER')
print BROKER
GROUP_ID = "scheduler_group"
SCHEDULER_TOPIC = os.environ.get('TOPIC') or "scheduler"
CONSUMER_CONF = {
    'bootstrap.servers': BROKER,
    'group.id': GROUP_ID,
    'auto.offset.reset': 'smallest'
}
PRODUCER_CONF = {
    'bootstrap.servers': BROKER
}


consumer = Consumer(CONSUMER_CONF)
producer = Producer(PRODUCER_CONF)

min_heap = PriorityQueue()


running = True

def push_item_to_topic(data):
    target_topic = data.pop('__target_topic__')
    print "pushing data %s" %data
    producer.produce(target_topic, key=None, value=json.dumps(data))



def basic_consume_loop(consumer, topics):
    try:
        consumer.subscribe(topics)
        while running:
            while not min_heap.empty():
                item = min_heap.queue[0]
                schedule_time = item[0]
                IST = pytz.timezone('Asia/Kolkata')
                if schedule_time.tzinfo:
                    schedule_time = schedule_time.replace(tzinfo=None)
                if datetime.now(IST).replace(tzinfo=None) > schedule_time:
                    item = min_heap.get_nowait()
                    push_item_to_topic(item[1])
                else:
                    time.sleep(2)
                    break
            msg = consumer.poll(timeout=1.0)
            if msg is None: continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    sys.stderr.write('%% %s [%d] reached end at offset %d\n' %
                                     (msg.topic(), msg.partition(), msg.offset()))
                elif msg.error():
                    raise KafkaException(msg.error())
            else:
                try:
                    msg_process(msg)
                except Exception as e:
                    print e
    finally:
        # Close down consumer to commit final offsets.
        consumer.close()

def shutdown():
    running = False

def msg_process(msg):
    print msg.key(), msg.value()
    data = json.loads(msg.value())
    eta = data.pop('__eta__')
    min_heap.put((parser.parse(eta), data))



basic_consume_loop(consumer, [SCHEDULER_TOPIC])
#doker run --add-host kafka:192.168.225.115  -it -e BROKER=kafka:9092 --rm --name my-running-app my-python-app



