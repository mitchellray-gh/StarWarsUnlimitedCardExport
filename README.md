# Star Wars Unlimited Card Database

This project fetches and organizes all Star Wars Unlimited cards from the official SWU-DB API.

## Features

- Fetches all cards from all available sets (SOR, TWI, SHD, LOF, JTL, SEC)
- Saves data in multiple formats:
  - Complete JSON database (`swu_cards.json`)
  - CSV format (`swu_cards.csv`)
  - Individual set files in `by_set/` directory
- Generates statistics about the card collection

## Installation

1. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the script to build the database:
```bash
python fetch_cards.py
```

The script will:
1. Fetch all cards from the API (this may take 10-15 minutes)
2. Save the database in the `database/` directory
3. Display statistics about the collection

## Output Structure

```
database/
├── swu_cards.json          # Complete database (all cards)
├── swu_cards.csv           # CSV format
├── statistics.json         # Database statistics
└── by_set/                 # Individual set files
    ├── SOR.json
    ├── TWI.json
    ├── SHD.json
    ├── LOF.json
    ├── JTL.json
    └── SEC.json
```

## Card Metadata

Each card includes the following metadata (when available):
- Set and card number
- Name and subtitle
- Type (Leader, Unit, Base, Event, Upgrade)
- Arena (Ground, Space)
- Stats (Cost, Power, HP)
- Traits
- Rarity
- Artist
- Card text and abilities
- And more...

## API Information

This project uses the official SWU-DB API:
- Base URL: `https://api.swu-db.com/cards`
- Endpoint: `/cards/{set}/{number}?format=json`
- No authentication required

## Sets Included

- **SOR** - Spark of Rebellion (252 cards)
- **TWI** - Twilight of the Republic (257 cards)
- **SHD** - Shadows of the Galaxy (262 cards)
- **LOF** - Legends of the Force (264 cards)
- **JTL** - Jump To Lightspeed (262 cards)
- **SEC** - Secrets of Power (264 cards)

Total: 1,561 cards
