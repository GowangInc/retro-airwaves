from datetime import datetime
from pathlib import Path
from time import time

import xbmcgui

from resources.schedule import tune

CHANNELS = 9000
BACK_ACTIONS = {9, 10, 92}  # Previous menu, parent directory, navigation back.
ADDON_DIR = str(Path(__file__).resolve().parents[1])


class Guide(xbmcgui.WindowXML):
    def onInit(self):
        self.window_id = xbmcgui.getCurrentWindowId()
        self.rows = self.getControl(CHANNELS)
        self.refresh()
        self.setFocusId(CHANNELS)
        self.rows.selectItem(self.previous)
        self.ready = True

    def refresh(self):
        now = time()
        stamp = datetime.fromtimestamp(now)
        self.getControl(9010).setLabel(stamp.strftime('%H:%M'))
        self.getControl(9011).setLabel(stamp.strftime('%a  %d %b %Y').upper())
        slots = [tune(channel, now) for channel in self.channels]
        starts = tuple(round(slot.starts_at, 3) for slot in slots)
        if starts == self.starts:
            return
        selected = self.rows.getSelectedPosition() if self.starts else self.previous
        self.starts = starts
        entries = []
        for number, (channel, slot) in enumerate(zip(self.channels, slots), 1):
            item = xbmcgui.ListItem(label=channel['name'].upper(), label2=slot.program['title'], offscreen=True)
            item.setProperty('Number', f'{number:02d}')
            item.setProperty('Since', datetime.fromtimestamp(slot.starts_at).strftime('%H:%M'))
            item.setProperty('UpNext', slot.next_program['title'])
            item.setProperty('NextAt', datetime.fromtimestamp(slot.ends_at).strftime('%H:%M'))
            entries.append(item)
        self.rows.reset()
        self.rows.addItems(entries)
        self.rows.selectItem(max(0, selected))

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
    window.starts = ()
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
