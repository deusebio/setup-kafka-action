# Setup Kafka Github Action

Action for easily setting up a Kafka cluster in your CI/CD pipeline.

## Usage

Simply include the action as a step in your Workflow:

```yaml
- name: Setup Kafka Cluster
  id: kafka
  uses: deusebio/setup-kafka-action@main
```

This will give your job an environment with the following:

  * Kafka deployment
  * ZooKeeper deployment
  * Juju installed
  * A LXD (default) controller bootstrapped


## Input Parameters

The actions takes the following parameters as input

| Name              | Description                                                                                      | Default      |
|-------------------|--------------------------------------------------------------------------------------------------|--------------|
| `broker-units`    | Number of Kafka broker to be used                                                                | 1            |
| `zookeeper-units` | Number of ZooKeeper servers to be used                                                           | 1            |
| `topic`           | Name for the requested topic. The `user-roles` parameter sets the permission level on such topic | "test-topic" |
| `user-roles`      | Role for the user to be created on the requested topic                                           | "admin"      |
| `model`           | Name of the Juju model where to deploy the cluster                                               | "kafka"      |


## Output Parameters

Once the Kafka cluster is deployed, the actions provides the following parameters as output

| Name               | Description                                                     |
|--------------------|-----------------------------------------------------------------|
| `bootstrap-server` | Address for the bootstrap server to be used to connect to Kafka |
| `username`         | User created in the Kafka cluster for external use              |
| `password`         | Password for the admin user                                     |


The output parameters can be refer using the `action-id`, e.g. 

```commandline
steps.<step-id>.outputs.bootstrap-server
```

## License

The Setup Kafka Github Action is free software, distributed under the Apache Software License, version 2.0. See LICENSE for more information.