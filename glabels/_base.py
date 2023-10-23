import os
import logging
import subprocess
from typing import List


class GlabelsBatchRunError(Exception):
    pass


class GlabelsBase:
    def __init__(
            self,
            path: str,
            *,
            command_env: List[str] = None,
            logger: any = None,
            echo: bool = False,
    ):
        self.path = path
        self.base_args = []
        self.logger = logger
        self.echo = echo

        if command_env:
            self.base_args = command_env

        self.base_args.append(path)

        if logger is None:
            self.logger = logging.getLogger(__name__)
            logging.basicConfig(
                handlers=(logging.StreamHandler(), ),
                format='%(asctime)s | %(levelname)s: %(message)s',
                datefmt="%Y-%m-%dT%H:%M:%S%z",
                level=logging.INFO
            )

    def _run(self, args: List[str], *, stdin: bytes = b'') -> bytes:
        args = self.base_args + args

        if self.echo:
            self.logger.info(f"Running: {' '.join(args)}")

        result = subprocess.run(
            args,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            input=stdin,
        )

        if result.returncode != 0:
            self.logger.error(repr(result))
            raise GlabelsBatchRunError(repr(result))

        return result.stdout

    @staticmethod
    def raise_if_not_exist(filename: str):
        if not os.path.exists(filename):
            raise FileNotFoundError(filename)
