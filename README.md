# Captain America on Screen: a TimelineJS timeline

An interactive [TimelineJS](https://timeline.knightlab.com/) timeline of Captain America in the Marvel Cinematic Universe, published with GitHub Pages.

**Live site:** https://kolby-white.github.io/captain-america-timeline/

## What changed from the original spreadsheet

| Area | Original | Revised |
|---|---|---|
| Scope | 5 entries: four films and one series | 12 entries: the Captain America films, the four Avengers films Steve leads, *The Falcon and the Winter Soldier*, *Thunderbolts\**, and the upcoming *Avengers: Doomsday* (Dec 18, 2026) and *Secret Wars* (Dec 17, 2027) |
| Title slide | Headline only | Intro text, a poster and a background color |
| Organization | No groups | Groups (Captain America films, Avengers team-ups, Disney+ series, Related films, Upcoming) and **eras** (Steve Rogers era, Sam Wilson era, Coming soon) |
| Second view | None | A **Story order** toggle that reorders entries by when they happen in the MCU (1943 to about 2027) |
| Text | Long quotes copied from ScreenRant with no link | Original summaries that track the shield's story from Steve to Sam, each with a "Read more" source link |
| Accuracy | "the new Falcon (Danny Ramierez)" | "Joaquín Torres (Danny Ramirez) as the new Falcon" |
| Media | Images hotlinked from Bing, Amazon and a poster-print store, which can break or vanish | Official posters from Wikipedia, linked to their articles |
| Credits and accessibility | Media Credit and Alt Text blank | Every image has a credit and descriptive alt text |
| Dates | Raw dates only | Display dates ("Released July 22, 2011"); the series shows its full run (Mar 19 to Apr 23, 2021) |

## Further ideas

- Add trailers: put an official Marvel YouTube trailer URL in the Media column of any slide. TimelineJS embeds it automatically.
- Add the comics: Captain America #1 (1941), Sam Wilson becoming Captain America in the comics (2014), and the 1944 serial and 1990 film.
- Add actor slides for Chris Evans, Anthony Mackie and Sebastian Stan.
- After *Avengers: Doomsday* comes out, update its slide with the story.

## Files

- `index.html`: the page, with the TimelineJS embed and the release/story toggle
- `data/release.json`, `data/chronology.json`: the timeline data
- `data/release.csv`: the release-order data in TimelineJS's Google Sheet column layout. Import it into your sheet if you want to keep editing there.
- `build.py`: regenerates all three data files. Edit the entries in it, then run `python build.py`.

Fan project for education and commentary. Not affiliated with Marvel or Disney. Posters © Marvel Studios / Disney.
