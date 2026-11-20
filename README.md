# FRIDAY, EVERYWHERE AT ONCE — news-image-20261120

![Friday, Everywhere at Once](entry.png)

[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/Gillangzx/news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/Gillangzx/news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

Sum up 20 November 2026's world news in one image: a classic cream-paper
front page — **THE WORLD TODAY, Friday 20 November 2026** — built on the
winning front-page pattern (36 stories, 6 continents) with a simultaneity
angle: everything, everywhere, at once.

- **3 illustrated leads:** Kyiv hit by a seven-wave overnight barrage;
  Cyclone Akvan makes landfall in Odisha; COP31 ends in a finance
  deadlock — each with a large rich illustration and a red SO WHAT line.
- **Six-cell gold number strip:** 300,000+ evacuated in Odisha, ~30
  ballistic missiles fired at Kyiv, −6.22% Taiex close, 2.3% Japan October
  headline CPI, 118 Phillips vs India, 8 years BepiColombo to Mercury.
- **Region chips:** Europe 7 · Americas 8 · Asia-Pacific 10 · Mideast 3 ·
  Africa 3 · Oceania 4 · World/Space 1.
- **THE DAY BY HOURS:** 00:49 UTC New Caledonia quake → 01:25 Kyiv barrage
  → 02:00 UTC Akvan landfall → morning Asia markets plunge → midday COP31
  final day → P.M. Brussels reset summit → evening Las Vegas practice.
- **10 tiles (stories 4–13) in 5×2:** Asia's AI sell-off, Japan core
  inflation, China lending rates, EU–UK reset summit, Saudi interceptions,
  Hormuz shut, Bukele's third-term filing, Senegal boat capsize, Italy's
  CGIL strike, BepiColombo reaches Mercury — each with a small illustration
  strip and a red → consequence phrase.
- **THE WORLD IN ONE DAY map** with numbered red pins, plus **ALSO — 23
  more stories** in three columns.
- **DATE CHECK (red box):** the 19 November stories that are NOT today's
  list — including Anthropic's IPO debut and the ~$2tn figure, which were
  Thursday's news, not a Friday surge.

## How it runs

`main.ts` (Node 22, standard library only) copies the committed `entry.png`
to `/output/entry.png`. The image is drawn once, by hand, in `render.py`
(Pillow) and committed beside the program — the grader sees exactly the
committed bytes, byte-identical on every run.

## License

MIT — see [LICENSE](LICENSE).
