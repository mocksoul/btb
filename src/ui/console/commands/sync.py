import textwrap

from .. import HelpFormatter


def create_parser(parser):
    parser = parser.add_parser(
        'sync',
        formatter_class=HelpFormatter,
        help='run synchronization',
        add_help=False,
        description=textwrap.dedent('''
            Run backup
        '''),
        epilog=None
    )

    parser.set_defaults(
        main='{}.main'.format(__name__),
        config='x.y'
    )

    path_selection_group = parser.add_argument_group(
        title='Path selection'
    )
    path_selection_group.add_argument(
        'source',
        metavar='SOURCE',
        help='source path'
    )
    path_selection_group.add_argument(
        'target',
        metavar='TARGET',
        help='target path'
    )
    path_selection_group.add_argument(
        '--exclude', type=list, nargs='*',
        metavar='PATTERN',
        default=[],
        help='exclude pattern (rsync-like), can be specified multiple times'
    )

    options = parser.add_argument_group(title='Options')
    options.add_argument(
        '-h', '--help',
        action='help',
        help='show this help message and exit'
    )


def main(ctx):
    raise NotImplementedError('Not yet made')
