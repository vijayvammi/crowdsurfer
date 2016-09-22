# crowdsurfer
Interview questions for crowdsurfer

The main script for the questions is in main_script.py which can be invoked by 
$python main_script.py

Internally it just calls four different functions relating to the four sections of the assessment. 

1). store_in_db() -- The function extracts information from crowdcube and stores it in mongodb

2). analyze_investements() -- Sums up the amount_raised by all live projects in crowdcube with more than 10 days left.

3). analyze_investements_mongo() -- Does the same as previous function but by using MongoDB's aggregation framework

4). dump_kickstarter() -- Uses kickstarter internal API to get information about projects in JSON format and stores them in Mongo.
  
Unit and integration tests for most of the functions are written in :

    test_scrape_crowdcube.py -- Unit tests for extract function of scrape_crowdcube

    test_main_script.py -- Unit and integration tests for using main_script

I have used py.test framework to write the tests and they can be invoked by using pytest in the main directory. 
