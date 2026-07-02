# NHL Jersey Lookup

A simple CLI that finds current NHL players by jersey number using the [NHL Stats API](https://api.nhle.com/stats/rest) (`cayenneExp` filter).

## Requirements

- Python 3.13+
- [uv](https://docs.astral.sh/uv/)

## Installation

```bash
git clone https://github.com/jcasman/nhl-jersey-lookup.git
cd nhl-jersey-lookup
uv sync
```

## Run

```bash
uv run python main.py
```

Defaults to jersey **#27**. Because I'm a fan of John Tonelli #27 on the New York Islanders back in the early 80s during the dynasty days. Pass any number as an argument:

```bash
uv run python main.py 99
```

Example output:

```
NHL Jersey Lookup — searching for #27...

Found 20 player(s).

           Current NHL Players Wearing #27
┏━━━━━━━━━━━━━━━━━━━┳━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━┓
┃ Player            ┃ Team ┃ Position   ┃ Player ID ┃
┡━━━━━━━━━━━━━━━━━━━╇━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━┩
│ Shea Theodore     │ VGK  │ Defense    │ 8477447   │
│ Ryan McDonagh     │ TBL  │ Defense    │ 8474151   │
│ ...               │      │            │           │
└───────────────────┴──────┴────────────┴───────────┘
```

