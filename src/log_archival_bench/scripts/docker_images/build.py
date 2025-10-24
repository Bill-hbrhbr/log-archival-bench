#!/usr/bin/env python3
"""
Builds a Docker image for the specified benchmark engine, and optionally dumps the image
configuration as JSON.
"""

import argparse
import subprocess
import sys
from pathlib import Path

from log_archival_bench.scripts.docker_images.utils import get_image_name
from log_archival_bench.utils.project_config import CONFIG_DIR, PACKAGE_ROOT


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


def main(argv: list[str]) -> int:
    """
    Builds a Docker image for the specified benchmark engine, and optionally dumps the image
    configuration as JSON.

    :param argv:
    :return: 0 on success, non-zero error code on failure.
    """
    args_parser = argparse.ArgumentParser()
    args_parser.add_argument(
        "--engine-name", required=True, help="The engine to be installed inside the Docker image."
    )
    args_parser.add_argument(
        "--dump-config-path", help="Path to the file to dump the Docker image JSON metadata."
    )

    parsed_args = args_parser.parse_args(argv[1:])
    engine_name = parsed_args.engine_name
    dump_config_path = parsed_args.dump_config_path

    valid_engines = ["clickhouse", "clp", "elasticsearch", "sparksql", "zstandard"]
    if engine_name not in valid_engines:
        err_msg = f"Invalid engine name `{engine_name}`. Valid engines: {', '.join(valid_engines)}"
        raise ValueError(err_msg)

    docker_file_path = Path(CONFIG_DIR) / "docker-images" / engine_name / "Dockerfile"
    if not docker_file_path.is_file():
        err_msg = f"Dockerfile for `{engine_name}` does not exist."
        raise RuntimeError(err_msg)

    image_name = get_image_name(engine_name)
    build_docker_image(image_name, str(docker_file_path))

    if dump_config_path is not None:
        output_path = Path(dump_config_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with output_path.open("w", encoding="utf-8") as f:
            dump_cmds = ["docker", "inspect", "--type=image", image_name]
            subprocess.run(dump_cmds, check=True, stdout=f)

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
