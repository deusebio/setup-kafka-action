from uuid import uuid4

import pytest
from juju.application import Application
from juju.model import Model
from kafka.admin import NewTopic
from kafka.errors import InvalidReplicationFactorError

from setup_kafka_action.fixtures import KafkaCredentials, kafka_credentials, model
from tests.app import KafkaClient

@pytest.fixture
def app_name():
    return "user"

@pytest.mark.asyncio
async def test_juju_connection(model: Model):
    status = await model.get_status()

    assert "kafka" in status.applications


@pytest.mark.asyncio
async def test_non_replicated_topic_creation(kafka_credentials: KafkaCredentials):
    client = KafkaClient(
        servers=kafka_credentials.bootstrap_servers,
        username=kafka_credentials.username,
        password=kafka_credentials.password,
    )

    topic_name = uuid4().hex

    topic_config = NewTopic(
        name=topic_name,
        num_partitions=4,
        replication_factor=1,
    )

    client.create_topic(topic=topic_config)


@pytest.mark.asyncio
async def test_replicated_topic_creation_ko(kafka_credentials: KafkaCredentials):
    client = KafkaClient(
        servers=kafka_credentials.bootstrap_servers,
        username=kafka_credentials.username,
        password=kafka_credentials.password,
    )

    topic_name = uuid4().hex

    topic_config = NewTopic(
        name=topic_name,
        num_partitions=4,
        replication_factor=3,
    )

    with pytest.raises(InvalidReplicationFactorError):
        client.create_topic(topic=topic_config)


@pytest.mark.asyncio
async def test_replicated_topic_creation_ok(
    model: Model, kafka_credentials: KafkaCredentials
):
    kafka: Application = model.applications["kafka"]
    await kafka.add_unit(2)

    # Scaling up the Kafka cluster
    await model.wait_for_idle(apps=["kafka"], status="active")

    client = KafkaClient(
        servers=kafka_credentials.bootstrap_servers,
        username=kafka_credentials.username,
        password=kafka_credentials.password,
    )

    topic_name = uuid4().hex

    topic_config = NewTopic(
        name=topic_name,
        num_partitions=4,
        replication_factor=3,
    )

    client.create_topic(topic=topic_config)
