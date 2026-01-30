import json
from pathlib import Path
from typing import List, Dict, Any, Optional

class SWUCardDatabase:
    """Query interface for the Star Wars Unlimited card database."""
    
    def __init__(self, db_path="database/swu_cards.json"):
        """Load the card database."""
        self.db_path = Path(db_path)
        with open(self.db_path, 'r', encoding='utf-8') as f:
            self.cards = json.load(f)
        print(f"Loaded {len(self.cards)} cards from database")
    
    def get_card(self, set_code: str, number: str) -> Optional[Dict[str, Any]]:
        """Get a specific card by set and number."""
        for card in self.cards:
            if card.get('Set') == set_code.upper() and card.get('Number') == str(number).zfill(3):
                return card
        return None
    
    def search_by_name(self, name: str) -> List[Dict[str, Any]]:
        """Search for cards by name (case-insensitive, partial match)."""
        name_lower = name.lower()
        return [card for card in self.cards 
                if name_lower in card.get('Name', '').lower() 
                or name_lower in card.get('Subtitle', '').lower()]
    
    def filter_by_set(self, set_code: str) -> List[Dict[str, Any]]:
        """Get all cards from a specific set."""
        return [card for card in self.cards if card.get('Set') == set_code.upper()]
    
    def filter_by_type(self, card_type: str) -> List[Dict[str, Any]]:
        """Filter cards by type (Leader, Unit, Base, Event, Upgrade)."""
        return [card for card in self.cards if card.get('Type') == card_type]
    
    def filter_by_rarity(self, rarity: str) -> List[Dict[str, Any]]:
        """Filter cards by rarity."""
        return [card for card in self.cards if card.get('Rarity') == rarity]
    
    def filter_by_trait(self, trait: str) -> List[Dict[str, Any]]:
        """Find cards with a specific trait."""
        trait_upper = trait.upper()
        return [card for card in self.cards 
                if trait_upper in [t.upper() for t in card.get('Traits', [])]]
    
    def filter_by_aspect(self, aspect: str) -> List[Dict[str, Any]]:
        """Find cards with a specific aspect."""
        return [card for card in self.cards 
                if aspect in card.get('Aspects', [])]
    
    def filter_by_cost(self, min_cost: int = 0, max_cost: int = 99) -> List[Dict[str, Any]]:
        """Filter cards by cost range."""
        results = []
        for card in self.cards:
            try:
                cost = int(card.get('Cost', 0))
                if min_cost <= cost <= max_cost:
                    results.append(card)
            except (ValueError, TypeError):
                pass
        return results
    
    def get_legendaries(self) -> List[Dict[str, Any]]:
        """Get all legendary cards."""
        return self.filter_by_rarity('Legendary')
    
    def get_leaders(self) -> List[Dict[str, Any]]:
        """Get all leader cards."""
        return self.filter_by_type('Leader')
    
    def print_card(self, card: Dict[str, Any]) -> None:
        """Pretty print a card's details."""
        print("=" * 60)
        print(f"{card.get('Name', 'Unknown')} - {card.get('Subtitle', '')}")
        print("=" * 60)
        print(f"Set: {card.get('Set')} #{card.get('Number')}")
        print(f"Type: {card.get('Type')}")
        
        if card.get('Aspects'):
            print(f"Aspects: {', '.join(card.get('Aspects', []))}")
        
        if card.get('Traits'):
            print(f"Traits: {', '.join(card.get('Traits', []))}")
        
        if card.get('Arenas'):
            print(f"Arena: {', '.join(card.get('Arenas', []))}")
        
        if card.get('Cost'):
            stats = f"Cost: {card.get('Cost')}"
            if card.get('Power'):
                stats += f" | Power: {card.get('Power')}"
            if card.get('HP'):
                stats += f" | HP: {card.get('HP')}"
            print(stats)
        
        print(f"Rarity: {card.get('Rarity')}")
        
        if card.get('FrontText'):
            print(f"\nText: {card.get('FrontText')}")
        
        if card.get('EpicAction'):
            print(f"\nEpic Action: {card.get('EpicAction')}")
        
        if card.get('BackText') and card.get('DoubleSided'):
            print(f"\nBack Text: {card.get('BackText')}")
        
        if card.get('Keywords'):
            print(f"\nKeywords: {', '.join(card.get('Keywords', []))}")
        
        print(f"\nArtist: {card.get('Artist')}")
        print(f"Market Price: ${card.get('MarketPrice', 'N/A')}")
        print("=" * 60)


def main():
    """Example usage of the card database."""
    db = SWUCardDatabase()
    
    print("\n### Example 1: Get a specific card ###")
    card = db.get_card("SOR", "10")
    if card:
        db.print_card(card)
    
    print("\n### Example 2: Search by name ###")
    results = db.search_by_name("Darth Vader")
    print(f"\nFound {len(results)} cards matching 'Darth Vader':")
    for card in results:
        print(f"  - {card.get('Name')} ({card.get('Set')} #{card.get('Number')})")
    
    print("\n### Example 3: Get all legendary cards ###")
    legendaries = db.get_legendaries()
    print(f"\nFound {len(legendaries)} legendary cards")
    print("First 5 legendaries:")
    for card in legendaries[:5]:
        print(f"  - {card.get('Name')} ({card.get('Set')} #{card.get('Number')})")
    
    print("\n### Example 4: Find cards by trait ###")
    jedi_cards = db.filter_by_trait("JEDI")
    print(f"\nFound {len(jedi_cards)} JEDI cards")
    
    print("\n### Example 5: Filter by cost ###")
    expensive_cards = db.filter_by_cost(min_cost=8)
    print(f"\nFound {len(expensive_cards)} cards with cost 8 or more")
    print("First 5:")
    for card in expensive_cards[:5]:
        print(f"  - {card.get('Name')} (Cost: {card.get('Cost')}) - {card.get('Set')} #{card.get('Number')}")


if __name__ == "__main__":
    main()
