"""Shared helpers for Docker image scripts."""

import os
import subprocess

from log_archival_bench.utils.project_config import PACKAGE_ROOT


def get_image_name(engine_name: str) -> str:
    """
    :param engine_name: The service engine inside the Docker image.
    :return: The name assigned to the Docker image that contains the engine.
    """
    user = os.getenv("USER", "clp-user")
    return f"log-archival-bench-{engine_name}-ubuntu-jammy:dev-{user}"


def build_docker_image(image_name: str, docker_file_path_str: str) -> None:
    """
    Builds a docker image.

    :param image_name:
    :param docker_file_path_str:
    """
    # fmt: off
    build_cmds = [
      "docker",
      "build",
      "--tag", image_name,
      "--file", docker_file_path_str,
      str(PACKAGE_ROOT),
    ]
    # fmt: on
    subprocess.run(build_cmds, check=True)
