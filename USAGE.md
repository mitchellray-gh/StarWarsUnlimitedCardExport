# Star Wars Unlimited Card Database - User Guide

A comprehensive tool for fetching, organizing, and analyzing Star Wars Unlimited cards from the official SWU-DB API.

---

## 🚀 Quick Start

### 1. Installation

Clone the repository:
```bash
git clone https://github.com/mitchellray-gh/StarWarsUnlimitedCardExport.git
cd StarWarsUnlimitedCardExport
```

Install dependencies:
```bash
pip install -r requirements.txt
```

### 2. Fetch the Card Database

Run the main fetch script to download all cards:
```bash
python fetch_cards.py
```

**What happens:**
- ✅ Automatically discovers all available card sets from swu-db.com
- ✅ Fetches every card with full metadata (1,500+ cards)
- ✅ Saves data in multiple formats (JSON, CSV)
- ✅ Organizes cards by set
- ✅ Generates statistics

**Time:** Takes approximately 10-15 minutes depending on your connection.

### 3. Query the Database

After fetching, use the query tool to search cards:
```bash
python query_cards.py
```

This runs example queries showing how to:
- Get specific cards
- Search by name
- Filter by rarity, type, trait, cost
- Find legendary cards

---

## 📁 Project Structure

```
StarWarsUnlimitedCardExport/
├── fetch_cards.py              # Main script - fetches all cards
├── query_cards.py              # Query tool with examples
├── analyze_twin_suns.py        # Twin Suns format analyzer
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
├── USAGE.md                    # This file
└── database/                   # Generated database files
    ├── swu_cards.json          # Complete card database
    ├── swu_cards.csv           # CSV format
    ├── statistics.json         # Database stats
    └── by_set/                 # Individual set files
        ├── SOR.json
        ├── TWI.json
        ├── SHD.json
        └── ...
```

---

## 🎮 Features

### 1. Automatic Set Discovery

The tool now **automatically discovers new card sets** when they're released! No manual updates needed.

- Scans swu-db.com/sets for available sets
- Detects set codes and card counts
- Falls back to known sets if discovery fails

### 2. Twin Suns Deck Builder

Analyze the best leader combinations for Twin Suns multiplayer format:

```bash
python analyze_twin_suns.py
```

**Output:**
- Top Heroism (light side) leader pairs
- Top Villainy (dark side) leader pairs
- Aspect coverage analysis
- Best 3-aspect combinations

### 3. Query Database

Use `query_cards.py` as a template or library:

```python
from query_cards import SWUCardDatabase

db = SWUCardDatabase()

# Search by name
vader_cards = db.search_by_name("Darth Vader")

# Get a specific card
card = db.get_card("SOR", "10")

# Filter by type
all_leaders = db.get_leaders()
all_legendaries = db.get_legendaries()

# Filter by trait
jedi_cards = db.filter_by_trait("JEDI")

# Filter by cost
expensive = db.filter_by_cost(min_cost=8)

# Print card details
db.print_card(card)
```

---

## 📊 Database Information

### Card Metadata Included

Each card contains:
- **Identifiers:** Set, Number, Name, Subtitle
- **Card Type:** Leader, Unit, Base, Event, Upgrade
- **Game Stats:** Cost, Power, HP
- **Gameplay:** Aspects, Traits, Arenas, Keywords
- **Card Text:** Front text, back text, epic actions
- **Collectible Info:** Rarity, Artist, Variant Type
- **Market Data:** Current price, low price
- **Images:** Front art URL, back art URL

### Available Sets (Auto-Updated)

The tool automatically detects all sets. As of creation:
- **SOR** - Spark of Rebellion (252 cards)
- **TWI** - Twilight of the Republic (257 cards)
- **SHD** - Shadows of the Galaxy (262 cards)
- **LOF** - Legends of the Force (264 cards)
- **JTL** - Jump To Lightspeed (262 cards)
- **SEC** - Secrets of Power (264 cards)

**New sets are automatically detected when you run `fetch_cards.py`!**

---

## 🔧 Advanced Usage

### Update Existing Database

To refresh your database with new cards or sets:

```bash
python fetch_cards.py
```

The script will:
1. Discover any new sets that have been released
2. Fetch all cards (including new ones)
3. Overwrite existing database files

### Export Formats

The tool saves data in multiple formats:

**JSON** (Complete metadata)
- `database/swu_cards.json` - All cards
- `database/by_set/[SET].json` - Individual sets

**CSV** (Spreadsheet compatible)
- `database/swu_cards.csv` - Importable to Excel, Google Sheets

**Statistics** (Summary)
- `database/statistics.json` - Cards by set, type, rarity

### Custom Queries

Modify `query_cards.py` or create your own scripts:

```python
from query_cards import SWUCardDatabase

db = SWUCardDatabase()

# Example: Find all 3-cost Jedi units
jedi = db.filter_by_trait("JEDI")
units = [c for c in jedi if c.get('Type') == 'Unit']
three_cost = [c for c in units if c.get('Cost') == '3']

for card in three_cost:
    print(f"{card['Name']} - {card['Subtitle']}")
```

---

## 🎯 Twin Suns Format

### What is Twin Suns?

Twin Suns is a multiplayer format for Star Wars Unlimited with special rules:
- **2 leaders** (must share Heroism or Villainy aspect)
- **Singleton format** (only 1 copy of each card)
- **50 card minimum** (80 after 4th set)
- **3-4 players**

### Using the Analyzer

```bash
python analyze_twin_suns.py
```

The analyzer shows:
1. **All valid leader combinations** sorted by aspect coverage
2. **Top Heroism combinations** (light side decks)
3. **Top Villainy combinations** (dark side decks)
4. **Best 3-aspect pairings** for maximum card pool access

### Best Combinations

**Heroism (Light Side):**
- Luke Skywalker + Ahsoka Tano (Aggression + Heroism + Vigilance)
- Luke Skywalker + The Mandalorian (Cunning + Heroism + Vigilance)

**Villainy (Dark Side):**
- Darth Vader + Moff Gideon (Aggression + Command + Villainy)
- Darth Vader + General Grievous (Aggression + Cunning + Villainy)

---

## 🛠️ Troubleshooting

### "Failed to fetch" errors

Some cards may fail due to temporary API issues. The script will:
- Continue fetching other cards
- Report failures at the end
- Save all successfully fetched cards

**Solution:** Run the script again to retry failed cards.

### Slow performance

The script includes a 0.1s delay between requests to be respectful to the API.

**Expected time:** ~10-15 minutes for full database

### Import errors

Ensure all dependencies are installed:
```bash
pip install -r requirements.txt
```

### Empty database

Make sure you have internet connection and the API is accessible:
- Test: Visit https://www.swu-db.com/
- If site is down, try again later

---

## 📝 API Information

This tool uses the official SWU-DB API:
- **Base URL:** `https://api.swu-db.com/cards`
- **Format:** `/cards/{set}/{number}?format=json`
- **No authentication required**
- **Free to use**

Please be respectful to the API:
- The tool includes rate limiting
- Don't run multiple instances simultaneously
- Cache results instead of repeated fetching

---

## 🤝 Contributing

Found a bug or want to add a feature?

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

## 📜 License

This project uses data from the official SWU-DB API. All Star Wars Unlimited card data and images are property of Fantasy Flight Games and Lucasfilm.

This tool is for personal, non-commercial use only.

---

## 🔗 Links

- **GitHub Repository:** https://github.com/mitchellray-gh/StarWarsUnlimitedCardExport
- **SWU-DB Website:** https://www.swu-db.com/
- **SWU-DB API Docs:** https://www.swu-db.com/api

---

## 📧 Support

For questions or issues:
- Open an issue on GitHub
- Check existing issues for solutions
- Review this guide for common problems

---

**Last Updated:** January 30, 2026
**Database Version:** Auto-updating
**Total Cards:** 1,500+ (updates automatically)
