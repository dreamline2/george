from models import Food, FoodDailyInfo
from google.appengine.ext import ndb, db

def process_item(item):
#    print item
    food = Food.get_or_insert(item['name'])
    for key, value in item.items():
        try:
            if key != 'date':
                setattr(food, key, value)
        except Exception as e:
            print e

    food.push_info(item['date'])
    food.aggregate()
    food.get_point()
    food.get_recommand()
    return food


def download(date):
    from works import pork, checken, fish, vegetable
    
    results = []
    for item in vegetable.get(date):
        results.append(process_item(item))

    for item in fish.get(date):
        results.append(process_item(item))

    for item in checken.get(date):
        results.append(process_item(item))

    for item in pork.get(date):
        results.append(process_item(item))
    
    ndb.put_multi(results)
    print results


