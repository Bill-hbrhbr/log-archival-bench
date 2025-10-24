"""Shared helpers for Docker image scripts."""

import os


def get_image_name(engine_name: str) -> str:
    """
    :param engine_name: The name of the service engine inside the Docker image.
    :return: The name assigned to the Docker image that contains the engine.
    """
    user = os.getenv("USER", "clp-user")
    return f"log-archival-bench-{engine_name}-ubuntu-jammy:dev-{user}"


def validate_engine_name(engine_name: str) -> None:
    """
    :param engine_name: The name of the service engine to be validated.
    :return: Whether this is a valid service engine that exists in the benchmark list.
    """
    # NOTE: Keep in sync with `G_DOCKER_IMAGE_ENGINES` in taskfiles/docker-images/main.yaml
    valid_engines = ["clickhouse", "clp", "elasticsearch", "sparksql", "zstandard"]
    if engine_name not in valid_engines:
        err_msg = f"Invalid engine name `{engine_name}`. Valid engines: {', '.join(valid_engines)}"
        raise ValueError(err_msg)
