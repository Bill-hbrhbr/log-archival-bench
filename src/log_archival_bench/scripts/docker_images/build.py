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


def main(argv: list[str]) -> int:
    """
    Builds a Docker image for the specified benchmark engine, and optionally dumps the image
    configuration as JSON.

    :param argv:
    :return: 0 on success, non-zero error code on failure.
    """
    args_parser = argparse.ArgumentParser()
    args_parser.add_argument(
        "--engine-name", required=True, help="The engine to be benchmarked inside the Docker image."
    )
    args_parser.add_argument(
        "--metadata-file", metavar="FILE", help="Path to write build result metadata."
    )

    parsed_args = args_parser.parse_args(argv[1:])
    engine_name = parsed_args.engine_name
    metadata_file = parsed_args.metadata_file

    valid_engines = ["clickhouse", "clp", "elasticsearch", "sparksql", "zstandard"]
    if engine_name not in valid_engines:
        err_msg = f"Invalid engine name `{engine_name}`. Valid engines: {', '.join(valid_engines)}"
        raise ValueError(err_msg)

    docker_file_path = Path(CONFIG_DIR) / "docker-images" / f"{engine_name}.Dockerfile"
    if not docker_file_path.is_file():
        err_msg = f"Dockerfile for `{engine_name}` does not exist."
        raise RuntimeError(err_msg)

    # fmt: off
    build_cmds = [
      "docker", "buildx", "build",
      "--load",
      "--tag", get_image_name(engine_name),
      "--file", str(docker_file_path),
    ]
    # fmt: on
    if metadata_file is not None:
        Path(metadata_file).parent.mkdir(parents=True, exist_ok=True)
        build_cmds.append("--metadata-file")
        build_cmds.append(metadata_file)
    build_cmds.append(str(PACKAGE_ROOT))

    subprocess.run(build_cmds, check=True)

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
