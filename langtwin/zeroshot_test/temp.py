a = 'above bowl position'
b = 'bowl_01'

# Replace underscores with spaces and split into words
set_a = set(a.replace('_', ' ').split())
set_b = set(b.replace('_', ' ').split())

# Find common elements
common_elements = set_a.intersection(set_b)

print(common_elements)
