from dataclasses import dataclass
from typing import Optional

import pytest
import pytest_asyncio
from juju.action import Action
from juju.application import Application
from juju.model import Model
from juju.unit import Unit


class NotFoundError(Exception):
    pass


@dataclass
class KafkaCredentials:
    username: str
    password: str
    bootstrap_servers: list[str]


@pytest_asyncio.fixture
async def model() -> Model:
    current_model = Model()

    await current_model.connect_current()

    yield current_model

    await current_model.disconnect()


@pytest.fixture
def app_name():
    return "user"


@pytest_asyncio.fixture
async def kafka_credentials(
    model: Model,
    app_name: str,
) -> KafkaCredentials:
    user: Application = model.applications[app_name]

    leader: Optional[Unit] = None
    for unit in user.units:
        is_leader = await unit.is_leader_from_status()
        if is_leader:
            leader = unit
            break

    if leader is None:
        raise NotFoundError(f"application {app_name} does not have a leader")

    res: Action = await leader.run_action("get-credentials")
    await res.wait()

    kafka_data = res.results["kafka"]

    username = kafka_data["username"]
    password = kafka_data["password"]
    bootstrap_servers = kafka_data["endpoints"].split(",")

    return KafkaCredentials(
        username=username, password=password, bootstrap_servers=bootstrap_servers
    )
