#Moving Parts

##elife-bot

(decider and worker pre-date PPP project)

#### decider.py
polls for and reacts to swf decisions to schedule execution of activities by the worker

####worker.py
polls for activities that have been scheduled and executes them

####queue_workflow_starter.py
polls workflow starter queue for messages in a defined format and calls the starter for the workflows described in the messages, passing the included parameters. This is a general mechanism for calling bot workflow starters and is potentially applicable outside the PPP parts of the bot.

####queue_worker.py
listens to an SQS queue that receives standard S3 notification messages and adds messages to the workflow starter queue to process them. Also potentially more widely applicable than just PPP.

##elife-dashboard

####process\_dashboard_queue.py
listens to an SQS queue that the elife-bot adds property and event messages to, and writes them in to the monitoring database. 

####dashboard app
Flask app to display information in the monitoring database and initiate publication of articles held for review.

##elife-article-scheduler

####scheduler app 
django app to store scheduled publication information for articles.

####custom admim command 
runs via cron and sends messages to the dashboard when the scheduled publication of an article is due.

##jats-scraper

uses elife-tools and the scraper library to convert JATS XML files to EIF (elife ingest format) JSON files

##elife-tools

Python API to JATS XML files