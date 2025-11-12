import re

# Test the current pattern
pattern = r'<glossary::([^:<>"\|/\@&#][^:<>"\|/\@]*)(;([\\\;\=\w\+\-]+))?>'

test_cases = [
    '<glossary::users>',
    '<glossary::users;theme=detailed>',
    '<glossary::role_perms;theme=detailed>',
    '<glossary::simulated-internet>'
]

for test in test_cases:
    match = re.search(pattern, test)
    if match:
        print(f"✓ {test}")
        print(f"  Groups: {match.groups()}")
        print(f"  Group 1 (section): {match.group(1)!r}")
        print(f"  Group 2 (;options): {match.group(2)!r}")
        if len(match.groups()) > 2:
            print(f"  Group 3 (options): {match.group(3)!r}")
        print()
    else:
        print(f"✗ {test} - NO MATCH")
        print()