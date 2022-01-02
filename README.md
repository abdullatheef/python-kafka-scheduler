# python-kafka-scheduler

## Run Command
```
python kf_consumer.py
```
# How this works

This script will run as a consumer for Kafka topic `scheduler` (can override using environment variable `TOPIC`)
Any message push to this topic will be expecting two keys `__eta__`(expected time to execute push the message) and `__target_topic__`(target topic where actual consumer is)


For example, If there is a sample data 
```
{
    "user_id": 123,
    "action": "send_mail"
}
```
Lets say, there is a topic named `send_mail` which has consumers. 
No if this action has to scheduled, data should send to topic `scheduler` as
```
{
    "user_id": 123,
    "action": "send_mail",
    "__eta__": "2022-01-03 01:35:28",
    "__target_topic__": "send_mail"
}
```
Then the message will be pushing to `send_mail` topuc once time reaches to `__eta__` value

#Docker
https://hub.docker.com/r/itzmeontv/python-kafka-scheduler
