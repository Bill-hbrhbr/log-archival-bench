#!/usr/bin/env python3
"""Builds a Docker image and optionally dumps its configuration as JSON."""

import argparse
import subprocess
import sys
from pathlib import Path

from log_archival_bench.utils.project_config import PACKAGE_ROOT


def main(argv: list[str]) -> int:
    """
    Builds a Docker image and optionally dumps its configuration as JSON.

    :param argv:
    :return: 0 on success, non-zero error code on failure.
    """
    args_parser = argparse.ArgumentParser()
    args_parser.add_argument("--image-name", required=True, help="The name of the Docker image.")
    args_parser.add_argument("--docker-file-path", required=True, help="Path to the Dockerfile.")
    args_parser.add_argument(
        "--dump-config-path", help="Path to the file to dump the Docker image JSON metadata."
    )

    parsed_args = args_parser.parse_args(argv[1:])
    image_name = parsed_args.image_name
    docker_file_path = parsed_args.docker_file_path
    dump_config_path = parsed_args.dump_config_path

    # fmt: off
    build_cmds = [
      "docker",
      "build",
      "--tag", image_name,
      "--file", docker_file_path,
      PACKAGE_ROOT,
    ]
    # fmt: on
    subprocess.run(build_cmds, check=True)

    if dump_config_path is not None:
        output_path = Path(dump_config_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with output_path.open("w", encoding="utf-8") as f:
            dump_cmds = ["docker", "inspect", "--type=image", image_name]
            subprocess.run(dump_cmds, check=True, stdout=f)

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
