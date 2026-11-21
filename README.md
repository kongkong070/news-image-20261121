# The World Today — Saturday 21 November 2026

[![make.fun](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/kongkong070/news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/kongkong070/news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

A one-page newspaper front page summing up the world's news of
**Saturday 21 November 2026**, drawn with Pillow and shipped as `entry.png`.
`main.ts` (Node 22, stdlib only) copies it to `/output/entry.png`.

## The day's stories

- **Lead — Russian missiles land in Poland.** Two Russian missiles and a drone
  crossed into Poland during Friday's huge strike on Ukraine; Prime Minister
  Donald Tusk called it a deliberate provocation as NATO jets scrambled.
  No one was hurt. It came days after the Trump–Xi–Putin peace declaration
  in Shenzhen.
- **Washington — Trump hails "very good" Putin talks.** Home from Shenzhen,
  the president also threatened a "tremendous tax" on US firms building
  AI data centres abroad.
- **Copenhagen — Denmark expels envoy in rapper "murder plot".** Police say
  two men were held over a plan to kill Ukrainian rapper Kyivstoner.
- **New York — Mamdani: Rikers Island jail to close by 2032.** The mayor's
  plan replaces the jail with four borough jails and cuts inmate numbers.
- **South Africa — ANC scrambles for coalition deals after election setback.**
  The ruling party won just 31% and lost most big cities; talks must end
  by 27 November.
- **Sport — Kane out for months with ankle ligament tear.** England's captain
  was hurt in Bayern Munich's draw with Cologne and will miss the rest
  of 2026.

See [SOURCES.md](SOURCES.md) for the source of each story.

## Reproduce

```sh
python3 draw.py            # regenerates entry.png (1024x1024, deterministic)
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```
