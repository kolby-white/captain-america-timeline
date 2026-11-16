"""Builds the TimelineJS data files for the Captain America timeline.

Run:  python build.py
Writes:
  data/release.json      - entries in release order (the default view)
  data/chronology.json   - entries in in-universe story order
  data/release.csv       - release-order entries in the TimelineJS Google Sheet
                           column layout, ready to paste back into the sheet
"""
import csv
import json
import os

WIKI = "https://en.wikipedia.org/wiki/"
IMG = "https://upload.wikimedia.org/wikipedia/en/"
CREDIT = "Poster &copy; Marvel Studios / Disney, via Wikipedia"

# Each entry: release date, story-time dates (None = not placed), text, media.
ENTRIES = [
    dict(
        key="first-avenger",
        headline="Captain America: The First Avenger",
        group="Captain America films",
        release=(2011, 7, 22), release_end=None,
        story=(1943,), story_end=(1945,), story_label="Set in 1943&ndash;1945 (epilogue: 2011)",
        image=IMG + "3/37/Captain_America_The_First_Avenger_poster.jpg",
        alt="Poster for Captain America: The First Avenger showing Steve Rogers holding his shield",
        wiki="Captain_America:_The_First_Avenger",
        bg="#012e5d",
        text=("<p>Frail Brooklyn volunteer <b>Steve Rogers</b> (Chris Evans) is transformed by the "
              "Super Soldier Serum and becomes Captain America, leading the fight against HYDRA and "
              "the Red Skull during World War II.</p>"
              "<p>His sacrifice at the end of the war leaves him frozen in the Arctic ice for nearly "
              "seventy years &mdash; and his best friend, <b>Bucky Barnes</b>, presumed dead.</p>"),
    ),
    dict(
        key="avengers",
        headline="The Avengers",
        group="Avengers team-ups",
        release=(2012, 5, 4), release_end=None,
        story=(2012,), story_end=None, story_label="Set in 2012",
        image=IMG + "8/8a/The_Avengers_%282012_film%29_poster.jpg",
        alt="Poster for The Avengers showing the six original Avengers",
        wiki="The_Avengers_(2012_film)",
        bg="#3b4a5a",
        text=("<p>A man out of time, Steve is recruited by Nick Fury to lead Earth's Mightiest Heroes "
              "against Loki's invasion of New York &mdash; and learns to work alongside Tony Stark.</p>"),
    ),
    dict(
        key="winter-soldier",
        headline="Captain America: The Winter Soldier",
        group="Captain America films",
        release=(2014, 4, 4), release_end=None,
        story=(2014,), story_end=None, story_label="Set in 2014",
        image=IMG + "9/9e/Captain_America_The_Winter_Soldier_poster.jpg",
        alt="Poster for Captain America: The Winter Soldier showing Captain America with his shield",
        wiki="Captain_America:_The_Winter_Soldier",
        bg="#6084a3",
        text=("<p>Steve discovers HYDRA has been hiding inside S.H.I.E.L.D. since the war. With Black "
              "Widow and new ally <b>Sam Wilson</b> (Anthony Mackie) as the Falcon, he faces a deadly "
              "assassin: a brainwashed Bucky Barnes, the Winter Soldier.</p>"),
    ),
    dict(
        key="age-of-ultron",
        headline="Avengers: Age of Ultron",
        group="Avengers team-ups",
        release=(2015, 5, 1), release_end=None,
        story=(2015,), story_end=None, story_label="Set in 2015",
        image=IMG + "f/ff/Avengers_Age_of_Ultron_poster.jpg",
        alt="Poster for Avengers: Age of Ultron showing the Avengers facing Ultron",
        wiki="Avengers:_Age_of_Ultron",
        bg="#4a3f5c",
        text=("<p>The Avengers fight Ultron, a rogue AI built by Tony Stark. The destruction of Sokovia "
              "sets up the political fallout that will split the team.</p>"),
    ),
    dict(
        key="civil-war",
        headline="Captain America: Civil War",
        group="Captain America films",
        release=(2016, 5, 6), release_end=None,
        story=(2016,), story_end=None, story_label="Set in 2016",
        image=IMG + "5/53/Captain_America_Civil_War_poster.jpg",
        alt="Poster for Captain America: Civil War showing Captain America and Iron Man on opposing sides",
        wiki="Captain_America:_Civil_War",
        bg="#8a8a92",
        text=("<p>The <b>Sokovia Accords</b> would put the Avengers under United Nations oversight. Steve "
              "refuses to sign, sides with Bucky, and goes to war with Tony Stark &mdash; leaving the "
              "Avengers broken apart.</p>"),
    ),
    dict(
        key="infinity-war",
        headline="Avengers: Infinity War",
        group="Avengers team-ups",
        release=(2018, 4, 27), release_end=None,
        story=(2018,), story_end=None, story_label="Set in 2018",
        image=IMG + "4/4d/Avengers_Infinity_War_poster.jpg",
        alt="Poster for Avengers: Infinity War showing Thanos above the heroes",
        wiki="Avengers:_Infinity_War",
        bg="#5a2d4a",
        text=("<p>A bearded, fugitive Steve returns to defend Wakanda against Thanos. The heroes lose: "
              "Thanos's snap wipes out half of all life, Bucky and Sam included.</p>"),
    ),
    dict(
        key="endgame",
        headline="Avengers: Endgame",
        group="Avengers team-ups",
        release=(2019, 4, 26), release_end=None,
        story=(2023,), story_end=None, story_label="Set in 2023, five years after the Snap",
        image=IMG + "0/0d/Avengers_Endgame_poster.jpg",
        alt="Poster for Avengers: Endgame showing the surviving Avengers",
        wiki="Avengers:_Endgame",
        bg="#3d2a6b",
        text=("<p>Steve finally lifts Mjolnir, leads the final battle, then stays in the past to live a "
              "life with Peggy Carter. As an old man he <b>passes the shield to Sam Wilson</b>.</p>"),
    ),
    dict(
        key="fatws",
        headline="The Falcon and the Winter Soldier",
        group="Disney+ series",
        release=(2021, 3, 19), release_end=(2021, 4, 23),
        story=(2024,), story_end=None, story_label="Set in 2024",
        image=IMG + "9/9a/The_Falcon_and_the_Winter_Soldier_logo.png",
        alt="Title logo for The Falcon and the Winter Soldier",
        wiki="The_Falcon_and_the_Winter_Soldier",
        bg="#9e4f52",
        text=("<p>A six-episode Disney+ series. Unsure he deserves the shield, Sam gives it to the "
              "Smithsonian &mdash; only for the government to hand it to John Walker as a new Captain "
              "America. Teaming up with Bucky, Sam learns the legacy of Isaiah Bradley and finally "
              "<b>takes up the mantle himself</b>.</p>"),
    ),
    dict(
        key="brave-new-world",
        headline="Captain America: Brave New World",
        group="Captain America films",
        release=(2025, 2, 14), release_end=None,
        story=(2027,), story_end=None, story_label="Set around 2027",
        image=IMG + "a/a4/Captain_America_Brave_New_World_poster.jpg",
        alt="Poster for Captain America: Brave New World showing Sam Wilson as Captain America",
        wiki="Captain_America:_Brave_New_World",
        bg="#860000",
        text=("<p>The first Captain America film without Steve Rogers. Sam Wilson is now Captain America, "
              "with <b>Joaqu&iacute;n Torres</b> (Danny Ramirez) as the new Falcon, and he is pulled into "
              "a conspiracy around President Thaddeus Ross (Harrison Ford).</p>"),
    ),
    dict(
        key="thunderbolts",
        headline="Thunderbolts*",
        group="Related films",
        release=(2025, 5, 2), release_end=None,
        story=(2027,), story_end=None, story_label="Set around 2027",
        image=IMG + "9/90/Thunderbolts%2A_poster.jpg",
        alt="Poster for Thunderbolts* showing the team of antiheroes",
        wiki="Thunderbolts*",
        bg="#2f3b2f",
        text=("<p>Bucky Barnes, now a congressman, and John Walker (U.S. Agent) join a team of antiheroes "
              "&mdash; a look at what happened to the people who once stood beside, or in place of, "
              "Captain America.</p>"),
    ),
    dict(
        key="doomsday",
        headline="Avengers: Doomsday",
        group="Upcoming",
        release=(2026, 12, 18), release_end=None,
        story=None, story_end=None, story_label=None,
        image=IMG + "e/ee/Avengers_Doomsday_poster.jpg",
        alt="Poster for Avengers: Doomsday",
        wiki="Avengers:_Doomsday",
        bg="#1f2a33",
        text=("<p><b>Coming December 18, 2026.</b> The Russo brothers return to direct. A teaser revealed "
              "that Chris Evans is back as Steve Rogers, alongside Anthony Mackie's Sam Wilson.</p>"),
    ),
    dict(
        key="secret-wars",
        headline="Avengers: Secret Wars",
        group="Upcoming",
        release=(2027, 12, 17), release_end=None,
        story=None, story_end=None, story_label=None,
        image=None,
        alt=None,
        wiki="Marvel_Cinematic_Universe:_Phase_Six",
        bg="#1f2a33",
        text=("<p><b>Coming December 17, 2027.</b> The planned finale of the Multiverse Saga.</p>"),
    ),
]

TITLE_TEXT = ("<p>Every Captain America film, plus the Avengers team-ups and the Disney+ series that "
              "carry the story from <b>Steve Rogers</b> to <b>Sam Wilson</b>.</p>"
              "<p>Use the buttons above to switch between <b>release order</b> and "
              "<b>story order</b> (when each one takes place in the MCU).</p>")


def date(t):
    keys = ("year", "month", "day")
    return {k: str(v) for k, v in zip(keys, t)}


def fmt(t):
    months = ["January", "February", "March", "April", "May", "June", "July", "August",
              "September", "October", "November", "December"]
    return f"{months[t[1] - 1]} {t[2]}, {t[0]}"


def slide(e, mode):
    s = {
        "unique_id": f"{e['key']}-{mode}",
        "group": e["group"],
        "text": {
            "headline": e["headline"],
            "text": e["text"] + f'<p class="src"><a href="{WIKI}{e["wiki"]}" target="_blank" '
                                f'rel="noopener">Read more on Wikipedia</a></p>',
        },
        "background": {"color": e["bg"]},
    }
    if mode == "release":
        s["start_date"] = date(e["release"])
        if e["release_end"]:
            s["end_date"] = date(e["release_end"])
            s["display_date"] = f"Streamed {fmt(e['release'])} &ndash; {fmt(e['release_end'])}"
        else:
            verb = "Releases" if e["group"] == "Upcoming" else "Released"
            s["display_date"] = f"{verb} {fmt(e['release'])}"
    else:
        s["start_date"] = date(e["story"])
        if e["story_end"]:
            s["end_date"] = date(e["story_end"])
        s["display_date"] = f"{e['story_label']} &middot; released {e['release'][0]}"
    if e["image"]:
        s["media"] = {
            "url": e["image"],
            "thumbnail": e["image"],
            "credit": CREDIT,
            "alt": e["alt"],
            "link": WIKI + e["wiki"],
            "link_target": "_blank",
        }
    return s


def timeline(mode):
    if mode == "release":
        items = ENTRIES
        eras = [
            {"start_date": {"year": "2011"}, "end_date": {"year": "2019"},
             "text": {"headline": "Steve Rogers era"}},
            {"start_date": {"year": "2021"}, "end_date": {"year": "2025"},
             "text": {"headline": "Sam Wilson era"}},
            {"start_date": {"year": "2026"}, "end_date": {"year": "2027"},
             "text": {"headline": "Coming soon"}},
        ]
        subtitle = "Release order"
    else:
        items = sorted((e for e in ENTRIES if e["story"]), key=lambda e: (e["story"], e["release"]))
        eras = [
            {"start_date": {"year": "1943"}, "end_date": {"year": "1945"},
             "text": {"headline": "World War II"}},
            {"start_date": {"year": "2012"}, "end_date": {"year": "2023"},
             "text": {"headline": "Steve Rogers leads the Avengers"}},
            {"start_date": {"year": "2024"}, "end_date": {"year": "2027"},
             "text": {"headline": "Sam Wilson takes the shield"}},
        ]
        subtitle = "Story order (in-universe)"
    return {
        "title": {
            "text": {"headline": "Captain America on Screen",
                     "text": f"<p class=\"mode\">{subtitle}</p>" + TITLE_TEXT},
            "media": {
                "url": IMG + "3/37/Captain_America_The_First_Avenger_poster.jpg",
                "credit": CREDIT,
                "alt": "Poster for Captain America: The First Avenger",
            },
            "background": {"color": "#0b1f3a"},
        },
        "eras": eras,
        "events": [slide(e, mode) for e in items],
    }


def write_csv(path):
    cols = ["Year", "Month", "Day", "Time", "End Year", "End Month", "End Day", "End Time",
            "Display Date", "Headline", "Text", "Media", "Media Credit", "Media Caption",
            "Media Thumbnail", "Alt Text", "Type", "Group", "Background"]
    t = timeline("release")
    rows = [dict.fromkeys(cols, "")]
    rows[0].update({"Headline": t["title"]["text"]["headline"], "Text": TITLE_TEXT,
                    "Media": t["title"]["media"]["url"], "Media Credit": CREDIT,
                    "Alt Text": t["title"]["media"]["alt"], "Type": "title", "Background": "#0b1f3a"})
    for era in t["eras"]:
        r = dict.fromkeys(cols, "")
        r.update({"Year": era["start_date"]["year"], "End Year": era["end_date"]["year"],
                  "Headline": era["text"]["headline"], "Type": "era"})
        rows.append(r)
    for s in t["events"]:
        r = dict.fromkeys(cols, "")
        sd, ed, m = s["start_date"], s.get("end_date", {}), s.get("media", {})
        r.update({"Year": sd["year"], "Month": sd["month"], "Day": sd["day"],
                  "End Year": ed.get("year", ""), "End Month": ed.get("month", ""),
                  "End Day": ed.get("day", ""), "Display Date": s["display_date"],
                  "Headline": s["text"]["headline"], "Text": s["text"]["text"],
                  "Media": m.get("url", ""), "Media Credit": m.get("credit", ""),
                  "Media Thumbnail": m.get("thumbnail", ""), "Alt Text": m.get("alt", ""),
                  "Group": s["group"], "Background": s["background"]["color"]})
        rows.append(r)
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    os.makedirs(os.path.join(here, "data"), exist_ok=True)
    for mode in ("release", "chronology"):
        with open(os.path.join(here, "data", f"{mode}.json"), "w", encoding="utf-8") as f:
            json.dump(timeline(mode), f, indent=2, ensure_ascii=False)
    write_csv(os.path.join(here, "data", "release.csv"))
    print("Wrote data/release.json, data/chronology.json, data/release.csv")
