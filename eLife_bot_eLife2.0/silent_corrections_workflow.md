 
##Introduction

The Silent Corrections process has long been needing automation and considering the new changes for Bot/lax integration, the usual Silent corrections way would not work. The solution we came up with was to have a workflow definition just for Silent Corrections, re-using most of the bot/lax workflow activities.

That create the workflows SilentCorrectionsIngest and SilentCorrectionsProcess.
##Step 1 - Starting the SilentCorrectionsIngest workflow:
The current way to start the SilentCorrectionsIngest workflow is to run it through the econ-feeder passing the workflow-name at the end of the command.
e.g.
python econ_article_feeder.py -p elife-14721-vor-r1 -r 1  elife-bucket-name workflow-starter-queue SilentCorrectionsIngest
##Step 2 - SilentCorrectionsIngest workflow:
At the start of the SilentCorrectionsIngest workflow we will set the values "force = True" and the "version_lookup_function = article_highest_version" which represents the way lax will take the Ingest request and which function the VersionLookup activity should run to get the version from Lax.

Activities:

Version Lookup

ExpandArticle

ApplyVersionNumber

IngestToLax:
- IngestToLax    ----- SQS message ---->  queue:bot-lax-[environment]-inc  

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
                           "force": True }
}
```
About this schema: https://github.com/elifesciences/bot-lax-adaptor/tree/develop/schema 
The only difference between the IngestArticleZip workflow usage of IngestToLax activity is that force will be set to True. That is because a Silent Correction always occurs for an article already published, therefore already ingested. Lax will refuse the ingestion of already published articles unless it has the force attribute set to True.
##Step 3 - lax response adapter:
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
                            u'version': u'1',
                            u'run': u'a8bb05df-2df9-4fce-8f9f-219aca0b0148',
                            u'force': True }
}
```

Sample data converted to worklow_starter_queue compatible format: 
```
{
    'workflow_name': 'SilentCorrectionsProcess'
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
 
##Step 4 - Silent Corrections Process workflow:

The bot workflow starter will poll messages from the AWS "workflow_starter_queue" and will receive the message above that requests the start of 'SilentCorrectionsProcess" workflow. This workflow starter also sets the attribute force to true as lax needs to be aware that's a silent correction Silent Corrections Process runs the following activities:

VerifyLaxResponse:  
- Checks if the ingest request has been successfully made to lax for the given article and wether there is an error with the ingest or not, it will report so to the dashboard.

ScheduleCrossref

ConvertJATS

SetPublicationStatus

ResizeImages

DepositAssets

SetEIFPublish:
- Sets the attribute publish to true on the EIF JSON in S3 (Support for eLife 1.0)

PublishToLax:
- Sends a message to the Lax incoming queue bot-lax-[environment]-inc telling Lax to publish the article with force attribute set to true.
```
{
 'action': 'publish',
 'location': 'https://s3.amazonaws.com/elife-publishing-xml/00353.1/bb2d37b8-e73c-43b3-a092-d555753316af/elife-00353-v1.xml,    
 'id': '00353', 
 'version': '1', 
 'force': True
 'token': (base64encoded){ "run": "bb2d37b8-e73c-43b3-a092-d555753316af",
                           "version": "1",
                           "expanded_folder": "00353.1/bb2d37b8-e73c-43b3-a092-d555753316af",
                           "eif_location": "00353.1/74e22d8f-6b5d-4fb7-b5bf-179c1aaa7cff/elife-00353-v1.json",
                           "status": "vor",
                           "force": True }
}
```
##Step 5 - lax response adapter (publish):
lax_response_adapter will do the same as step 2 but at this time it will poll a message from a "publish" action. After the lax message has been to converted to a workflow_starter compatible message it will be made into a message that aims to start a PostPerfectPublication workflow.
```
{'workflow_name': 'PostPerfectPublication,
 'workflow_data':
     {'article_id': u'837411455',
      'eif_location': u'837411455.1/a8bb05df-2df9-4fce-8f9f-219aca0b0148/elife-837411455-v1.json',
      'expanded_folder': u'837411455.1/a8bb05df-2df9-4fce-8f9f-219aca0b0148',
      'message': None,
      'requested_action': u'publish',
      'result': u'published',
      'run': u'a8bb05df-2df9-4fce-8f9f-219aca0b0148',
      'status': u'vor',
      'update_date': '2013-03-26T00:00:00Z',
      'version': u'1'}}
 ```

 
