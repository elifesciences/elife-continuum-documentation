# this doc

this doc describes how to setup the components of the eLife bot on a local machine for development or testing. The elife-bot containts the python components of the PPP publihsing workflow. 

# elife-bot

elife-bot handles the setup and orchestration of the eLife publishing workflow on AWS.

## Terminology

AWS S3 buckets are file stores used for receiving source files, acting as temporary staging areas, and storing processed artefacts.

AWS SQS queues are used for organising messages between different parts of the publishing process.

AWS SNS topics may be subscribed to by multiple queues, and so can be used to fan out message delivery.

AWS domains are used to provide isolated namespaces in some parts of the AWS stack. Domains in different parts of AWS are completely independent, even if they have the same name. The bot uses SWF domains.

An AWS activity describes a thing to be done in an AWS SWF workflow.

An AWS SWF workflow is a defined sequence of AWS activities.

Activities and workflows must belong to exactly one AWS SWF domain. The name of the domain in AWS must match the value in `settings.py` (see below)

The names of the activities and workflows need to be registered with AWS (do this in `register.py`).

A decider works out which workflow step to do next, and schedules it. It does this by working out which was the most recently completed workflow step, and whether it succeeded or failed.

A worker polls the SWF domain for scheduled activies, and runs one if it finds one.

The elife-bot's decider is `decider.py`, and its worker is `worker.py`

## Grab it

```
git clone git@github.com:elifesciences/elife-bot
cd elife-bot
```
## Install dependencies

1. Install ImageMagick [http://www.imagemagick.org/script/index.php](http://www.imagemagick.org/script/index.php) with the optional libtiff library. (On a Mac with Homebrew installed you can do this with `brew install imagemagick --with-libtiff`)

1. create a Python 2 virtual environment (Python 2.7.6 is known to work, Python 2.7.2 is known not to work, so pick accordingly), and activate it.

1. what you do next depends on whether the Python library `libxml2` is already installed in the environment where the bot will live.
    1. **only if libxml2 is already installed:** delete the following line from `requirements.txt`:

       ```
       lxml==3.4.1
       ````
        and build `lxml` statically: `sudo STATIC_DEPS=true pip install lxml==3.4.1`
        (see http://stackoverflow.com/questions/27084580/python-error-when-installing-packages)

    1. **always** run ```pip -r install requirements.txt``` Once this has run, check the permissions on the generated `src` directory within the Python virtual environment. Ensure that the user that will run the bot has write permissions within `src/jats_scraper`, otherwise things will break later.

## Configure prerequisites/settings

Find out what to create in AWS by looking at the `settings.py`, then building it. Or update `settings.py` with details of what you've already built in AWS.

### settings.py

Some of the settings describe the names of things so AWS knows about them. Whatever you call on an AWS service, the relavent names must be described in here so that the bot can use the service correctly.

There is a class for each set of settings that may be used to configure the bot. At the time of writing there are 3: `exp`, `dev` and `live`.

- make sure that the variables `aws_access_key_id` and `aws_secret_access_key` are populated for an appropriate AWS user.

- the name of the AWS SWF domain that will host the activities and workflows is described in the value of the `domain` variable.

- note the value of `s3_hostname`, this must correspond to the AWS region where this infrastructure resides. For example if it's set to `'s3-eu-west-1.amazonaws.com'`, build the S3 buckets things in Ireland. (See the comment in `settings.py`.)

- `publishing_buckets_prefix` is a string that will prefix the name of each of the S3 buckets used by the bot in a development context (your initials are a good choice here). Set to empty string when configuring `live` settings.

- the values of the following variables, together with `publishing_buckets_prefix`, describe the names of the S3 buckets that the bot needs:

    - `production_bucket`
    - `eif_bucket`
    - `expanded_bucket`
    - `ppp_cdn_bucket`
    - `archive_bucket`

   For example, for a dev environment with code like this:
   ```Python
  publishing_buckets_prefix = 'me-'
  ...
  production_bucket = 'elife-production-final'
   ```
   there must be a corresponding S3 bucket named `me-elife-production-final`. (If this were a production environment, the bucket name must be just `elife-production-final`.)

- the values of the following variables describe the names of the SQS queues that the bot needs:

    - `S3_monitor_queue`
    - `event_monitor_queue`
    - `workflow_starter_queue`

- `drupal_EIF_endpoint` and `drupal_approve_endpoint` should be given the appropriate endpoint values for the Drupal site.

# In AWS:
Ensure you're in the correct AWS region (see value of `s3_hostname`, and associated comment in `settings.py`).

- Create 5 S3 buckets corresponding to the names derived in `settings.py`.

- Create 3 SQS queues corresponding to the names described in `settings.py`

- The `S3_monitor_queue` needs to be given permission to monitor the appropriate S3 bucket: this is governed by an access policy. Get the JSON for the access policy at http://docs.aws.amazon.com/AmazonS3/latest/dev/ways-to-add-notification-config-to-bucket.html#step1-create-sqs-queue-for-notification. Replace "SQS-queue-ARN" with the ARN for the S3 monitor queue you're giving the permission to, and "bucket-name" with the name of the S3 bucket the queue should monitor.

- To apply the policy, click on the S3 monitor queue in the AWS console, click the Permissions tab, then "Edit policy document (Advanced)". Paste in the JSON and click through the affirmative actions to save it.

- Now the queue has permission to see the S3 bucket, the bucket needs to be hooked up to the queue. Click on the S3 monitor queue bucket in the AWS console, view its properties, and click on "Events". Fill the form in as follows:
  - In the "Events" field, select "ObjectCreated (All)"
  - For the "Send To" field, select "SQS queue", and then select the appropriate queue
  - In the "SNS topic ARN" field, enter the ARN of the S3 monitor queue.
  - Save the changes.
  
(Note that rather than hooking up the S3 bucket directly to an SQS queue, we could hook it up to an SNS topic instead. An SNS topic may subscribe to multiple queues, and this way the bucket event could be sent to multiple queues concurrently.)

## Getting things running

When a file is dropped into the monitored S3 bucket, a message is put onto the SQS queue;  `queue_worker.py` polls for these messages. When it picks one up, it initiates the workflow starter `starter/starter_NewS3File.py`, which in turn kicks off the workflow `workflow/workflow_NewS3File.py`. This workflow runs the activity  `activity/activity_ProcessNewS3File.py`. Based on the bucket name and the file that's arrived in the S3 bucket, this activity decides which follow on workflow starter to run (e.g. `starter_PublishPerfectArticle.py`).

s3 -> queue -> queue_worker -> starter_news3file -> workflow_news3file -> activity_processnews3file
(activity decides based on bucket and file name)
-> starter for follow-on workflow (e.g. starter_publishperfectarticle)

(Note that the definition of which steps are defined in a workflow is quite flexible. For example, see the `workflow_definition` dict in `workflow/workflow_NewS3File.py`.)

1. Activities and workflows need to be registered on the appropriate SWF domain. To do this, ensure all activities and workflows are included in the appropriate arrays in `register.py`, and run this file. This only needs to happen **if something has changed** in the workflow/activity name since the last time `register.py` was run.

1. Run `queue_worker.py`. 

1. Run `decider.py`: this polls for a decision task, and if it finds one triggers the next appropriate step in the workflow.

1. Run `worker.py`: actually does the work for the next appropriate step in the workflow.

1. Run `queue_workflow_starter.py`: this is simliar to `queue_worker.py`, but listens for messages in elife format rather than S3 format. At the moment, this is only used by the bot to send the "publish" message from the dashboard to the bot.

1. Drop a correctly named and configured article zip file into `production_bucket`.

1. While processing the drop, `worker.py` will probably give a warning about tiff metadata if the article contains images, this may be safely ignored.

1. wait a minute

1. Verify that there no errors being thrown by the bot processes, and that all artefacts are generated in the appropriate buckets as expected. (Resized images should appear in the cdn bucket, and the EIF JSON should appear in the EIF bucket).

1. Load the ingestor site at the Drupal endpoint specified in `settings.py`, and verify that the article appears as expected.

###A note about the scrapers
As part of pip's installation of the requirements, the Python virtual environment will contain `src/scraper`, `src/jats-scraper` and `src/elifetools`. `elifetools` is the parser for JATSXML. This uses Luke's `scraper` wrapped in `jats-scraper` that converts the data to EIF.

