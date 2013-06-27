import textwrap

from .. import HelpFormatter


def create_parser(parser):
    parser = parser.add_parser(
        'archive',
        formatter_class=HelpFormatter,
        help='archive old backups',
        add_help=False,
        description=textwrap.dedent('''
            Archive old backups
        '''),
        epilog=None
    )

    parser.set_defaults(
        main='{}.main'.format(__name__),
        config='x.y'
    )

    options = parser.add_argument_group(title='Options')
    options.add_argument(
        '-h', '--help',
        action='help',
        help='show this help message and exit'
    )


def main(ctx):
    raise NotImplementedError('Not yet made')
