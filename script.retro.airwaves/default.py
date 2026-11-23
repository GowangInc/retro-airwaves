import json
from pathlib import Path
from time import monotonic, time

import xbmc
import xbmcgui

from resources.guide import select_channel
from resources.schedule import media_url, tune

NAME = 'Retro Airwaves'
FULLSCREEN_VIDEO = 12005


class ChannelPlayer(xbmc.Player):
    def onAVStarted(self):
        self.started = True

    def onPlayBackEnded(self):
        self.outcome = 'ended'

    def onPlayBackStopped(self):
        self.outcome = 'stopped'

    def onPlayBackError(self):
        self.outcome = 'error'


def play_channel(channel, monitor):
    player = ChannelPlayer()
    while not monitor.abortRequested():
        now = time()
        slot = tune(channel, now)
        program = slot.program
        url = media_url(program)
        item = xbmcgui.ListItem(label=program['title'], path=url, offscreen=True)
        tag = item.getVideoInfoTag()
        tag.setTitle(program['title'])
        tag.setPlot(f"{channel['name']} · Internet Archive: {program['item']}")
        item.setProperty('StartOffset', f'{now - slot.starts_at:.3f}')
        player.started = False
        player.outcome = None
        player.play(url, item)
        deadline = monotonic() + 25
        fullscreen = False
        while player.outcome is None and not monitor.waitForAbort(0.2):
            if player.started:
                if xbmcgui.getCurrentWindowId() == FULLSCREEN_VIDEO:
                    fullscreen = True
                elif fullscreen and player.isPlayingVideo():
                    player.stop()
                    return
            elif monotonic() >= deadline:
                player.stop()
                player.outcome = 'error'
                break

        if monitor.abortRequested() or player.outcome == 'stopped':
            return
        remaining = slot.ends_at - time()
        if player.outcome != 'ended' or remaining > 3:
            xbmcgui.Dialog().notification(NAME, f"Could not finish {program['title']}", xbmcgui.NOTIFICATION_WARNING, 4000)
            return
        if remaining > 0 and monitor.waitForAbort(remaining):
            return


def main():
    channels = json.loads(Path(__file__).with_name('resources').joinpath('channels.json').read_text(encoding='utf-8'))
    monitor = xbmc.Monitor()
    previous = 0
    while not monitor.abortRequested():
        previous = select_channel(channels, previous, monitor)
        if previous < 0:
            return
        play_channel(channels[previous], monitor)


if __name__ == '__main__':
    main()
