#!/usr/bin/env python3
"""Builds a Docker image for the specified benchmark engine."""

import argparse
import subprocess
import sys
from pathlib import Path

from log_archival_bench.scripts.docker_images.utils import get_image_name, validate_engine_name
from log_archival_bench.utils.project_config import CONFIG_DIR, PACKAGE_ROOT


def main(argv: list[str]) -> int:
    """
    Builds a Docker image for the specified benchmark engine.

    :param argv:
    :return: 0 on success, non-zero error code on failure.
    """
    args_parser = argparse.ArgumentParser()
    args_parser.add_argument(
        "--engine-name", required=True, help="The engine to be installed inside the Docker image."
    )

    parsed_args = args_parser.parse_args(argv[1:])
    engine_name = parsed_args.engine_name

    validate_engine_name(engine_name)

    docker_file_path = Path(CONFIG_DIR) / "docker-images" / f"{engine_name}.Dockerfile"
    if not docker_file_path.is_file():
        err_msg = f"Dockerfile for `{engine_name}` does not exist in {CONFIG_DIR}/docker-images."
        raise RuntimeError(err_msg)

    # fmt: off
    build_cmds = [
      "docker",
      "build",
      "--tag", get_image_name(engine_name),
      "--file", str(docker_file_path),
      str(PACKAGE_ROOT),
    ]
    # fmt: on
    subprocess.run(build_cmds, check=True)

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
