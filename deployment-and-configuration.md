** DRAFT, NOT YET FULLY TESTED **

eLife continuum is currently deployed within eLife's AWS infrastructure. This guide will outline how to install the system on your own AWS infrastructure using  [https://github.com/elifesciences/builder](https://github.com/elifesciences/builder).

As of writing this deployment recipe is incomplete, and will probably not lead to success, but we are actively working on getting this into a usable state ASAP and expect to have a Jenkins build pipeline ready soon.


# System configuration

## Image File Format configuration

## Default Publishing Behaviour configuration

## Configuring default publishing workflows

Most of the workflows in continuum are triggered by a message sent into a specific Amazon SQS queue, the `workflow-starter-queue`. There is a long running process that listens to messages on this queue. If the message is in the correct format, and contains the name of a registered workflow, then `queue-workflow-starter.py` triggers that workflow.

Amazon S3 buckets can be configured to send a message to a queue if any of their content is modified. We make use of this to start the very first of the workflows. Modifications to a specific bucket are configured to send a message into a `S3_monitor_queue`. There is a long running process `queue_worker.py` that listens in to this queue. `queue_worker.py` is configured to launch a workflow defined in `newFileWorkflows.yaml`. It does this by sending a message in to `workflow-starter-queue` and the usual process takes over from there. In this way files arriving from a typesetter can automatically trigger the appropriate publication workflows, and those workflows can be configured easily by modifying `newFileWorkflows.yaml`.
