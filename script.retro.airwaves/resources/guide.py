from datetime import datetime
from pathlib import Path
from time import time

import xbmcgui

from resources.schedule import tune

CHANNELS = 9000
BACK_ACTIONS = {9, 10, 92}  # Previous menu, parent directory, navigation back.
ADDON_DIR = str(Path(__file__).resolve().parents[1])
ICON_DIR = Path(ADDON_DIR) / 'resources/skins/default/media/channels'


class Guide(xbmcgui.WindowXML):
    def onInit(self):
        self.window_id = xbmcgui.getCurrentWindowId()
        self.rows = self.getControl(CHANNELS)
        self.entries = []
        self.starts = [None] * len(self.channels)
        for number, channel in enumerate(self.channels, 1):
            item = xbmcgui.ListItem(label=channel['name'].upper())
            item.setProperty('Number', f'{number:02d}')
            item.setArt({'thumb': str(ICON_DIR / f"{channel['icon']}.png")})
            self.entries.append(item)
        self.refresh()
        self.rows.reset()
        self.rows.addItems(self.entries)
        self.setFocusId(CHANNELS)
        self.rows.selectItem(self.previous)
        self.ready = True

    def refresh(self):
        now = time()
        stamp = datetime.fromtimestamp(now)
        self.getControl(9010).setLabel(stamp.strftime('%H:%M'))
        self.getControl(9011).setLabel(stamp.strftime('%a  %d %b %Y').upper())
        for index, (channel, item) in enumerate(zip(self.channels, self.entries)):
            slot = tune(channel, now)
            start = round(slot.starts_at, 3)
            if start == self.starts[index]:
                continue
            self.starts[index] = start
            item.setLabel2(slot.program['title'])
            item.setProperty('Since', datetime.fromtimestamp(slot.starts_at).strftime('%H:%M'))
            item.setProperty('UpNext', slot.next_program['title'])
            item.setProperty('NextAt', datetime.fromtimestamp(slot.ends_at).strftime('%H:%M'))

    def onClick(self, control_id):
        if control_id == CHANNELS:
            index = self.rows.getSelectedPosition()
            if index >= 0:
                self.selected = index
                self.close()

    def onAction(self, action):
        if action.getId() in BACK_ACTIONS:
            self.selected = -1
            self.close()


def select_channel(channels, previous, monitor):
    window = Guide('Airwaves.xml', ADDON_DIR, 'default', '1080i')
    window.channels = channels
    window.previous = previous
    window.ready = False
    window.selected = None
    window.show()
    try:
        while (window.selected is None
               and (not window.ready or xbmcgui.getCurrentWindowId() == window.window_id)
               and not monitor.waitForAbort(1)):
            if window.ready and window.selected is None:
                window.refresh()
        return -1 if window.selected is None else window.selected
    finally:
        if window.selected is None:
            window.close()
