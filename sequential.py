import requests

# dictionary with user -> score
table = {}

def increase(author):
    if author in table:
        table[author] += 1
    else:
        table[author] = 1

# get data
topUrl = 'https://hacker-news.firebaseio.com/v0/topstories.json'
items = requests.get(url=topUrl).json()[:1]

index = 0
while index < len(items):
    itemId = items[index]
    itemUrl = 'https://hacker-news.firebaseio.com/v0/item/' + str(itemId) + '.json'
    item = requests.get(url=itemUrl).json()

    # original author
    try:
        author = item.get('by', None)
        if author != None:
            increase(author)
    except:
        print('Error with: ' + str(id))

    # analyse each comment
    try:
        kidIds = item.get('kids', [])
        items.extend(kidIds)
    except:
        print('Error with: ' + str(id))

leaderboard = sorted(table.items(), key=lambda item: item[1], reverse=True)
for author, score in leaderboard:
    print(author + ' : ' + str(score))

print(sum(map(lambda item: item[1], leaderboard)))
