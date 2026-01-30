import requests
import json
import time
from pathlib import Path

# Define all card sets with their card counts
CARD_SETS = {
    'SOR': 252,  # Spark of Rebellion
    'TWI': 257,  # Twilight of the Republic
    'SHD': 262,  # Shadows of the Galaxy
    'LOF': 264,  # Legends of the Force
    'JTL': 262,  # Jump To Lightspeed
    'SEC': 264,  # Secrets of Power
}

API_BASE_URL = "https://api.swu-db.com/cards"

def fetch_card(set_code, card_number):
    """Fetch a single card from the API."""
    url = f"{API_BASE_URL}/{set_code.lower()}/{card_number}?format=json"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to fetch {set_code}/{card_number}: Status {response.status_code}")
            return None
    except Exception as e:
        print(f"Error fetching {set_code}/{card_number}: {e}")
        return None

def build_database():
    """Build the complete card database."""
    all_cards = []
    total_cards = sum(CARD_SETS.values())
    current_card = 0
    
    print(f"Starting to fetch {total_cards} cards from {len(CARD_SETS)} sets...")
    
    for set_code, card_count in CARD_SETS.items():
        print(f"\nFetching {set_code} set ({card_count} cards)...")
        
        for card_num in range(1, card_count + 1):
            current_card += 1
            card_data = fetch_card(set_code, card_num)
            
            if card_data:
                all_cards.append(card_data)
                if current_card % 50 == 0:
                    print(f"Progress: {current_card}/{total_cards} cards fetched ({current_card/total_cards*100:.1f}%)")
            
            # Be respectful to the API - small delay between requests
            time.sleep(0.1)
    
    print(f"\nCompleted! Successfully fetched {len(all_cards)}/{total_cards} cards.")
    return all_cards

def save_database(cards, output_dir="database"):
    """Save the database in multiple formats."""
    Path(output_dir).mkdir(exist_ok=True)
    
    # Save as JSON
    json_path = Path(output_dir) / "swu_cards.json"
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(cards, f, indent=2, ensure_ascii=False)
    print(f"Saved JSON database: {json_path} ({json_path.stat().st_size / 1024:.1f} KB)")
    
    # Save as CSV
    if cards:
        import csv
        csv_path = Path(output_dir) / "swu_cards.csv"
        
        # Get all unique keys from all cards
        all_keys = set()
        for card in cards:
            all_keys.update(card.keys())
        
        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=sorted(all_keys))
            writer.writeheader()
            for card in cards:
                # Flatten lists/dicts to strings for CSV
                row = {}
                for key, value in card.items():
                    if isinstance(value, (list, dict)):
                        row[key] = json.dumps(value)
                    else:
                        row[key] = value
                writer.writerow(row)
        print(f"Saved CSV database: {csv_path} ({csv_path.stat().st_size / 1024:.1f} KB)")
    
    # Save organized by set
    by_set_dir = Path(output_dir) / "by_set"
    by_set_dir.mkdir(exist_ok=True)
    
    cards_by_set = {}
    for card in cards:
        set_code = card.get('Set', 'UNKNOWN')
        if set_code not in cards_by_set:
            cards_by_set[set_code] = []
        cards_by_set[set_code].append(card)
    
    for set_code, set_cards in cards_by_set.items():
        set_path = by_set_dir / f"{set_code}.json"
        with open(set_path, 'w', encoding='utf-8') as f:
            json.dump(set_cards, f, indent=2, ensure_ascii=False)
        print(f"Saved {set_code}: {len(set_cards)} cards")

def create_summary_stats(cards):
    """Generate summary statistics about the database."""
    stats = {
        'total_cards': len(cards),
        'by_set': {},
        'by_type': {},
        'by_rarity': {},
        'by_aspect': {},
        'by_arena': {},
    }
    
    for card in cards:
        # Count by set
        set_code = card.get('Set', 'UNKNOWN')
        stats['by_set'][set_code] = stats['by_set'].get(set_code, 0) + 1
        
        # Count by type
        card_type = card.get('Type', 'UNKNOWN')
        stats['by_type'][card_type] = stats['by_type'].get(card_type, 0) + 1
        
        # Count by rarity
        rarity = card.get('Rarity', 'UNKNOWN')
        stats['by_rarity'][rarity] = stats['by_rarity'].get(rarity, 0) + 1
        
        # Count by arena
        arena = card.get('Arena', 'N/A')
        if arena:
            stats['by_arena'][arena] = stats['by_arena'].get(arena, 0) + 1
    
    return stats

if __name__ == "__main__":
    print("=" * 60)
    print("Star Wars Unlimited Card Database Builder")
    print("=" * 60)
    
    # Build the database
    cards = build_database()
    
    if cards:
        # Save the database
        print("\n" + "=" * 60)
        print("Saving database...")
        print("=" * 60)
        save_database(cards)
        
        # Generate and save statistics
        print("\n" + "=" * 60)
        print("Database Statistics")
        print("=" * 60)
        stats = create_summary_stats(cards)
        
        print(f"\nTotal Cards: {stats['total_cards']}")
        
        print("\nCards by Set:")
        for set_code, count in sorted(stats['by_set'].items()):
            print(f"  {set_code}: {count}")
        
        print("\nCards by Type:")
        for card_type, count in sorted(stats['by_type'].items()):
            print(f"  {card_type}: {count}")
        
        print("\nCards by Rarity:")
        for rarity, count in sorted(stats['by_rarity'].items()):
            print(f"  {rarity}: {count}")
        
        print("\nCards by Arena:")
        for arena, count in sorted(stats['by_arena'].items()):
            print(f"  {arena}: {count}")
        
        # Save stats
        stats_path = Path("database") / "statistics.json"
        with open(stats_path, 'w', encoding='utf-8') as f:
            json.dump(stats, f, indent=2)
        print(f"\nStatistics saved to: {stats_path}")
    else:
        print("\nNo cards were fetched. Please check your internet connection and try again.")
    
    print("\n" + "=" * 60)
    print("Complete!")
    print("=" * 60)
