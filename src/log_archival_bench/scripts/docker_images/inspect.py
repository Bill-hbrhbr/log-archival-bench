#!/usr/bin/env python3
"""Inspect a Docker image for the specified benchmark engine and dump its JSON metadata."""

import argparse
import subprocess
import sys
from pathlib import Path

from log_archival_bench.scripts.docker_images.utils import get_image_name, validate_engine_name


def main(argv: list[str]) -> int:
    """
    Inspect a Docker image for the specified benchmark engine and dump its JSON metadata.

    :param argv:
    :return: 0 on success, non-zero error code on failure.
    """
    args_parser = argparse.ArgumentParser()
    args_parser.add_argument(
        "--engine-name",
        required=True,
        help="Name of the benchmark engine whose Docker image should be inspected.",
    )
    args_parser.add_argument(
        "--metadata-file",
        metavar="FILE",
        required=True,
        help="Path to dump the Docker image JSON metadata.",
    )
    args_parser.add_argument(
        "--id-only",
        action="store_true",
        help="Only dump the Docker image ID which is a stable digest of the image content.",
    )

    parsed_args = args_parser.parse_args(argv[1:])
    engine_name = parsed_args.engine_name
    metadata_file = parsed_args.metadata_file
    id_only = parsed_args.id_only

    validate_engine_name(engine_name)

    dump_cmds = ["docker", "inspect", "--type=image", get_image_name(engine_name)]
    if id_only:
        dump_cmds.append("--format")
        dump_cmds.append("{{.Id}}")

    metadata_file_path = Path(metadata_file)
    metadata_file_path.parent.mkdir(parents=True, exist_ok=True)
    with metadata_file_path.open("w", encoding="utf-8") as f:
        subprocess.run(dump_cmds, check=True, stdout=f)

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
