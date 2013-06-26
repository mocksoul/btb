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

    historic_group = parser.add_argument_group(
        title='Backup history management'
    )
    historic_group.add_argument(
        '--max-age', metavar='AGE',
        default='1w',
        help=textwrap.dedent('''
            Max snapshots age.
            Examples:
             - 30 (30 days)
             - 2d10h (2 days 10 hours)
             - 10m (invalid! cant distinguish between months and minutes)
             - 10mi (10 minutes)
             - 10mo (10 months)
             - 10s1h (stupid form, but valid: 1 hour 10 seconds)
        ''').strip()
    )

    options = parser.add_argument_group(title='Options')
    options.add_argument(
        '-h', '--help',
        action='help',
        help='show this help message and exit'
    )


def main(ctx):
    raise NotImplementedError('Not yet made')
