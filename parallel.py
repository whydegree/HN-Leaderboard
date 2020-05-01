# I work with multiple threads because the requests to the API are slow
# This means that I have a queue of tasks that need to be done,
# and I need to make sure my dictionary is thread-safe

import requests
import threading
import queue
import time

def worker():
    while True:
        id = items.get()
        author, kids = getAuthorAndKids(id)

        if author != None:
            increase(author)
            add(kids)

        items.task_done()

def getAuthorAndKids(id):
    url = 'https://hacker-news.firebaseio.com/v0/item/' + str(id) + '.json'
    item = requests.get(url=url).json()

    try:
        author = item.get('by', None)
        kids = item.get('kids', [])
        return author, kids
    except:
        print('Error with: ' + str(id))
        return None, []

def increase(author):
    with lock:
        if author in table:
            table[author] += 1
        else:
            table[author] = 1

def add(kids):
    for kid in kids:
        items.put(kid)

def main():
    # used for measuring performance
    start = time.time()
    
    concurrent = 100
    for i in range(concurrent):
        threading.Thread(target=worker, daemon=True).start()
        
    topUrl = 'https://hacker-news.firebaseio.com/v0/topstories.json'
    ids = requests.get(url=topUrl).json()[:30]
    add(ids)

    # Wait for work to be done
    items.join()
    end = time.time()

    leaderboard = sorted(table.items(), key=lambda item: item[1], reverse=True)
    
    for (author, score) in leaderboard:
        if score >= 5:
            print(author + ' : ' + str(score))
    print('Total number: ' + str(sum(map(lambda item: item[1], leaderboard))))

    print('Total time: ' + str(end - start))
    
# dictionary with user -> score
table = {}
lock = threading.Lock()
items = queue.Queue()

if __name__ == '__main__':
    main()
