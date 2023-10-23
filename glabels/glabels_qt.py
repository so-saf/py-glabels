from typing import List, Dict, Union, Optional

from glabels._base import GlabelsBase


class GLabelsBatchQT(GlabelsBase):
    """Simple wrapper for glabels-batch-qt"""

    def __init__(
            self,
            path: str = 'glabels-batch-qt',
            *,
            command_env: List[str] = None,
            logger: any = None,
            echo: bool = False,
            qt_args: Dict[str, str] = None,
    ):
        """
        :param path: Path to glabels-batch-qt.
        :param command_env: Command environment.
            For example, ['xvfb-run', '--wait=0.1'] will call `xvfb-run --wait=0.1 glabels-batch-qt`.
        :param logger: Logger.
        :param echo: Echo output of glabels-batch-qt to logger.
        :param qt_args: Qt specific options.
            For example, {"platform": "offscreen"} will call "... --platform offscreen ..."
            See `glabels-batch-qt --help-all` for details.
        """
        super().__init__(path, command_env=command_env, logger=logger, echo=echo)

        if qt_args:
            self.base_args.extend([f'--{k} {v}' for k, v in qt_args.items()])

    def version(self) -> str:
        result = self._run(['--version'])
        return result.decode().split()[1]

    def run(
            self,
            template: Union[str, bytes] = None,
            stdin: bytes = None,
            *,
            printer: str = None,
            output: str = None,
            sheets: int = None,
            copies: int = None,
            collate: bool = False,
            group: bool = False,
            first: int = None,
            outlines: bool = False,
            crop_marks: bool = False,
            reverse: bool = False,
            define: dict = None,
    ) -> Optional[bytes]:
        """
        :param template: gLabels project file to print. It can be a file path or bytes.
        :param stdin: Send input to glabels-batch-qt.
            Сan be a file with template arguments if the template specifies <Merge src="/dev/stdin" type="...">.
            Сannot be set if template parameter is given in bytes.

        :param printer: Send output to printer.
        :param output: Set output filename.
            If not specify, output will be returned by the function in byte form.
        :param sheets: Set number of sheets.
        :param copies: Set number of copies.
        :param collate: Collate merge copies.
        :param group: Start each merge group on a new page.
        :param first: Set starting position.
        :param outlines: Print label outlines.
        :param crop_marks: Print crop marks.
        :param reverse: Print in reverse (mirror image).
        :param define: Set user variable <var> to <value>
        :return: STDOUT of glabels-batch-qt
        :raises GlabelsQTRunError:
        """
        args = []
        _stdin = b''

        # options
        if printer and output:
            raise ValueError("Can't set both printer and output")
        elif printer:
            args.extend(['--printer', printer])
        elif output:
            args.extend(['--output', output])
        else:
            # To STDOUT as default
            args.extend(['--output', '-'])

        if sheets:
            if not isinstance(sheets, int):
                raise ValueError("Sheets must be int")
            args.extend(['--sheets', str(sheets)])
        if copies:
            if not isinstance(copies, int):
                raise ValueError("Copies must be int")
            args.extend(['--copies', str(copies)])
        if collate:
            args.append('--collate')
        if group:
            args.append('--group')
        if first:
            args.extend(['--first', str(first)])
        if outlines:
            args.append('--outlines')
        if crop_marks:
            args.append('--crop-marks')
        if reverse:
            args.append('--reverse')
        if define:
            for k, v in define.items():
                args.extend(['--define', f'{str(k)}={str(v)}'])
        #

        # file
        if isinstance(template, str):
            self.raise_if_not_exist(template)
            args.append(template)
        elif isinstance(template, bytes):
            if stdin is not None:
                raise ValueError("Standard input is supplied with template")

            args.append("-")
            _stdin = template

        if stdin is not None:
            _stdin = stdin
        #

        result = self._run(args, stdin=_stdin)
        return result if result else None
