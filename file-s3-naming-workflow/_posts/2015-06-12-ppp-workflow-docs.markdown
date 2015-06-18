---
layout: post
title:  "PPP workflow configuration"
date:   2015-06-12 11:40:32
categories: ppp docs workflow
---

{% assign ppp = site.ppp_docs_config %}

# Scene setting

## This documentation

This documentation aims to refer to the [exp branch](https://github.com/elifesciences/elife-bot/tree/exp) of the eLife-bot code.

## Deploying and configuring the bot code

The bot code is deployed via salt. During deployment [elife-poa-xml-generation is cloned]( https://github.com/elifesciences/elife-builder/blob/d0f15aaea37fd953de421c2c84333286078e2823/salt/salt/elife-bot/init.sls#L99) is brought into the same directory structure as the bot-code. The [elife-poa-xml-generation repo](https://github.com/elifesciences/elife-poa-xml-generation) has many functions that are used throughout.

The bot code imports functions from the elife-poa-xml-generation code, e.g. [here](https://github.com/elifesciences/elife-bot/blob/master/activity/activity_PackagePOA.py#L478).


# High Level POA workflow

- Zipfile gets sent to {{ ppp.poa-input-bucket-value }} by EJP  
- `NewS3POA` starter invokes the `PackagePOA` workflow and activity based on a timestamp and the presence of new files having been sent from EJP.  
- A set of directories are created on the ec2 instance that is running the activiy.
- Zipfile gets downloaded to a temporary directory on the Ec2 instance running the activity  
- extract a DOI from the Zipfile
- abort if no DOI can be generated  
- otherwise create a new directory for output to Highwire (https://github.com/elifesciences/elife-bot/blob/master/activity/activity_PackagePOA.py#L192)  
- in the [copy_pdf_to_hw_staging_dir](https://github.com/elifesciences/elife-poa-xml-generation/blob/master/transform-ejp-zip-to-hw-zip.py#L343) function we attempt to decapitate the PDF
- The new processed files are placed in `self.elife_poa_lib.settings.STAGING_TO_HW_DIR`.  
- the processing of the zip file should also have decapitated the PDF from EJP, so we
check whether that PDF has been decapitated. We look in `elife_poa_lib.settings.STAGING_DECAPITATE_PDF_DIR` to see if that decapitated PDF is present.  
- a new manifest XML file is generated for Highwire
- download a set of CSV files from EJP
- create a new XML files for submission to HW that has the article XML in it, insofar as we can generate it from the
csv files downloaded from EJP (this will not cotain the body text of the XML file).  
- copy all of these files to an S3 Outbox  
- create an email of the format " email_type = "PackagePOA" and add this to a mail queue. (Mail templates are stored on s3). This is a
system email and is sent to emails that are configured in `settings.ses_poa_recipient_email`.

---
- the `PublishPOA` workflow kicks in now  
- this invokes the `PublishPOA` and the `DepositCrossref` activities  
- `PublishPOA` creates the following locations
    - self.publish_bucket = settings.poa_packaging_bucket
    - self.outbox_folder = "outbox/"
    - self.published_folder = "published/"  
- files are downloaded from the s3 bucket that `NewS3POA` populated  
- some checks are made to confirm that supp files and zip files have complimentary data and files in them  
- supplement files and zip files are sent to the HW ftp site
- a go.xml file is created and sent the HW FTP endpoint  
- If these files make it to HW then xml is sent to
    - xml_to_crossref_outbox_s3
    - xml_to_pubmed_outbox_s3
    - xml_to_publication_email_outbox_s3
- an email is sent to `settings.ses_poa_recipient_email` (the code here is duplicated from the packacgePOA script)

---
- the `DepositCrossref` activity kicks in
- files are downloaded from s3
- crossref XML is generated
- files are tidied away
- an email is sent to `settings.ses_poa_recipient_email`

---
- Files appears in Highwire express (HWX) with a go.xml file  
- HWX shows all POA articles for the day on one "batch"
- <span style="color:red">HW creates a record in HWX</span>
- <span style="color:red">HW creates nodes in Drupal</span>
- <span style="color:red">supp files are loaded to the appropriate location for download</span>
- the PAP batch shows all the POA papers in HWX
- HWX has a link to the paper in Drupal where the content is in a "not published state"
- production manually checks the PDF on HWX, usually to check against
    - special characters
    - that decapitation has happened on the PDF
    - that the abstract appears OK
    - some other checks (listed in the POA protocalls document)
- production push an "Approve" button
- another page is displayed with another "Approve button"
- a "Success Page" is displayed
- <span style="color:red">Content is added to the search index </span>
- usually within 1/2 an hour the paper on the Drupal Site is in a published state

---

# High level VOR workflow  
- content processor sends a zip file to an S3 bucket and to a HW FTP endpoint
- Files appears in Highwire express (HWX) with a go.xml file  [&#128279;]()
- each file takes it's own batch through the system  
- <span style="color:red">HW creates a record in HWX</span>
- if production can get to HWX then they see the following stages (information can been seen at each of these stages)
    - preintake
    - intake
    - processing
    - assembly
    - production  
    - downstream
- before assembly HWX does the following
  - <span style="color:red">images are converted</span>
  - <span style="color:green">HW creates nodes in Drupal</span>
  - <span style="color:red">assetts are loaded to the appropriate location, e.g. for download or to the CDN</span>
  - <span style="color:red">XML is transformed to HTML and provided via a markdup service</span>
  - <span style="color:red">Some magic rlated article fun happens</span>
- when the workflow gets to assembly assembly will turn organge and prouction can make a decision
- at assembly there is a QA report that links to the Drupal site
- production checks everything in the article on the drupal site
  - videos
  - images
  - tables
  - decsioin letters
- production push an "Approve" button
- another page is displayed with another "Approve button"
- HWX shows that state is changing in the productino process
- if the system works correctly then in about 20 minutes
- <span style="color:red">Content is added to the search index </span>
- <span style="color:red">HW starts to collect PDF download and pageview metrics </span>
- <span style="color:red">RSS feed is updated </span>
- if it goes "red" all bets are off
- elife-bot picks up the zip file and does activities on that zip file **TODO:to be described**

---

# Other Workflows run in our publishing system

---
- `cron_NewS3XML`
- check in SimpleDB for info on any new or modified XML files that are in an S3 bucket since a given date [code](https://github.com/jrdigi/elife-bot/blob/exp/starter/cron_NewS3XML.py#L61)  
- if there is a new or modified XML file then run the [starter_PublishArticle starter](https://github.com/jrdigi/elife-bot/blob/exp/starter/cron_NewS3XML.py#L61)
- `PublishArticle` starter creates a custom workflow for publishing a specific numbered article
- this workflow [calls UnzipArticleXML](https://github.com/jrdigi/elife-bot/blob/exp/starter/cron_NewS3XML.py#L61), [calls LensArticle](https://github.com/jrdigi/elife-bot/blob/exp/starter/cron_NewS3XML.py#L61), [calls ArticleToOutbox](https://github.com/jrdigi/elife-bot/blob/exp/starter/cron_NewS3XML.py#L61), [calls LensXMLFilesList](https://github.com/jrdigi/elife-bot/blob/exp/starter/cron_NewS3XML.py#L61)
- [UnzipArticleXML](https://github.com/jrdigi/elife-bot/blob/exp/activity/activity_UnzipArticleXML.py) - Download a S3 object from the elife-articles bucket, unzip if necessary, and save to the elife-cdn bucket. Functions for handling documents are provided by [filesystem.py](https://github.com/elifesciences/elife-bot/blob/exp/provider/filesystem.py). The cdn name is set  by a [call to settings.py](https://github.com/elifesciences/elife-bot/blob/exp/activity/activity_UnzipArticleXML.py#L58). **TODO:How do we know where to download a file from?**
- `LensArticle` Create a lens article index.html page for the particular article. The HTML template for the lens landing page is stored in S3 and is accessed via [templates.py](https://github.com/elifesciences/elife-bot/blob/exp/provider/templates.py). The name of the
location of the templates dir in s3 is [set in settings.py](https://github.com/elifesciences/elife-bot/blob/exp/provider/templates.py#L33). The location of the lens bucket is [set in a call to settings.py](https://github.com/elifesciences/elife-bot/blob/exp/activity/activity_LensArticle.py#L70).
- [ArticleToOutbox](https://github.com/elifesciences/elife-bot/blob/exp/activity/activity_ArticleToOutbox.py) Download a S3 object from the elife-articles bucket, unzip if necessary, and save to outbox folder on S3. This will actually write the file to the following
locations  
```
  self.pubmed_outbox_folder = "pubmed/outbox/"  
  self.publication_email_outbox_folder = "publication_email/outbox/"  
  self.pub_router_outbox_folder = "pub_router/outbox/"  
  self.cengage_outbox_folder = "cengage/outbox/"  
```
Much of the logic seems quite similar to `UnzipArticleXML`, however this activity includes a function [is_resupply](https://github.com/elifesciences/elife-bot/blob/exp/activity/activity_ArticleToOutbox.py#L140) that seems to hard-code
eLife article numbers into volumes, and it's not clear that this is doing. **TODO: find out why we have this card coded**


---
- `cron_NewS3PDF` checks for new PDF file, and if found [starts the starter_PublishPDF](https://github.com/elifesciences/elife-bot/blob/exp/starter/cron_NewS3PDF.py#L79) **TODO:look at how to tidy up the starter code to remove dependency on SDB**  
- The [starter_PublishPDF](https://github.com/elifesciences/elife-bot/blob/exp/starter/starter_PublishPDF.py) [starts the PublishPDF ](https://github.com/elifesciences/elife-bot/blob/exp/starter/starter_PublishPDF.py#L56) **TODO: determine where we look for new PDF files**
- the [workflow_PublishPDF](https://github.com/elifesciences/elife-bot/blob/exp/workflow/workflow_PublishPDF.py) [invokes UnzipArticlePDF](https://github.com/elifesciences/elife-bot/blob/exp/workflow/workflow_PublishPDF.py#L54)  
- [UnzipArticlePDF](https://github.com/elifesciences/elife-bot/blob/exp/activity/activity_UnzipArticlePDF.py) Downloads a S3 object from the elife-articles bucket, unzip if necessary, and save to the elife-cdn bucket **TODO: refactor UnzipArticlePDF along with other activities, that push content to the CDN, and provide one generalised activity for this**.  

---  
- `cron_NewS3SVG` very similar to previous workflow in terms of getting SVG files, but then we do the following
 [call UnzipArticleSVG](https://github.com/elifesciences/elife-bot/blob/exp/workflow/workflow_PublishSVG.py#L54) and then
 [call ConverterSVGtoJPG](https://github.com/elifesciences/elife-bot/blob/exp/workflow/workflow_PublishSVG.py#L65).
 - [UnzipArticleSVG](https://github.com/elifesciences/elife-bot/blob/exp/activity/activity_UnzipArticleSVG.py) Download a S3 object from the elife-articles bucket, unzip if necessary, and save to the elife-cdn bucket.
 - [ConverterSVGtoJPG](https://github.com/elifesciences/elife-bot/blob/exp/activity/activity_ConverterSVGtoJPG.py) - Extract base64 image data from SVG and save as JPG: Download a S3 object from the elife-articles bucket, unzip if necessary, convert each, and save to the elife-cdn bucket. **TODO: evaluate if we need this workflow, or can we dump it and replace it with the on-server image processing workflow that we currently have?**
 **TODO: remove this workflow from cron.py**


---
- `cron_NewS3Suppl` - Cron job to check for new article S3 supplemental and start workflows, eventually runs the
[UnzipArticleSuppl](https://github.com/elifesciences/elife-bot/blob/exp/activity/activity_UnzipArticleSuppl.py) activity. This Downloads a S3 object from the elife-articles bucket, unzip if necessary, and save to the elife-cdn bucket." **TODO: reafctor this method into a general upload to CDN method**.

---
- `cron_NewS3JPG` starts `starter_PublishJPG` which starts the workflow `PublishJPG`, which invokes the activity `UnzipArticleJPG`
- [UnzipArticleJPG](https://github.com/elifesciences/elife-bot/blob/exp/activity/activity_UnzipArticleJPG.py) puts a file into the CDN.

---
- `cron_NewS3FiguresPDF` starts starter `starter_PublishFiguresPDF` which invokes workflow `PublishFiguresPDF` which invokes the activity
`UnzipArticleFiguresPDF` **TODO: refactor crons and starters to place `start_ping_marker` and similar into a single code location**
- [UnzipArticleFiguresPDF](https://github.com/elifesciences/elife-bot/blob/exp/activity/activity_UnzipArticleFiguresPDF.py) again we have
"Download a S3 object from the elife-articles bucket, unzip if necessary, and save to the elife-cdn bucket.".

---
- `PublicationEmail` starts worker `PublicationEmail` which starts activity `PublicationEmail`.
- [PublicationEmail activity](https://github.com/elifesciences/elife-bot/blob/exp/activity/activity_PublicationEmail.py) - Queue emails to notify of a new article publication.
- [sets a POA publication bucket from settings.py](https://github.com/elifesciences/elife-bot/blob/exp/activity/activity_PublicationEmail.py#L50)
- [internally defines some settings](https://github.com/elifesciences/elife-bot/blob/exp/activity/activity_PublicationEmail.py#L50) that specify which article types not to email about, and which kinds of emails to send.
- [downloads templates from s3](https://github.com/elifesciences/elife-bot/blob/exp/activity/activity_PublicationEmail.py#L341)
- [gets xml files from s3 outbox](https://github.com/elifesciences/elife-bot/blob/exp/activity/activity_PublicationEmail.py#L109)
- do some author extraction and article checking
- [send an email](https://github.com/elifesciences/elife-bot/blob/exp/activity/activity_PublicationEmail.py#L150)
- emails are sent by adding the [email to a queue](https://github.com/elifesciences/elife-bot/blob/exp/activity/activity_PublicationEmail.py#L583) **TODO: find out how this queue is then processed for actually sending mail**
- [clean up the outbox](https://github.com/elifesciences/elife-bot/blob/exp/activity/activity_PublicationEmail.py#L157)


---
- `PubRouterDeposit_HEFCE` there is [an interesting](https://github.com/elifesciences/elife-bot/blob/exp/starter/starter_PubRouterDeposit.py#L63) logic block that multipurposes this starter to start a workflow if the workflow is `HEFCE` or `Cengage`. Starts workflow `PubRouterDeposit`.
Starts activity `PubRouterDeposit`.
- [PubRouterDeposit activity](https://github.com/elifesciences/elife-bot/blob/exp/activity/activity_PubRouterDeposit.py) "Download article XML from pub_router outbox, approve each for publication, and deposit files via FTP to pub router."
- looks again at [poa packaging outboux](https://github.com/elifesciences/elife-bot/blob/exp/activity/activity_PubRouterDeposit.py#L55)
- if we have an approved article [ftp the article](https://github.com/elifesciences/elife-bot/blob/exp/activity/activity_PubRouterDeposit.py#L105) **TODO: get clarity on how we get aproval for this step**  
- starts the [FTPArticle workflow](https://github.com/elifesciences/elife-bot/blob/exp/activity/activity_PubRouterDeposit.py#L163). This seems to potentially be the first location where an activity starts a new workflow.
- the [FTPArticle workflow](https://github.com/elifesciences/elife-bot/blob/exp/workflow/workflow_FTPArticle.py) simply starts the
[FTPArticle activity](https://github.com/elifesciences/elife-bot/blob/exp/activity/activity_FTPArticle.py)
- creates [internal activity directories](https://github.com/elifesciences/elife-bot/blob/exp/activity/activity_FTPArticle.py#L71)
- [download files to be sent](https://github.com/elifesciences/elife-bot/blob/exp/activity/activity_FTPArticle.py#L79)  
- [choose between HEFCE and CENGAGE](https://github.com/elifesciences/elife-bot/blob/exp/activity/activity_FTPArticle.py#L85) for ftping the article
- extract ftp credentials [from the settings.py file](https://github.com/elifesciences/elife-bot/blob/exp/activity/activity_FTPArticle.py#L105-L117)
- the main differences between HEFCE and CENGAGE can be seen [here](https://github.com/elifesciences/elife-bot/blob/exp/activity/activity_FTPArticle.py#L121-L137) and seem to be based on differences in files to be sent.  
**TODO: refactor to rationalise download from s3**  
**TODO: refactor activity_FTPArticle.py to be a generic FTP script with no knowledge of the endpoint**

---
- `PubRouterDeposit_Cengage`  - this is identical to the PubRouterDeposit_HEFCE starter, execpt that the workflow id is set to
Cengage in order to trigger the if clauses int he PubRouterDeposit workflow.


---
- `PubmedArticleDeposit` starts workflow `PubmedArticleDeposit` which starts activity `PubmedArticleDeposit`
- [PubmedArticleDeposit activity](https://github.com/elifesciences/elife-bot/blob/exp/activity/activity_PubmedArticleDeposit.py) Download article XML from pubmed outbox, generate pubmed article XML, and deposit with pubmed.
- [poa packaging bucket set by settings](https://github.com/elifesciences/elife-bot/blob/exp/activity/activity_PubmedArticleDeposit.py#L66)
- [download files](https://github.com/elifesciences/elife-bot/blob/exp/activity/activity_PubmedArticleDeposit.py#L93)
- [ftp file files](https://github.com/elifesciences/elife-bot/blob/exp/activity/activity_PubmedArticleDeposit.py#L104)
- this [calls on a funciton in the elife-poa-xml-generation repo to ftp to highwire](https://github.com/elifesciences/elife-bot/blob/exp/activity/activity_PubmedArticleDeposit.py#L604)
- the actual [ftp to highwire code](https://github.com/elifesciences/elife-poa-xml-generation/blob/master/ftp_to_highwire.py) seems to get it's
FTP settings from a [settings file local to elife-poa-xml-generation](https://github.com/elifesciences/elife-poa-xml-generation/blob/master/ftp_to_highwire.py#L23-L27)
- **TODO: bring the ftp to pubmed function into a common ftp function** 


**TODO: bring more clarity to which kinds of new files (VOR vs POA, asset vs XML) are the files that get actioned by the many cdn deposit workflows.**



---

# Global configuration options for PPP workflow

Get all of our pieces of AWS infrastructure setup in the correct regions.

`{{ ppp.region }} = {{ ppp.region-value }}`

`{{ ppp.sqs-region }} = {{ ppp.region-value }}`

`{{ ppp.simple-db-region }} = {{ ppp.region-value }}`

`{{ ppp.ses-region }} = {{ ppp.region-value }}`


Setup variable for the Amazon Simple Workflow  

`{{ ppp.domain }} = {{ ppp.domain-value}}`  

`{{ ppp.task-list }} = {{ ppp.task-list-value}}`  

Setup variable for the Amazon Simple Queue Service

  `{{ ppp.monitor-queue }} = {{ ppp.monitor-queue-value }}`

  `{{ ppp.monitor-bucket }} = {{ ppp.monitor-bucket-value }}`  

  `{{ ppp.eif-output-bucket }} = {{ ppp.eif-output-bucket-value }}`

---

# eLife bot info.

We refer to workers that are part of the [{{ ppp.bot-repo }}]()

# File naming convention.

The file naming convention can be found at [{{ ppp.naming-convention }}]()

---

# The cron file

A system wide [cron]() file runs. This invokes a [cron.py]({{ ppp.bot-cron-py }}) script.

This script runs multiple starters that start workflows, which call specific sets of activities.

---
I should make the answer more complete,

https://github.com/elifesciences/elife-bot/blob/master/activity/activity_PackagePOA.py#L146
That is where the settings bucket name gets used to download the POA zip package

https://github.com/elifesciences/elife-bot/blob/master/provider/ejp.py#L33
The ejp provider takes the CSV bucket and knows how to find the latest files and data from them

From: Graham Nott [mailto:gnott@starglobal.ca]
Sent: June-12-15 11:21
To: 'Ian MULVANY'
Subject: RE: question about POA bucket settings

Bucket names I see,

For live they are

Where POA zip files are
https://github.com/elifesciences/elife-bot/blob/master/settings-example.py#L167

Where EJP CSV files are
https://github.com/elifesciences/elife-bot/blob/master/settings-example.py#L151

There's a different value for each environment, and these of course are in settings.py  (taken from the example)

From: Ian MULVANY [mailto:i.mulvany@elifesciences.org]
Sent: June-12-15 11:08

---

#### S3Monitor
  is a generic activity that can look to see if there is something new in an S3 bucket,
  can probably remain unchanged.

  The `S3Monitor` workflow runs an [S3Monitor activity]({{ ppp.bot-s3-monitor-activity }}) which checks an S3 bucket to see if it has been modified. The time window
  in which this activity checks an S3 bucket is hardcoded into the cron.py script.

  The `S3Monitor activity` checks state against an AWS Simple DB. This is configured
  in settings.py with the following setting

  `{{ ppp.simple-db-namespace }} = {{ ppp.simple-db-namespace-value }}`

  The S3 bucket that S3Monitor activity will check against is passed in via a data
  value to the `do_activity` method of the class instance. It returns information
  on any items that have changed since last checked.

  **I'm not sure how the S3Monitor activity is pointed at the bucket it needs to
  look at for the POA publication workflow**.

  The input S3 bucket that is checked for the PublishPOA workflow is set in setttings.py with
  the following setting

    `{{ ppp.poa-input-bucket }} = {{  ppp.poa-input-bucket-value }}`



#### `cron_NewS3POA`
  downloads zip files and csv files from S3 buckets that EJP delivers to. Creates
  the POA xml from these, and decapitates the PDF. Prepares content for later
  publication by placing the generated files into an s3 outbox. We may want to
  create the EIF JSON here.  


#### **to be described**
- `cron_NewS3XML`
- `cron_NewS3PDF`
- `cron_NewS3SVG`
- 'cron_NewS3Suppl'
- `cron_NewS3JPG`
- `cron_NewS3FiguresPDF`

We may want to include a new workflow for generating the appropriate images as
an extension here.  


---

#### PublishPOA

`starter_PublishPOA`
  Publishes POA content that the bot has created from files sent to S3 from EJP.
  These get publised to `Highwire` `Crossref` and `pubmed`. This activity checks
  that delivered files contain xml and pdf. This generates the go.xml file needed
  for Highwire. This prepares an email to be sent to authors to notify them that
  they have been published. We will need to intercept or replace the control
  mechanisim in this part of the workflow as part of the PPP project.  


The PublishPOA workflow starts two actvities: `PublishPOA` and `DepositCrossref`.


#### PublishPOA Activity

New files are downloaded from an S3 Bucket to a temporary set of
directories on the `Ec2` instance running the activity.

These tempoarary directories are configured created and named in , and they can
be set in settings.py if desired, but if not set the bot will create them automatically.

This overriding happens in the `override_poa_settings` method of the `activity_PublishPOA`.

Settings that can be overridden are

{% highlight python %}
  # Override the settings
   settings.XLS_PATH                   = self.get_tmp_dir() + os.sep + 'ejp-csv' + os.sep
   settings.TARGET_OUTPUT_DIR          = self.get_tmp_dir() + os.sep + settings.TARGET_OUTPUT_DIR
   settings.STAGING_TO_HW_DIR          = self.get_tmp_dir() + os.sep + settings.STAGING_TO_HW_DIR
   settings.FTP_TO_HW_DIR              = self.get_tmp_dir() + os.sep + settings.FTP_TO_HW_DIR
   settings.MADE_FTP_READY             = self.get_tmp_dir() + os.sep + settings.MADE_FTP_READY
   settings.EJP_INPUT_DIR              = self.get_tmp_dir() + os.sep + settings.EJP_INPUT_DIR
   settings.STAGING_DECAPITATE_PDF_DIR = self.get_tmp_dir() + os.sep + settings.STAGING_DECAPITATE_PDF_DIR
   settings.TMP_DIR                    = self.get_tmp_dir() + os.sep + settings.TMP_DIR
   settings.DO_NOT_FTP_TO_HW_DIR       = self.get_tmp_dir() + os.sep + 'do-not-ftp-to-hw' + os.sep

   # Override the FTP settings with the bot environment settings
   settings.FTP_URI = self.settings.POA_FTP_URI
   settings.FTP_USERNAME = self.settings.POA_FTP_USERNAME
   settings.FTP_PASSWORD = self.settings.POA_FTP_PASSWORD
   settings.FTP_CWD = self.settings.POA_FTP_CWD
{% endhighlight %}

**FIND OUT WHICH OF THESE ARE INTERNAL EC2 DIRECTORIES AND WHICH ARE S3 BUCKETS**

These directories are created by the `create_activity_directories` function. This
funciton creates the following directories

  - {{ ppp.tmp-dir-TARGET_OUTPUT_DIR }}  
  - {{ ppp.tmp-dir-STAGING_TO_HW_DIR }}  
  - {{ ppp.tmp-dir-FTP_TO_HW_DIR }}  
  - {{ ppp.tmp-dir-MADE_FTP_READY }}  
  - {{ ppp.tmp-dir-EJP_INPUT_DIR }}  
  - {{ ppp.tmp-dir-STAGING_DECAPITATE_PDF_DIR }}  
  - {{ ppp.tmp-dir-TMP_DIR }}
  - {{ ppp.tmp-dir-XLS_PATH }}
  - {{ ppp.tmp-dir-DO_NOT_FTP_TO_HW_DIR }}

All of the logic of the activity is described in the `do_activity` function. What
it does is

download_files_from_s3_outbox:
    Files `.zip`, `.pdf` and `.xml` files are downloaded from  `{{ ppp.poa-input-bucket }}` to
    **list the local directory name here**. These file types are hardcoded in the
    `download_files_from_s3_outbox` function.

#### DepositCrossref Activity


---

# PPP POA workflow

# POA workflow

### Zip file arrives from the content processor.

A file with a name like `elife-00012-poa.zip` will arrive into

---

# VOR workflow


# YAML config variables.

---

# Current AWS s3 buckets (2015-06-12)

elife-articles
elife-articles-hw
elife-articles-log
elife-billing-alerts
elife-bot
elife-bot-dev
elife-builder
elife-cdn
elife-cdn-dev
elife-cdn-drupal-log
elife-cdn-log
elife-ejp-ftp
elife-ejp-ftp-dev
elife-ejp-ftp-test
elife-ejp-poa-delivery
elife-ejp-poa-delivery-dev
elife-ejp-raw-output
elife-lens
elife-lens-0.1
elife-lens-dev
elife-lens-log
elife-log-data
elife-nas-s3-backup
elife-poa-packaging
elife-poa-packaging-dev
elife-production
elife-share
elife-static-web-host-test
elife-tahi-uploads-dev
elife-tahi-uploads-dev-logs
elife-tnq-crossref-delivery



{{ ppp.aws_base_path }}
