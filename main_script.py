import scrape_crowdcube as sc

from pymongo import MongoClient
import urllib2
import json

client = MongoClient()

db = client.crowdcube

def store_in_db():
    '''
    Extract information from crowdcube and store it in MongoDB
    '''
    invs = sc.extract()
    if len(invs) == 0:
        return []
    results = db.live_investements.insert_many([x.__dict__ for x in invs])
    return results

def analyze_investements():
    cursor = db.live_investements.find()
    total_amount_raised = 0
    count = 0
    for c in cursor:
        if c['days_remaining'] > 10:
            count += 1
            total_amount_raised +=  c['amount_raised']
    return count, total_amount_raised

def analyze_investements_mongo():
    cursor = db.live_investements.aggregate(
        [
            {"$match": {"days_remaining": {"$gt": 10}}},
            {"$group": {"_id": "null", "total": {"$sum": "$amount_raised"}, "count": {"$sum": 1}}}
        ]
    )
    result = list(cursor)
    return result[0]['count'], result[0]['total']


def analyze_investements_mongo_sql():
    key = None
    condition = { 'days_remaining' : {'$gt':10}}
    initial = { 'count':0, 'sum':0}
    reduce = 'function(doc, out) {out.count++, out.sum+=doc.amount_raised}'
    result = db.live_investements.group(key, condition, initial, reduce)[0] 
    return result['count'], result['sum']

def dump_kickstarter():
    '''
    Use kickstarter internal API to extract information about 100 projects in 
    category_id =1 (ART) and store them in Mongo
    '''
    base_url = 'https://www.kickstarter.com/discover/advanced?google_chrome_workaround&category_id=1&woe_id=0&sort=magic&seed=2457444'
    hdr = {'X-Requested-With': 'XMLHttpRequest',
            'Accept': 'application/json, text/javascript, */*; q=0.01'}
    #since the api only gives 20 at a time.
    total_rows = 0
    for i in range(5):
        url = base_url + '&page=' + str(i+1)
        req = urllib2.Request(url, headers = hdr)
        response = urllib2.urlopen(req)
        if response.getcode() != 200:
            print ' Houston, we have a problem!!'
            return 0
        json_content = json.loads(response.read())
        results = db.kickstarter.insert_many([x for x in json_content['projects']])
        total_rows += len(results.inserted_ids)
        print 'Inserted ' + str(len(results.inserted_ids)) + ' rows. Total inserted till now ' + str(total_rows) 
        if json_content['has_more'] != True:
            break    
    print 'Total rows in kickstarter collection: ' + str(db.kickstarter.count()) 

if __name__ == "__main__":
    print 'The number of records in live_investements before scraping:' + str(db.live_investements.count())
    results = store_in_db()
    print 'Feteched ' + str( len(results.inserted_ids)) + ' from scraping'
    print 'The number of records in live_investements after scraping:' + str(db.live_investements.count())
    count_p, total_amount_raised_p = analyze_investements()
    count_m, total_amount_raised_m = analyze_investements_mongo()
    print 'The number of investements with days_left greater than 10: ' + str(count_p) + ' ,Amount raised: ' + str(total_amount_raised_p) + ' using python'
    print 'The number of investements with days_left greater than 10: ' + str(count_m) + ' ,Amount raised: ' + str(total_amount_raised_m) + ' using Mongo'
    print '######'
    print 'Extracting kickstarter data'
    dump_kickstarter()
