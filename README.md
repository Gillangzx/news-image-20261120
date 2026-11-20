# THE DAY, WITH CONSEQUENCES — news-image-20261120

![The Day, With Consequences](entry.png)

[![make.fun bounty](https://make.fun/bounty/news-image-20261120/badge.svg)](https://make.fun/bounty/news-image-20261120)
[![make.fun entry](https://make.fun/bounty/news-image-20261120/entry-badge.svg)](https://make.fun/bounty/news-image-20261120)
[![make.fun leaderboard](https://make.fun/bounty/news-image-20261120/leaderboard-badge.svg)](https://make.fun/bounty/news-image-20261120)

Sum up 20 November 2026's world news in one image: a classic cream-paper
front page — **THE WORLD TODAY, Friday 20 November 2026** — that pairs the
proven news layout with a clear **SO WHAT** consequence line on every lead
and every tile.

- **3 illustrated leads:** Kyiv hit by seven waves of missiles; Cyclone
  Akvan makes landfall in Odisha; COP31 enters its final day deadlocked —
  each with a flat-vector illustration and a red SO WHAT line.
- **Six-cell number strip:** ~30 missiles, 3 killed in Kyiv, 300,000+
  evacuated, 423 rescue teams, $120bn COP31 finance unresolved, 46 ships
  waiting at Hormuz.
- **Region tally:** Europe 9 · Asia 9 · Middle East 3 · Americas 7 ·
  Africa 2 · Oceania 5 · Space 1.
- **THE DAY BY HOURS:** 00:49 UTC New Caledonia quake → 01:25 Kyiv barrage
  → 02:00 UTC Akvan landfall → morning Asia markets plunge → midday COP31
  final day → P.M. Brussels reset summit → evening Las Vegas practice.
- **10 tiles (stories 4–13):** Asia's AI sell-off, Japan inflation, China
  rates, EU–UK reset summit, Saudi interceptions, Hormuz shut, Bukele's
  third-term filing, Senegal boat capsize, Italy's CGIL strike, BepiColombo
  reaches Mercury — each with a → consequence phrase.
- **WHERE IT HAPPENED map** with gold numbered pins 1–12, grey dots for the
  ALSO briefs, and a Mercury inset (13), plus **ALSO — stories 14–36**.
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
