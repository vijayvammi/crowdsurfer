import scrape_crowdcube as sc

from pymongo import MongoClient
import urllib2
import json

client = MongoClient()

db = client.crowdcube

def store_in_db():
    invs = sc.extract()
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

#need to read more about mongo aggregration using python
def analyze_investements_mongo():
    key = None
    condition = { 'days_remaining' : {'$gt':10}}
    initial = { 'count':0, 'sum':0}
    reduce = 'function(doc, out) {out.count++, out.sum+=doc.amount_raised}'
    result = db.live_investements.group(key, condition, initial, reduce)[0] 
    return result['count'], result['sum']

def dump_kickstarter():
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