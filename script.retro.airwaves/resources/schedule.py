from typing import NamedTuple
from urllib.parse import quote

EPOCH = 1767225600  # 2026-01-01 00:00:00 UTC


class Slot(NamedTuple):
    program: dict
    next_program: dict
    starts_at: float
    ends_at: float


def tune(channel, now):
    """Return the half-open slot containing this Unix timestamp."""
    programs = channel['programs']
    pos = (now - EPOCH + channel['phase']) % sum(p['seconds'] for p in programs)
    for index, program in enumerate(programs):
        duration = program['seconds']
        if pos < duration:
            start = now - pos
            return Slot(program, programs[(index + 1) % len(programs)], start, start + duration)
        pos -= duration


def media_url(program):
    item = quote(program['item'], safe='')
    filename = quote(program['file'], safe='')
    return f'https://archive.org/download/{item}/{filename}'
