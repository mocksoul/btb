import sys

from .ui.console import enter_ui


def main():
    return enter_ui(sys.argv[1:])


if __name__ == '__main__':
    raise SystemExit(main())
