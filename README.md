# Retro Airwaves

Retro Airwaves is an independent alternative to [Spelunkr](https://spelunkr.tv/app), with the same 18-channel lineup in Kodi and the browser. Both guides show archival film and television on a shared clock. Neither uses Spelunkr or requires an account.

![Retro Airwaves in Kodi: eight visible channels with Now Playing, Up Next, and Later columns](screenshots/guide.jpg)

[See the guide scrolled to channels 11–18](screenshots/guide-scrolled.jpg).

## Watch in a browser

Serve the repository root with any static HTTP server and open `/web/`. Choose a channel to join the program already in progress. The browser streams directly from the archives; if a stream is unavailable, use the program source link or try another channel. No Kodi installation is needed.

## Install on Kodi

1. Download the `script.retro.airwaves-*.zip` add-on package from the [latest release](../../releases/latest). Do not use GitHub's automatic source archive.
2. In Kodi, open **Add-ons → Add-on browser → Install from zip file** and pick the downloaded ZIP. If Kodi requires **Unknown sources**, enable it only long enough to install the ZIP.
3. Open **Retro Airwaves** from **Program add-ons**. If your skin supports Home shortcuts, add `RunAddon(script.retro.airwaves)`.

Tested on Kodi 20.5 (Nexus). The add-on uses Kodi's player to stream from the Internet Archive, Wikimedia Commons, NOAA, and the National Park Service. No account, separate server, or IPTV configuration is required. The ZIP does not change your skin or existing Live TV setup.

## Use the guide

The guide shows eight channels at a time. Each row shows **Now Playing**, **Up Next**, and **Later** (the program after Up Next), with start times in local time. Use **Up/Down** to scroll and **OK** to tune in live. **Stop** returns to the guide; **Back** closes it.

The first six channels are **Kids Club** (ranger activities and animation), **Storybook** (fairy tales and animated stories), **Time Travel** (history), **Ocean Life** (marine science), **Deep Time** (fossils and geology), and **Science Lab** (NASA education shows). The rest of the lineup includes Oddities, Space, Toons, In Motion, Retro Tech, Field Notes, Westerns, Film Noir, Sci-Fi, Silent Film, Newsreels, and Classroom. The guide is not a parental-control or ratings filter.

![A frame from the 1941 Superman cartoon playing fullscreen in Kodi](screenshots/playback.jpg)

Playback example: [Superman (1941)](https://archive.org/details/superman_1941), marked public domain by the Internet Archive item.

## Develop

The lineup is in `script.retro.airwaves/resources/channels.json`. For Internet Archive entries, see `https://archive.org/details/<item>` for the source and rights information. Direct streams instead carry `url` and `source_page` fields. Use the exact stream duration in seconds; editing durations or order changes the UTC schedule for that channel. Channel badges are 96×96 indexed PNGs under `resources/skins/default/media/channels/`.

Run `python3 -B check_schedule.py` to check cutovers, wraparound, and URL encoding. When packaging, put the `script.retro.airwaves/` folder at the ZIP root and include a copy of `LICENSE` in that folder.

## Credits

Inspired by [Spelunkr](https://spelunkr.tv/) and vintage cable guides. Selected titles overlap with Spelunkr's public listings, but the artwork, schedule, and app are independent. Retro Tech streams unmodified [Computer Chronicles](https://archive.org/details/computerchronicles) episodes under their item-level [CC BY-NC-ND 2.0](https://creativecommons.org/licenses/by-nc-nd/2.0/) licenses. No footage is bundled; see the source listing for each film.

Original code and guide artwork are provided under the [MIT License](LICENSE). The playback screenshot shows third-party archival footage and is not covered by that license.

