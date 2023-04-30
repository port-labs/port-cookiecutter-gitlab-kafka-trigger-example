import json
import logging
import signal

from typing import Any, Callable
from confluent_kafka import Consumer, KafkaException, Message
from core.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class KafkaConsumer():
    def __init__(
        self, msg_process: Callable[[Message], None], consumer: Consumer = None
    ) -> None:
        self.running = False
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)

        self.msg_process = msg_process

        if consumer:
            self.consumer = consumer
        else:
            conf = {
                "bootstrap.servers": settings.KAFKA_BOOTSTRAP_SERVERS,
                "security.protocol": "SASL_SSL",
                "sasl.mechanism": "SCRAM-SHA-512",
                "sasl.username": settings.KAFKA_USER,
                "sasl.password": settings.KAFKA_PASSWORD,
                "group.id": settings.KAFKA_USER,
                "auto.offset.reset": settings.KAFKA_CONSUMER_AUTO_OFFSET_RESET,
                "enable.auto.commit": "false",
            }
            self.consumer = Consumer(conf)

    def start(self) -> None:
        try:
            self.consumer.subscribe(
                [settings.KAFKA_RUNS_TOPIC],
                on_assign=lambda _, partitions: logger.info(
                    "Assignment: %s", partitions
                ),
            )
            self.running = True
            while self.running:
                try:
                    msg = self.consumer.poll(timeout=1.0)
                    if msg is None:
                        continue
                    if msg.error():
                        raise KafkaException(msg.error())
                    else:
                        try:
                            logger.info(
                                "Process message"
                                " from topic %s, partition %d, offset %d",
                                msg.topic(),
                                msg.partition(),
                                msg.offset(),
                            )
                            self.msg_process(json.loads(msg.value()))
                        except Exception as process_error:
                            logger.error(
                                "Failed process message"
                                " from topic %s, partition %d, offset %d: %s",
                                msg.topic(),
                                msg.partition(),
                                msg.offset(),
                                str(process_error),
                            )
                        finally:
                            logger.info("Committing offset")
                            self.consumer.commit(asynchronous=False)
                except Exception as message_error:
                    logger.error(str(message_error))
        except Exception as consumer_error:
            logger.error(str(consumer_error))
        finally:
            self.consumer.close()

    def exit_gracefully(self, *_: Any) -> None:
        logger.info("Exiting gracefully...")
        self.running = False
