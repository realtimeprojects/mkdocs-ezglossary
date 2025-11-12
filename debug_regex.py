import re

# This is the exact pattern from the logs
pattern = r'<glossary::([^:<>"\|/\@&#][^:<>"\|/\@]*)\?\|?([\\\|\=\w\+\-]+)?>'
test_string = '<glossary::users|theme=detailed>'

print(f"Pattern: {pattern}")
print(f"Test string: {test_string}")

match = re.search(pattern, test_string)
if match:
    print(f'Full match: {match.group()!r}')
    print(f'Group count: {len(match.groups())}')
    for i, group in enumerate(match.groups(), 1):
        print(f'Group {i}: {group!r}')
else:
    print('No match')