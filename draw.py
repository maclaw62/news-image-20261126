"""Draw the 26 November 2026 world-news board (1024x1024 PNG).

Hybrid hierarchy: three big stories across the top, six medium
stories under them, then dense smaller rows for the rest of the day.
Every headline was checked against reporting dated Thursday
26 November 2026 (Reuters, AP, Al Jazeera, BBC, CNN, AFP via CNA).
"""

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
BG = (246, 241, 231)
INK = (24, 22, 20)
MUTED = (96, 90, 82)
CARD = (255, 253, 248)
LINE = (201, 193, 178)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANSB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

REGION_COLORS = {
    "AMERICAS": (31, 122, 76),
    "EUROPE": (37, 84, 166),
    "MIDDLE EAST": (178, 44, 36),
    "AFRICA": (183, 102, 26),
    "ASIA": (166, 124, 18),
    "MARKETS": (110, 62, 160),
    "TECH & SPACE": (18, 116, 120),
}

TOP = [
    ("AMERICAS", "Trump fires tariffs at 14 partners",
     "China, EU and Japan targeted; 20-40% proposed, lower caps promised."),
    ("EUROPE", "Kyiv hit; Zelenskiy warns of mass strike",
     "Missiles wound 7, hit a mall; grain ships struck near Odesa."),
    ("MIDDLE EAST", "Hormuz mines, Houthi claim lift oil",
     "IRGC says two tankers burned; Brent near $94.7 on supply fears."),
]

ALSO = [
    ("MIDDLE EAST", "Gaza strikes kill 9, incl. deputy minister",
     "Deir al-Balah: Khaled Abu Nada killed, medics say."),
    ("MIDDLE EAST", "Drone kills two Italians in Kuwait",
     "Rheinmetall technicians, source tells Reuters."),
    ("AFRICA", "Cairo tanker fire kills 31",
     "Ring Road blaze injures 21; suspect arrested, prosecutors say."),
    ("AFRICA", "Congo Ebola passes 12,000 cases",
     "12,021 cases and 5,904 deaths."),
    ("EUROPE", "Spain's de Cos set to lead ECB",
     "First Spaniard to succeed Lagarde."),
    ("ASIA", "Kim urges wider tactical nuclear use",
     "Deploy across domains, KCNA says."),
]

REST = [
    ("EUROPE", "EU budget summit deadlocked",
     "Meloni: 'light-years' from a \u20ac1.6tn deal."),
    ("EUROPE", "UK net migration falls to 77,000",
     "Lowest since 1997 outside the pandemic."),
    ("EUROPE", "Germany arrests 2 over synagogue plot",
     "Iraqi suspects held over alleged Cologne plan."),
    ("EUROPE", "Serbia sets Dec 27 presidential vote",
     "After student-led movement's October win."),
    ("MIDDLE EAST", "Eisenkot revives coalition talks",
     "Resolves dispute with left-wing faction."),
    ("ASIA", "China tells Japan: stop stirring seas",
     "Beijing protests radar, drone aid to Philippines."),
    ("ASIA", "Indonesia mine flood: 13 dead, 13 trapped",
     "Rain halts Bogor rescue 100m underground."),
    ("ASIA", "Bangladesh garment protests dispersed",
     "Tear gas used after 36% minimum-wage rise."),
    ("ASIA", "Bangkok refinery blast injures 9",
     "Bangchak shuts units; fire controlled in 30 min."),
    ("AFRICA", "Kenya court halts Ebola quarantine site",
     "US-backed facility breached constitution."),
    ("AMERICAS", "Argentina weighs ending primaries",
     "Senate bill could boost Milei's re-election bid."),
    ("AMERICAS", "Lula sounds out Bradesco chief",
     "Trabuco approached as finance minister, sources say."),
    ("EUROPE", "London Tube strikes begin",
     "First of eight winter strike days hits commuters."),
    ("AMERICAS", "Storm postpones Macy's parade",
     "100th edition moved to Saturday, a first."),
    ("TECH & SPACE", "SpaceX cleared for 1m satellites",
     "FCC backs Starmind orbital data centres."),
    ("EUROPE", "Ukraine drones hit Russian refinery",
     "Fire at Slavyansk ECO plant in Krasnodar."),
    ("AMERICAS", "Second judge blocks birthright order",
     "Trump citizenship curbs halted again in court."),
    ("ASIA", "Trade chiefs meet in Vietnam",
     "CPTPP, ASEAN and EU gather under tariff shadow."),
]


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def card(draw, x, y, w, h, region, head, sub, head_size, sub_size, max_head=3):
    draw.rounded_rectangle([x, y, x + w, y + h], radius=8,
                           fill=CARD, outline=LINE, width=1)
    color = REGION_COLORS.get(region, INK)
    draw.rounded_rectangle([x, y, x + 7, y + h], radius=3, fill=color)
    tx = x + 16
    inner = w - 26
    compact = head_size <= 13
    draw.text((tx, y + (5 if compact else 8)), region,
              font=font(SANSB, 9 if compact else 11), fill=color)
    hf = font(SANSB, head_size)
    lines = wrap(draw, head, hf, inner)[:max_head]
    ly = y + (19 if compact else 26)
    for ln in lines:
        draw.text((tx, ly), ln, font=hf, fill=INK)
        ly += head_size + (2 if compact else 3)
    sf = font(SANS, sub_size)
    for ln in wrap(draw, sub, sf, inner)[:2]:
        if ly + sub_size + 4 > y + h:
            break
        draw.text((tx, ly + 1), ln, font=sf, fill=MUTED)
        ly += sub_size + 2


def section(draw, x, y, label):
    draw.text((x, y), label, font=font(SANSB, 15), fill=MUTED)


def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    m = 28
    d.text((m, 20), "THE WORLD IN ONE DAY", font=font(SANSB, 17), fill=MUTED)
    right = "THURSDAY"
    d.text((W - m - d.textlength(right, font=font(SANSB, 17)), 20),
           right, font=font(SANSB, 17), fill=MUTED)
    d.text((m, 42), "26 NOVEMBER 2026", font=font(SERIF, 63), fill=INK)
    d.text((m, 118), "27 dated stories \u00b7 6 regions \u00b7 date-checked",
           font=font(SANSB, 18), fill=INK)
    d.line([m, 148, W - m, 148], fill=INK, width=3)
    d.line([m, 154, W - m, 154], fill=INK, width=1)

    col_w = (W - 2 * m - 20) // 3
    xs = [m, m + col_w + 10, m + 2 * (col_w + 10)]

    section(d, m, 164, "TOP STORIES")
    for i, (region, head, sub) in enumerate(TOP):
        card(d, xs[i], 186, col_w, 122, region, head, sub, 24, 12)

    section(d, m, 320, "ALSO TODAY")
    for i, (region, head, sub) in enumerate(ALSO):
        card(d, xs[i % 3], 342 + (i // 3) * 92, col_w, 86,
             region, head, sub, 18, 11)

    section(d, m, 528, "THE REST OF THE DAY")
    for i, (region, head, sub) in enumerate(REST):
        card(d, xs[i % 3], 548 + (i // 3) * 64, col_w, 59,
             region, head, sub, 12, 9, max_head=2)

    d.line([m, 952, W - m, 952], fill=INK, width=2)
    ticker = ("Tariffs \u2192 Kyiv strike \u2192 Hormuz mines \u2192 "
              "Cairo fire \u2192 Ebola 12,000 \u2192 ECB pick \u2192 "
              "Macy's storm")
    d.text((m, 960), ticker, font=font(SANSB, 15), fill=INK)
    d.text((m, 984),
           "One image \u00b7 Thursday 26 November 2026 \u00b7 "
           "Sources: Reuters \u00b7 AP \u00b7 Al Jazeera \u00b7 BBC \u00b7 CNN",
           font=font(SANS, 12), fill=MUTED)
    img.save("entry.png", optimize=True)


if __name__ == "__main__":
    main()
