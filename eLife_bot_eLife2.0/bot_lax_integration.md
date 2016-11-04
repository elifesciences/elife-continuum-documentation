##Introduction:
eLife has decided to change its site and article delivery architecture and that involves using an new JSON standard for article delivery to the new Drupal website.

The bot currently is responsible for dealing with the article zip file and it's figures and does operations such as resizing images, convert JATS XML to EIF JSON format and publishes to the eLife website (1.0).
[View eLife 1.0 documentation here](https://github.com/elifesciences/elife-continuum-documentation/blob/master/elife-continuum-docs/workflow_overview_detailed.jpg)

It was decided that the XML(JATS) to JSON conversion would no longer be done under the eLife bot (a.k.a. "bot") but in Lax. The JSON standard has also been changed and the previously used format, EIF, will be deprecated. However before removing the old EIF publication implementation, we need to run the new (2.0) and old (1.0) implementations in parallel. 

That created a necessity to split the bot PublishPerfectArticle workflow in order to 'talk' to Lax and once completed, continuing through a second workflow:

Publish Perfect Article Workflow activities:

ExpandArticle

ApplyVersionNumber

ScheduleCrossref

ConvertJATS

SetPublicationStatus

ResizeImages

DepositAssets

PreparePostEIF

_________________________

The conversion of XML (JATS) to JSON in the future will no longer happen in Publish Perfect Article workflow, but in lax. So we needed to split the Publish Perfect Article workflow into two, "Ingest Article Zip" and "Process Article Zip":
(In fact, we will still support XML (JATS) to JSON EIF on the bot, as we need to run both conversions in parallel for now) 
##Step 1 - Ingest Article Zip workflow:
~~Publish Perfect Article Workflow~~ new name: Ingest Article Zip
IngestArticleZip activities: 

Version Lookup

ExpandArticle

ApplyVersionNumber

IngestToLax   

_________________________
As we can see, we took the first activities from the previously called Publish Perfect Article Workflow and added a new activity called "Ingest To Lax". IngestToLax will write a message to an incoming queue that Lax will read from and perform XML/JSON conversions and ingest the JSON file to the new Drupal site.

IngestToLax    ----- SQS message ---->  queue:bot-lax-[environment]-inc  

The data to be sent from the bot by IngestToLax activity will look like the following:
```
{
 'action': 'ingest',
 'location': 'https://s3.amazonaws.com/elife-publishing-xml/00353.1/bb2d37b8-e73c-43b3-a092-d555753316af/elife-00353-v1.xml,    
 'id': '00353', 
 'version': '1', 
 'token': (base64encoded){ "run": "bb2d37b8-e73c-43b3-a092-d555753316af",
                           "version": "1",
                           "expanded_folder": "00353.1/bb2d37b8-e73c-43b3-a092-d555753316af",
                           "eif_location": "",
                           "status": "vor",
                           "force": False }
}
```
About this schema: https://github.com/elifesciences/bot-lax-adaptor/tree/develop/schema 
 
Once the data is written to the queue, IngestToLax workflow will end its execution.

At this point the article processing is handed to Lax and it will convert the XML to Lax and ingest the article to the new Drupal site. The responsibility is handed back to the bot once Lax writes an SQS message to bot-lax-[environment]-out.

##Step 2 - lax response adapter:
There is a python file lax_response_adapter.py that is responsible for polling for messages from the bot-lax-[environment]-out queue. Once there is an incoming message, lax_response_adapter will parse the data into a format that is compatible with the bot workflow starter queue.

Sample data coming back from Lax:
```
{"status": "ingested",
  "requested-action": "ingest",
  "datetime": "2013-03-26T00:00:00+00:00",
  "id": "837411455"
  "token":(base64 encoded){ u'status': u'vor',
                            u'expanded_folder': u'',
                            u'eif_location': u'837411455.1/a8bb05df-2df9-4fce-8f9f-219aca0b0148/elife-837411455-v1.json',
                            u'version': u'1',u'run': u'a8bb05df-2df9-4fce-8f9f-219aca0b0148' }
}
```


Sample data converted to worklow_starter_queue compatible format: 
```
{
    'workflow_name': 'ProcessArticleZip'
    'workflow_data': {'article_id': u'837411455',
                      'eif_location': u'837411455.1/a8bb05df-2df9-4fce-8f9f-219aca0b0148/elife-837411455-v1.json',
                      'expanded_folder': u'837411455.1/a8bb05df-2df9-4fce-8f9f-219aca0b0148',
                      'message': None,
                      'requested_action': u'ingest',
                      'result': u'ingested',
                      'run': u'a8bb05df-2df9-4fce-8f9f-219aca0b0148',
                      'status': u'vor',
                      'update_date': '2013-03-26T00:00:00Z',
                      'version': u'1'},
}
```

##Step 3 - Process Article Zip workflow:

The bot workflow starter will poll messages from the AWS "workflow_starter_queue" and will receive the message above that requests the start of 'ProcessArticleZip" workflow. Process Article Zip runs the following activities:

VerifyLaxResponse:  
- Checks if the ingest request has been successfully made to lax for the given article and wether there is an error with the ingest or not, it will report so to the [dashboard](https://github.com/elifesciences/elife-continuum-documentation/blob/master/architecture-diagrams/current/dashboard_services.svg).

ScheduleCrossref

ConvertJATS

SetPublicationStatus

ResizeImages

DepositAssets

PreparePostEIF:
- Prepare Post EIF is the last activity of Process Article Zip workflow and it writes a message to website_ingest_queue that is read by a temporary shimmy.py file that posts the created JSON to EIF. Message format:

```
{ "eif_filename": "837411455.1/a8bb05df-2df9-4fce-8f9f-219aca0b0148/elife-837411455-v1.json",
  "eif_bucket": "bucket_name"
  "passthrough": {
                     "article_id": "00353", 
                     "version": "1",
                     "run": "a8bb05df-2df9-4fce-8f9f-219aca0b0148",
                     "article_path": "content/1/e00353v1",
                     "expanded_folder": "837411455.1/a8bb05df-2df9-4fce-8f9f-219aca0b0148",
                     "status": "vor",
                     "update_date": "2012-12-13T00:00:00Z" }
```

##Step 4 - shimmy:
Once ProcessArticleZip is finished, the message with the format previously shown will be in the website_ingest_queue waiting to be read by an adapter between ProcessArticleZip and ArticleInformationSupplier workflows which is called shimmy.py. 
Its only responsibilities are to poll messages from website_ingest_queue (Amazon SQS queue) which will contain the eif file address inside S3 which will be read and then posted to the old Drupal website. 
If the POST is successful shimmy.py will write a message to workflow_starter_queue which is the queue that is used generally to start the bot workflows. 

The format of the message will be the following:
```
{
    'workflow_name': 'ArticleInformationSupplier'
    'workflow_data': {'article_id': u'837411455',
                      'eif_filename': u'837411455.1/a8bb05df-2df9-4fce-8f9f-219aca0b0148/elife-837411455-v1.json',
                      'eif_bucket' : u'bucket_name'
                      'expanded_folder': u'837411455.1/a8bb05df-2df9-4fce-8f9f-219aca0b0148',
                      'requested_action': u'ingest',
                      'result': u'ingested',
                      'run': u'a8bb05df-2df9-4fce-8f9f-219aca0b0148',
                      'status': u'vor',
                      'update_date': '2013-03-26T00:00:00Z',
                      'version': u'1'},
}
```

##Step 5 - Article Information Supplier workflow:
ArticleInformationSupplier workflow contains only one activity, PostEIFBridge. PostEIFBridge only does one bit of logic. 
It checks whether the ingest that was made was also an ingest + publish. That information was sent via the workflow starter queue message. 

If publish is true, it will trigger another workflow called PostPerfectPublication (OBS: This case should no longer happen since we are not going to support automatic publishing - through a setting on the publication_settings.yaml file. We made that in order to make eLife 2.0 and eLife 1.0 running in parallel less complex). 

More commonly, if publish is false, PostEIFBridge will only send a message to a different queue, event_monitor_queue (it monitors the whole article publishing pipeline on the Dashboard) setting the property "publication-status" to "ready to publish". On the Dashboard, that moves the article to the panel of "ready to publish" articles. From there, the user can preview and click Publish for the given article(s).


From this point, the bot workflow starter will keep polling for queues waiting for its next workflow startup. For the article concerned in this document, the action that will write a message to worklow_starter_queue is the Dashboard user's click on the "Publish" button.

##Step 6 - Approve Article Publication workflow:

This workflow is responsible for Publishing an article on both Lax (eLife 2.0) and the Drupal website (eLife 1.0). This is done by each of the two activities:

PublishToLax 
- As its name says, this activity writes a message to the Lax incoming queue bot-lax-[environment]-inc. The message has the same format as the ingest message, but with the action: publish:
```
{
 'action': 'publish',
 'location': 'https://s3.amazonaws.com/elife-publishing-xml/00353.1/bb2d37b8-e73c-43b3-a092-d555753316af/elife-00353-v1.xml,    
 'id': '00353', 
 'version': '1', 
 'token': (base64encoded){ "run": "bb2d37b8-e73c-43b3-a092-d555753316af",
                           "version": "1",
                           "expanded_folder": "00353.1/bb2d37b8-e73c-43b3-a092-d555753316af",
                           "eif_location": "00353.1/74e22d8f-6b5d-4fb7-b5bf-179c1aaa7cff/elife-00353-v1.json",
                           "status": "vor",
                           "force": False }
}
```

About this schema: https://github.com/elifesciences/bot-lax-adaptor/tree/develop/schema 

ApprovePublication:
- Puts the publish flag to true and writes a message to workflow_starter_queue to start the PostPerfectPublication workflow.

##Step 7 - lax response adapter (publish):
lax_response_adapter will do the same as step 2 but at this time it will poll a message from a "publish" action. After the lax message has been to converted to a workflow_starter compatible message it will be made into a message that aims to start a PostPerfectPublication workflow.

##Step 8 - Post Perfect Publication:

We notice here that the 2 previous steps both start PostPerfectPublication workflow. That is deliberate as we wanted, until now, to support processing for both sites, 1.0 and 2.0. At this point however, we want to only continue once, as the PostPerfectPublication activities are not directly related to the sites, they only do archiving procedures and start other services that we only want to run once. In order to make it possible we use an attribute on the settings file "publication_authority" that is checked during the first activity of this workflow "VerifyPublishResponse".

VerifyPublishResponse:
- Checks publication_authority settings.
- If it's "elife-website" and the process that started PostPerfectPublication came from lax_response_adapter, it will stop that workflow execution gracefully. 
- If it's "elife-website" and the process that started PostPerfectPublication came from ApprovePublication, it will continuity to the activity. 
- If it's "Journal" and the process that started PostPerfectPublication came from ApprovePublication, it will stop that workflow execution gracefully.
- If it's "Journal" and the process that started PostPerfectPublication came from lax_response_adapter, it will give continuity to the activity. 
- The 'winner' execution will not be stopped and if that is the one from lax, it will check if the response was positive or negative and it will report to the dashboard success or error. If it reports error it will stop the workflow execution with a "Permanent failure" flag and if it's success it will proceed with the rest of the workflow. If the winner is the request that originated from ApprovePublication activity (under Approve article publication workflow - see step 5), it will simply proceed with the rest of the workflow.

RewriteEIF

ArchiveArticle

~~UpdateLAX~~: 
-This activity is not run on the lax/bot eLife 2.0 scenario. It's only there in case we want to turn off eLife 2.0 process.

LensArticle

ScheduleDownstream 

 
