
# -*- coding: utf-8 -*-
from models import Food, FoodDailyInfo
from google.appengine.ext import ndb, db

def process_item(item):
#    print item

    food = Food.get_or_insert(item['name'])
    for key, value in item.items():
        try:
            if key != 'date':
                setattr(food, key, value)
                print key, value
        except Exception as e:
            print e

    food.push_info(item['date'])
    food.aggregate()
    food.get_point()
    food.get_recommand()
    return food


def download(date):
    print 'start'
    from works import pork, checken, fish, vegetable
    
    results = []
    for item in vegetable.get(date):
        results.append(process_item(item))

    print len(results)
    for item in fish.get(date):
        results.append(process_item(item))

    print len(results)
    for item in checken.get(date):
        if u'其他' in item['name']:
            continue
        if u'待訂' in item['name']:
            continue
        results.append(process_item(item))

    print len(results)
    for item in pork.get(date):
        results.append(process_item(item))
    
    ndb.put_multi(results)
    print len(results)


from datetime import datetime, timedelta, date

def run():
    time = date(2014,6,1)
    today = datetime.now().date()
    while time <= today:
        print time
        download(time)
        time += timedelta(1)


def sort():
    vegetables = Food.query(Food.type=="vegetable").order(Food.point).fetch(1000)
    meats = Food.query(Food.type=="meat").order(Food.point).fetch(1000)
    fishs = Food.query(Food.type=="fish").order(Food.point).fetch(1000)

    c = 0
    for vegetable in vegetables:
        print 'vegetable', c, vegetable.name
        vegetable.rank = c
        if c:
            vegetable.prev = vegetables[c-1].name
        if c < len(vegetables) - 1:
            vegetable.next_one = vegetables[c+1].name
        c += 1

    c=0
    for meat in meats:
        print 'meat', c, meat.name
        meat.rank = c
        if c:
            meat.prev = meats[c-1].name
        if c < len(meats) - 1:
            meat.next = meats[c+1].name
        c += 1


    c=0
    for fish in fishs:
        print 'fish', c, fish.name
        fish.rank = c
        if c:
            fish.prev = fishs[c-1].name
        if c < len(fishs) - 1:
            fish.next = fishs[c+1].name
        c += 1

    result = []
    result.extend(vegetables)
    result.extend(fishs)
    result.extend(meats)
    ndb.put_multi(result)

