import scrape_crowdcube as sc

from pymongo import MongoClient

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
