from typing import List, Union, Optional


from glabels._base import GlabelsBase


class Glabels3Batch(GlabelsBase):
    """Simple wrapper for glabels-3-batch"""

    def __init__(
            self,
            path: str = 'glabels-3-batch',
            *,
            command_env: List[str] = None,
            logger: any = None,
            echo: bool = False,
    ):
        """
        :param path: Path to glabels-3-batch.
        :param command_env: Command environment.
            For example, ['xvfb-run', '--wait=0.1'] will call `xvfb-run --wait=0.1 glabels-3-batch`.
        :param logger: Logger.
        :param echo: Echo output of glabels-3-batch to logger.
        """
        super().__init__(path, command_env=command_env, logger=logger, echo=echo)

    def run(
            self,
            template: Union[str, bytes] = None,
            stdin: bytes = None,
            *,
            output: str = None,
            sheets: int = None,
            copies: int = None,
            first: int = None,
            outline: bool = False,
            reverse: bool = False,
            cropmarks: bool = False,
            input_file: Union[str, bytes] = None,
    ) -> Optional[bytes]:
        """
        :param template: gLabels project file to print. It can be a file path or bytes.
        :param stdin: Send input to glabels-batch-qt.
            Сan be a file with template arguments if the template specifies <Merge src="/dev/stdin" type="...">.
            Сannot be set if template parameter is given in bytes.

        :param output: Set output filename.
            If not specify, output will be returned by the function in byte form.
        :param sheets: Set number of sheets.
        :param copies: Set number of copies.
        :param first: Set starting position.
        :param outline: Print label outlines.
        :param reverse: Print in reverse (mirror image).
        :param cropmarks: Print crop marks.
        :param input_file: Set input filename.
        :return: STDOUT of glabels-3-batch
        :raises Glabels3RunError:
        """
        args = []
        _stdin = b''

        # options
        if output:
            args.extend(['--output', output])
        else:
            # To STDOUT as default
            args.extend(['--output', '/dev/stdout'])

        if sheets:
            if not isinstance(sheets, int):
                raise ValueError("Sheets must be int")
            args.extend(['--sheets', str(sheets)])
        if copies:
            if not isinstance(copies, int):
                raise ValueError("Copies must be int")
            args.extend(['--copies', str(copies)])
        if first:
            args.extend(['--first', str(first)])
        if outline:
            args.append('--outline')
        if cropmarks:
            args.append('--cropmarks')
        if reverse:
            args.append('--reverse')
        if input_file:
            if stdin is not None:
                raise ValueError("Only one file can be sent to stdin")

            if isinstance(input_file, str):
                self.raise_if_not_exist(input_file)
                args.extend(['--input', input_file])
            elif isinstance(input_file, bytes):
                args.extend(['--input', '-'])
                _stdin = input_file
            else:
                raise TypeError("input_file must be bytes or str")
        #

        # file
        if isinstance(template, str):
            self.raise_if_not_exist(template)
            args.append(template)
        elif isinstance(template, bytes):
            if stdin is not None:
                raise ValueError("Only one file can be sent to stdin")

            if isinstance(input_file, bytes):
                raise ValueError("You cannot send a template and an input file to stdin at the same time")

            args.append("-")
            _stdin = template
        else:
            raise TypeError("template must be str or bytes")

        if stdin is not None:
            _stdin = stdin
        #

        result = self._run(args, stdin=_stdin)
        return result if result else None
