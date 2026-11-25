# news-image-20261125

[![make.fun · news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/asfel307/news-image-20261125/rank.svg)](https://make.fun/bounty/news-image-20261125/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/asfel307/news-image-20261125/reward.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)

## The World Today — Wednesday, 25 November 2026

A single front-page newspaper infographic summing up the world's news for
Wednesday, 25 November 2026. One lead story on China launching Shenzhou-24
— carrying Pakistani astronaut Muhammad Zeeshan Ali as the first foreign
astronaut to visit the Tiangong space station — plus five more stories: an
Australia–Solomon Islands security pact; Zelenskiy confirming Ukraine's
drone strike on a Russian ship in the Gulf of Finland; Houthis hitting
Riyadh's tallest tower; the WHO evacuating staff from a hospital in the
Democratic Republic of the Congo; and a supermarket hostage standoff in
Cartagena, Colombia.

The image is drawn entirely in code with Pillow: warm cream paper, dark
slate ink, dark-teal and gold accents, a big serif masthead, and a small
pictogram for every story — a rocket, a Pacific map, a ship, a tower, a
hospital cross, and a storefront. No photos, no downloaded assets, no
network calls anywhere in the build.

## The six stories

The front page is dated Wednesday, 25 November 2026 and was compiled in
the early hours of that day (UTC). Each story was checked against wire
reporting before it was drawn.

1. **Lead — China launches Shenzhou-24; first foreign astronaut reaches
   Tiangong.** Shenzhou-24 lifted off from Jiuquan at 00:18 UTC carrying
   commander Tang Hongbo, Wu Yi, and Pakistani payload specialist Muhammad
   Zeeshan Ali — the first foreign astronaut ever to visit China's Tiangong
   space station.
   Sources: Xinhua / Reuters.
   https://www.chinadailyasia.com/hk/article/643205
2. **Australia and Solomon Islands sign security pact.** The two countries
   signed a security pact in Sydney making Canberra the island nation's
   defence partner of choice; Australian media reported the Solomon Islands'
   earlier security deal with China had been scrapped.
   Source: Reuters.
   https://www.srnnews.com/australia-and-solomon-islands-sign-security-pact/
3. **Zelenskiy confirms Ukraine hit a Russian ship in the Gulf of Finland.**
   President Volodymyr Zelenskiy confirmed Ukraine was responsible for the
   drone strike on a Russian cargo ship; the 16-member crew was evacuated
   and the ship was later towed to St Petersburg. Norway urged caution.
   Source: Reuters.
   https://www.devdiscourse.com/article/international/4011704-reuters-world-news-summary
4. **Houthis hit Riyadh's tallest tower; 11 wounded.** A strike on a tower
   in Riyadh's financial district wounded 11 people, including two Indian
   nationals, two Saudis, three Nepalis and four Egyptians, according to
   Saudi Civil Defense.
   Source: Reuters.
   https://www.devdiscourse.com/article/international/4011704-reuters-world-news-summary
5. **WHO evacuates staff from a hospital in DR Congo.** WHO staff were
   evacuated from a hospital in Akwe, Ituri province, after sheltering
   there for three days from fierce fighting; the area is also the centre
   of the country's Ebola outbreak.
   Source: WHO / Reuters.
   https://stockbiz.vn/en/news/international-news-on-november-25-new-developments-in-the-us-and-the-democratic-republic-of-the-congo/42897426
6. **Cartagena standoff: 10 of about 30 hostages freed.** Armed men seized
   an Éxito supermarket in Cartagena after a failed attempt to rob an
   armoured cash truck; ten hostages — elderly women — were released while
   around 20 remained inside as negotiations continued.
   Sources: Sky News / AP.
   https://www.qradio.com/news/q-radio-world-news/armed-men-take-at-least-20-hostages-in-supermarket-in-colombia-tourist-hotspot/

## How it works

`render.py` draws the front page with Pillow and writes `entry.png`
(1024×1024, under 1 MiB). `main.py` (Python standard library only) copies
`entry.png` byte for byte to the make.fun output directory, so both runs
produce identical bytes:

```sh
python3 render.py
MAKEFUN_OUTPUT_DIR=out python3 main.py
```
