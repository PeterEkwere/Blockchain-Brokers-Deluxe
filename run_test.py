import itertools



words = ['exact', 'ticket', 'mystery', 'scissors', 'today', 'gift', 'december', 'broken', 'frown', 'walk', 'spare', 'ice']

permutations = list(itertools.permutations(words))

for p in permutations[:10]:
    print(p)