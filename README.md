# python-kafka-scheduler

## Run Command
```
python kf_consumer.py
```
# How this works

This docker will run as a consumer for Kafka topic `scheduler` (can override using environment variable `TOPIC`)
Any message push to this topic will be expecting two keys `__eta__`(expected time to execute push the message) and `__target_topic__`(target topic where actual consumer is)


For example,
Consider a functionality of sending a mail with topic `send_mail` . A sample data looks like
```
{
    "user_id": 123,
    "action": "send_mail"
}
```
This is actually sending a mail instantly

Now Lets say, we need to send the mail in a specific time or with some count down (example as after 5 minutes). Then data should send to topic `scheduler` as
```
{
    "user_id": 123,
    "action": "send_mail",
    "__eta__": "2022-01-03 01:35:28",
    "__target_topic__": "send_mail"
}
```
Then the message will be pushing to `send_mail` topic once time reaches to `__eta__` value

after 5 minutes = ETA (current time + 5 min)

# Docker
https://hub.docker.com/r/itzmeontv/python-kafka-scheduler
