import pandas as pd
from kafka import KafkaConsumer
import time
import json

group = f"trade_{time.time_ns()}"
consumer = KafkaConsumer('tradeCallback', bootstrap_servers=['192.168.1.60:9092'], group_id=group,
                         auto_offset_reset='earliest', enable_auto_commit=True)
res = consumer.poll(timeout_ms=1000, max_records=1000)
items = res.items()
data_list = []
for topic, message_list in res.items():
    for message in message_list:
        message_dict = json.loads(message.value.decode())
        data_list.append(message_dict)
df = pd.DataFrame(data_list)
df.to_excel('trade.xlsx')
