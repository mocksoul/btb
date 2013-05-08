import argparse
import textwrap

from ...__version__ import PROGRAM, VERSION


SUBCOMMANDS = (
    'commands.sync',
)


class ArgumentParser(argparse.ArgumentParser):
    def _get_formatter(self):
        return self.formatter_class(prog=self.prog, max_help_position=80, width=120)


class HelpFormatter(
    argparse.ArgumentDefaultsHelpFormatter,
    argparse.RawTextHelpFormatter
):
    pass


def import_by_name(name):
    module_name, fromlist = name.rsplit('.', 1)
    module = __import__(module_name, globals(), locals(), [fromlist])
    return getattr(module, fromlist)


def iterate_commands_mods(submod=None, only_commands=None):
    for module_name in SUBCOMMANDS:
        if only_commands and module_name not in only_commands:
            continue
        if submod:
            fromlist = []
            for submod_part in submod.split('.'):
                if not fromlist:
                    current = submod_part
                else:
                    current = '.' + submod_part
                fromlist.append(current)
        else:
            fromlist = []

        cmd_module = __import__(module_name, globals(), locals(), fromlist)

        if submod:
            current_item = cmd_module
            for submod_part in submod.split('.'):
                try:
                    current_item = getattr(current_item, submod_part)
                except AttributeError:
                    raise AttributeError('Module %s does not have attribute %s' % (
                        current_item.__name__, submod_part
                    ))
            yield current_item
        else:
            yield cmd_module


def create_main_parser(prog, version):
    parser = ArgumentParser(
        prog=prog,
        formatter_class=HelpFormatter,
        description=textwrap.dedent('''
            Modern and lightweight backup system
        '''),
        epilog=None,
        add_help=False
    )

    # Add info options (--help and --version)
    info_options = parser.add_argument_group(title='Informational')
    info_options_group = info_options.add_mutually_exclusive_group()
    info_options_group.add_argument(
        '-h', '--help', action='help',
        help='show this help message and exit'
    )
    info_options_group.add_argument(
        '-V', '--version', action='version',
        version=(
            '%(prog)s v{}'.format(version)
            if version[0].isdigit() else
            '%(prog)s {}'.format(version)
        ),
        help='show program version number and exit'
    )

    # Create subparsers
    subparsers = parser.add_subparsers(
        dest='cmd',
        title='Commands',
        description=textwrap.dedent('''
            %(prog)s functionality is splitted into different commands,
            they are named as "CMD" in this help.

            Each command has its own set of options (find them by running
            "%(prog)s CMD --help") and there are some global options
            mentioned earlier which can be applied to all commands.

            Only one command can be executed at a time.
        ''').strip(),
        metavar='COMMAND'
    )

    return parser, subparsers


def parse_args(args):
    parser, subparsers = create_main_parser(PROGRAM, str(VERSION))
    for create_cmd_parser in iterate_commands_mods('create_parser'):
        create_cmd_parser(subparsers)
    return parser.parse_args(args)


def enter_ui(args):
    args = parse_args(args)
    if isinstance(args.main, str):
        args.main = import_by_name(args.main)

    return args.main('ctx')
