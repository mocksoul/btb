from collections import namedtuple


class Version(namedtuple('VersionBase', 'major minor maintainance extra')):
    def __str__(self):
        if all([i is None for i in self][:3]):
            return self[3]
        dotted = '.'.join([str(i) for i in self[:3] if i is not None])
        if not self[3]:
            return dotted
        return '{}-{}'.format(dotted, self[3])


PROGRAM = 'btb'
VERSION = Version(0, 1, None, 'dev')
