import csv
import json
from collections import defaultdict

# Load the CSV
print("Loading card database...")
with open('database/swu_cards.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    cards = list(reader)

# Filter for leaders only
leaders = [c for c in cards if c.get('Type') == 'Leader']

print(f'\n{"="*80}')
print(f'TWIN SUNS LEADER ANALYSIS')
print(f'{"="*80}')
print(f'Total Leaders Found: {len(leaders)}\n')

# Parse aspects and organize leaders
heroism_leaders = []
villainy_leaders = []
aspect_combinations = defaultdict(list)

for leader in leaders:
    aspects_str = leader.get('Aspects', '[]')
    try:
        aspects = json.loads(aspects_str) if aspects_str else []
    except:
        aspects = []
    
    name = leader.get('Name', 'Unknown')
    subtitle = leader.get('Subtitle', '')
    set_code = leader.get('Set', '')
    number = leader.get('Number', '')
    rarity = leader.get('Rarity', '')
    cost = leader.get('Cost', 'N/A')
    power = leader.get('Power', 'N/A')
    hp = leader.get('HP', 'N/A')
    
    # Check for Heroism (white) or Villainy (black)
    has_heroism = 'Heroism' in aspects
    has_villainy = 'Villainy' in aspects
    
    leader_info = {
        'name': name,
        'subtitle': subtitle,
        'full_name': f'{name} - {subtitle}' if subtitle else name,
        'set': set_code,
        'number': number,
        'aspects': aspects,
        'rarity': rarity,
        'cost': cost,
        'power': power,
        'hp': hp,
        'heroism': has_heroism,
        'villainy': has_villainy
    }
    
    if has_heroism:
        heroism_leaders.append(leader_info)
    if has_villainy:
        villainy_leaders.append(leader_info)
    
    # Track aspect combinations
    aspect_key = tuple(sorted(aspects))
    aspect_combinations[aspect_key].append(leader_info)

print(f'Heroism Leaders: {len(heroism_leaders)}')
print(f'Villainy Leaders: {len(villainy_leaders)}')
print(f'\n{"="*80}')

# Analyze aspect coverage
print("\nASPECT COMBINATIONS AVAILABLE:")
print("-" * 80)
for aspects, leader_list in sorted(aspect_combinations.items()):
    if aspects:  # Skip empty aspect sets
        print(f"{' + '.join(aspects)}: {len(leader_list)} leaders")

print(f'\n{"="*80}')
print("TOP HEROISM LEADER COMBINATIONS FOR TWIN SUNS")
print(f'{"="*80}')

# Find best Heroism combinations (max aspect coverage)
heroism_combos = []
for i, leader1 in enumerate(heroism_leaders):
    for leader2 in heroism_leaders[i+1:]:
        # Combine aspects from both leaders
        combined_aspects = set(leader1['aspects'] + leader2['aspects'])
        
        # Calculate synergy score
        aspect_count = len(combined_aspects)
        rarity_score = 0
        if leader1['rarity'] == 'Special': rarity_score += 2
        if leader2['rarity'] == 'Special': rarity_score += 2
        if leader1['rarity'] == 'Legendary': rarity_score += 1
        if leader2['rarity'] == 'Legendary': rarity_score += 1
        
        combo = {
            'leader1': leader1,
            'leader2': leader2,
            'aspects': sorted(combined_aspects),
            'aspect_count': aspect_count,
            'rarity_score': rarity_score,
            'score': aspect_count * 10 + rarity_score
        }
        heroism_combos.append(combo)

# Sort by aspect coverage first, then rarity
heroism_combos.sort(key=lambda x: (x['aspect_count'], x['rarity_score']), reverse=True)

# Display top 15 Heroism combinations
print("\nTop 15 Heroism Combinations (by aspect coverage):\n")
for idx, combo in enumerate(heroism_combos[:15], 1):
    l1 = combo['leader1']
    l2 = combo['leader2']
    print(f"{idx}. {l1['full_name']} ({l1['set']}) + {l2['full_name']} ({l2['set']})")
    print(f"   Aspects: {' + '.join(combo['aspects'])} ({combo['aspect_count']} total)")
    print(f"   Stats: L1: {l1['cost']}/{l1['power']}/{l1['hp']} | L2: {l2['cost']}/{l2['power']}/{l2['hp']}")
    print(f"   Rarity: {l1['rarity']} + {l2['rarity']}")
    print()

print(f'{"="*80}')
print("TOP VILLAINY LEADER COMBINATIONS FOR TWIN SUNS")
print(f'{"="*80}')

# Find best Villainy combinations
villainy_combos = []
for i, leader1 in enumerate(villainy_leaders):
    for leader2 in villainy_leaders[i+1:]:
        # Combine aspects from both leaders
        combined_aspects = set(leader1['aspects'] + leader2['aspects'])
        
        # Calculate synergy score
        aspect_count = len(combined_aspects)
        rarity_score = 0
        if leader1['rarity'] == 'Special': rarity_score += 2
        if leader2['rarity'] == 'Special': rarity_score += 2
        if leader1['rarity'] == 'Legendary': rarity_score += 1
        if leader2['rarity'] == 'Legendary': rarity_score += 1
        
        combo = {
            'leader1': leader1,
            'leader2': leader2,
            'aspects': sorted(combined_aspects),
            'aspect_count': aspect_count,
            'rarity_score': rarity_score,
            'score': aspect_count * 10 + rarity_score
        }
        villainy_combos.append(combo)

# Sort by aspect coverage first, then rarity
villainy_combos.sort(key=lambda x: (x['aspect_count'], x['rarity_score']), reverse=True)

# Display top 15 Villainy combinations
print("\nTop 15 Villainy Combinations (by aspect coverage):\n")
for idx, combo in enumerate(villainy_combos[:15], 1):
    l1 = combo['leader1']
    l2 = combo['leader2']
    print(f"{idx}. {l1['full_name']} ({l1['set']}) + {l2['full_name']} ({l2['set']})")
    print(f"   Aspects: {' + '.join(combo['aspects'])} ({combo['aspect_count']} total)")
    print(f"   Stats: L1: {l1['cost']}/{l1['power']}/{l1['hp']} | L2: {l2['cost']}/{l2['power']}/{l2['hp']}")
    print(f"   Rarity: {l1['rarity']} + {l2['rarity']}")
    print()

print(f'{"="*80}')
print("RECOMMENDED TWIN SUNS DECKS")
print(f'{"="*80}')

# Recommend specific strong combinations
print("\n🌟 BEST 3-ASPECT HEROISM COMBOS:")
heroism_3aspect = [c for c in heroism_combos if c['aspect_count'] == 3]
for idx, combo in enumerate(heroism_3aspect[:5], 1):
    l1 = combo['leader1']
    l2 = combo['leader2']
    print(f"\n{idx}. {l1['full_name']} + {l2['full_name']}")
    print(f"   Aspects: {' + '.join(combo['aspects'])}")
    print(f"   Sets: {l1['set']}, {l2['set']}")

print("\n\n🌟 BEST 3-ASPECT VILLAINY COMBOS:")
villainy_3aspect = [c for c in villainy_combos if c['aspect_count'] == 3]
for idx, combo in enumerate(villainy_3aspect[:5], 1):
    l1 = combo['leader1']
    l2 = combo['leader2']
    print(f"\n{idx}. {l1['full_name']} + {l2['full_name']}")
    print(f"   Aspects: {' + '.join(combo['aspects'])}")
    print(f"   Sets: {l1['set']}, {l2['set']}")

print(f'\n{"="*80}')
print("Analysis complete!")
print(f'{"="*80}')
