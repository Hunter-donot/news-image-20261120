[![make.fun](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/Hunter-donot/news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard)
[![reward](https://make.fun/badge/news-image-20261120/Hunter-donot/news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120)

# THE WORLD — 20 November 2026

A one-page newspaper front page summing up Friday 20 November 2026's
world news: Russia smashing Kyiv's bridges, Asia's AI rout (Nikkei -5%,
Taiex -6%), Cyclone Akvan making landfall in India, plus 9 more stories
and 24 briefs from across the world.

`render_20nov.py` draws the page with PIL and real TTF fonts
(Noto Serif Display Black masthead, Noto Serif headlines/body,
DejaVu Sans kickers) and writes `entry.png` (1024x1024).
`main.py` copies it to `/output/entry.png`.

Run: `python3 render_20nov.py` once, then `python3 main.py`.
