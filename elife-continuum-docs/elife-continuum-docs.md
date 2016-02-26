# eLife Continuum

## Introduction

## High Level Overview

## Troubleshooting

### Where do my files go?

### Common errors, and overcoming them

#### Dashboard article preview links are truncated.

Occasionally you may see a `The requested URL was not found on the server.` error when trying to view the processing history of an article on the dashboard. Check the link, and if the link looks like The requested URL was not found on the server.``

#### Feeding an article into the system using `ppp-feeder`

`ppp-feeder` is a small command line utility for sending signals to named queues in the publishing workflow.

So for example

	$ python ppp-feeder.py -p elife-10856-vor-r4 -r 1  elife-production-final workflow-starter-queue

	python ppp-feeder.py -p elife-10960-vor-r1 -r 1  elife-production-final workflow-starter-queue

#### Feeding an article into the system using an AWS bucket

#### Feeding an article into the system using the SWF console
