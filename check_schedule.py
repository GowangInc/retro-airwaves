import json
import sys
from pathlib import Path

addon = Path(__file__).with_name('script.retro.airwaves')
sys.path.insert(0, str(addon))
from resources.schedule import EPOCH, media_url, tune


def main():
    channels = json.loads((addon / 'resources' / 'channels.json').read_text(encoding='utf-8'))
    for channel in channels:
        programs = channel['programs']
        assert programs and all(p['seconds'] > 0 for p in programs)
        anchor = EPOCH - channel['phase']
        first = tune(channel, anchor)
        assert first.program == programs[0] and first.starts_at == anchor
        for pos, program in enumerate(programs):
            next_program = programs[(pos + 1) % len(programs)]
            cut = anchor + program['seconds']
            just_before = tune(channel, cut - 0.25)
            just_after = tune(channel, cut + 0.25)
            assert just_before.program == program and just_before.next_program == next_program
            assert abs(just_before.ends_at - cut) < 0.001
            assert just_after.program == next_program and abs(just_after.starts_at - cut) < 0.001
            anchor = cut
        assert tune(channel, EPOCH - channel['phase'] - 0.25).program == programs[-1]
    assert media_url({'item': 'old films', 'file': 'clip #1.mp4'}) == 'https://archive.org/download/old%20films/clip%20%231.mp4'
    print(f'Schedule cutovers, wraparound and stream URLs: {len(channels)} channels passed')


if __name__ == '__main__':
    main()
