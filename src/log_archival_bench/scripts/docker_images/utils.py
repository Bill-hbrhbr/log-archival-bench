"""Shared helpers for Docker image scripts."""

import os


def get_image_name(service_name: str) -> str:
    """
    :param service_name:
    :return: The name assigned to the Docker image that contains the service.
    """
    user = os.getenv("USER", "clp-user")
    return f"log-archival-bench-{service_name}-ubuntu-jammy:dev-{user}"


def validate_service_name(service_name: str) -> None:
    """
    :param service_name: The name of the benchmark service.
    :raise: ValueError if the service is invalid.
    """
    # NOTE: Keep in sync with `G_BENCHMARK_DOCKER_SERVICES` in taskfiles/docker-images/main.yaml
    valid_services = ["clickhouse", "clp", "elasticsearch", "sparksql", "zstandard"]
    if service_name not in valid_services:
        err_msg = (
            f"Invalid service name `{service_name}`. Valid services: {', '.join(valid_services)}"
        )
        raise ValueError(err_msg)
