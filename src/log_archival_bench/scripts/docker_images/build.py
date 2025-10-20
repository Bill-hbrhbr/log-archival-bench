#!/usr/bin/env python3
"""
Builds a Docker image for the specified benchmark engine, and optionally dump the image
configuration as JSON.
"""

import argparse
import subprocess
import sys

from log_archival_bench.scripts.docker_images.utils import get_image_name
from log_archival_bench.utils.path_utils import (
    get_config_dir,
    which,
)


def main(argv: list[str]) -> int:
    """
    Builds a Docker image for the specified benchmark engine, and optionally dump the image
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

    valid_engines = ["clickhouse", "clp", "elasticsearch", "sparksql", "zstandard"]
    if engine_name not in valid_engines:
        err_msg = f"Invalid engine name `{engine_name}`. Valid engines: {', '.join(valid_engines)}"
        raise ValueError(err_msg)

    docker_file_path = get_config_dir() / "docker-images" / engine_name / "Dockerfile"
    if not docker_file_path.is_file():
        err_msg = f"Dockerfile for `{engine_name}` does not exist."
        raise RuntimeError(err_msg)

    # fmt: off
    build_cmd = [
        which("python3"),
        "-m", "log_archival_bench.scripts.docker_images.native.build",
        "--image-name", get_image_name(engine_name),
        "--docker-file-path", str(docker_file_path),
    ]
    # fmt: on

    if parsed_args.dump_config_path is not None:
        build_cmd.append("--dump-config-path")
        build_cmd.append(parsed_args.dump_config_path)

    subprocess.run(build_cmd, check=True)

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
