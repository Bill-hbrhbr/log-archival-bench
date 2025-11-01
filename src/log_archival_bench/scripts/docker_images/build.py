#!/usr/bin/env python3
"""Builds a Docker image for the specified service."""

import argparse
import subprocess
import sys
from pathlib import Path

from log_archival_bench.scripts.docker_images.utils import get_image_name, validate_service_name
from log_archival_bench.utils.project_config import CONFIG_DIR, PACKAGE_ROOT


def main(argv: list[str]) -> int:
    """
    Builds a Docker image for the specified service.

    :param argv:
    :return: 0 on success, non-zero error code on failure.
    """
    args_parser = argparse.ArgumentParser()
    args_parser.add_argument(
        "--service-name",
        required=True,
        help="The service that the built Docker image will provide.",
    )

    parsed_args = args_parser.parse_args(argv[1:])
    service_name = parsed_args.service_name

    validate_service_name(service_name)

    docker_file_path = Path(CONFIG_DIR) / "docker-images" / service_name / "Dockerfile"
    if not docker_file_path.is_file():
        err_msg = f"Dockerfile for `{service_name}` does not exist in {CONFIG_DIR}/docker-images."
        raise RuntimeError(err_msg)

    # fmt: off
    build_cmds = [
      "docker",
      "build",
      "--tag", get_image_name(service_name),
      "--file", str(docker_file_path),
      str(PACKAGE_ROOT),
    ]
    # fmt: on
    subprocess.run(build_cmds, check=True)

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
