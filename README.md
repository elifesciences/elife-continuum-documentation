eLife Continuum

** DRAFT DOCUMENTATION **

<!-- TOC depthFrom:1 depthTo:6 withLinks:1 updateOnSave:1 orderedList:0 -->

- [Introduction](#introduction)
- [Conceptual overview](#conceptual-overview)
- [A comment about the the technology](#a-comment-about-the-the-technology)
- [Components](#components)
- [Licensing](#licensing)
	- [Architecture overview](#architecture-overview)
	- [Component description](#component-description)
		- [[https://github.com/elifesciences/elife-dashboard](https://github.com/elifesciences/elife-dashboard)](#httpsgithubcomelifescienceselife-dashboardhttpsgithubcomelifescienceselife-dashboard)
		- [[https://github.com/elifesciences/elife-article-scheduler](https://github.com/elifesciences/elife-article-scheduler)](#httpsgithubcomelifescienceselife-article-schedulerhttpsgithubcomelifescienceselife-article-scheduler)
		- [[https://github.com/elifesciences/elife-bot](https://github.com/elifesciences/elife-bot)](#httpsgithubcomelifescienceselife-bothttpsgithubcomelifescienceselife-bot)
		- [[https://github.com/elifesciences/elife-metrics](https://github.com/elifesciences/elife-metrics)](#httpsgithubcomelifescienceselife-metricshttpsgithubcomelifescienceselife-metrics)
		- [[https://github.com/elifesciences/jats-scraper](https://github.com/elifesciences/jats-scraper)](#httpsgithubcomelifesciencesjats-scraperhttpsgithubcomelifesciencesjats-scraper)
		- [[https://github.com/elifesciences/elife-tools](https://github.com/elifesciences/elife-tools)](#httpsgithubcomelifescienceselife-toolshttpsgithubcomelifescienceselife-tools)
		- [[https://github.com/elifesciences/lax](https://github.com/elifesciences/lax)](#httpsgithubcomelifescienceslaxhttpsgithubcomelifescienceslax)
		- [[https://github.com/elifesciences/elife-continuum-documentation](https://github.com/elifesciences/elife-continuum-documentation)](#httpsgithubcomelifescienceselife-continuum-documentationhttpsgithubcomelifescienceselife-continuum-documentation)
		- [[https://github.com/elifesciences/builder](https://github.com/elifesciences/builder)](#httpsgithubcomelifesciencesbuilderhttpsgithubcomelifesciencesbuilder)
		- [[https://github.com/elifesciences/builder-private-example](https://github.com/elifesciences/builder-private-example)](#httpsgithubcomelifesciencesbuilder-private-examplehttpsgithubcomelifesciencesbuilder-private-example)
	- [Article processing flow](#article-processing-flow)
- [A note about file formats and file naming](#a-note-about-file-formats-and-file-naming)
- [A note about communication with Drupal](#a-note-about-communication-with-drupal)
- [Installation and Deployment - **DRAFT**](#installation-and-deployment-draft)
- [Feedback and mailing list](#feedback-and-mailing-list)

<!-- /TOC -->

# Introduction
eLife Continuum is the platform that we use to manage the publishing and hosting or our research content. It is composed of a set of software components that form a publishing and article hosting system. In this documentation we will describe those components and how they fit together. We will describe how they can be deployed and customised.

# Conceptual overview

![High Level Overview][high-level-overview]

[high-level-overview]: https://raw.githubusercontent.com/elifesciences/ppp-project/continuum-user-docs/elife-continuum-docs/high-level-overview.jpg

eLife continuum is best described as a production and hosting platform It takes article packages from a content processor and then transforms those packages so that they can be hosted on the web. It also provides production teams with a dashboard to manage the publishing and scheduling of articles. It provides a Drupal 7 site that can be used to host that journal content. It is built out of a number of software components, and these components mostly interact through a set of well described APIs, meaning that different parts of the system can be replaced or extended with relative ease.

# A comment about the the technology
Most of the back-end components are written in python, with the hosting platform built on top of Drupal. We make liberal use of Amazon Web Services, and use a variety of storage engines exposed via RDS, including MySQL and Postgres. Redis is also used to store session information.

We manage workflows using AWS Simple WorkFlow.

# Components
The actual software resides in the following repositories

* [https://github.com/elifesciences/elife-dashboard](https://github.com/elifesciences/elife-dashboard)
* [https://github.com/elifesciences/elife-article-scheduler](https://github.com/elifesciences/elife-article-scheduler)
* [https://github.com/elifesciences/elife-bot](https://github.com/elifesciences/elife-bot)
* [https://github.com/elifesciences/elife-metrics](https://github.com/elifesciences/elife-metrics)
* [https://github.com/elifesciences/jats-scraper](https://github.com/elifesciences/jats-scraper)
* [https://github.com/elifesciences/elife-tools](https://github.com/elifesciences/elife-tools)
* [https://github.com/elifesciences/lax](https://github.com/elifesciences/lax)

Documentation and tools for building the components live in the following repositories

* [https://github.com/elifesciences/elife-continuum-documentation](https://github.com/elifesciences/elife-continuum-documentation)
* [https://github.com/elifesciences/builder](https://github.com/elifesciences/builder)
* [https://github.com/elifesciences/builder-private-example](https://github.com/elifesciences/builder-private-example)

# Licensing

eLife Continuum is licensed under the [MIT License](https://github.com/elifesciences/elife-continuum-documentation/blob/master/LICENSE) .

## Architecture overview

The three main components of continuum are workflow management, the publishing dashboard, and content hosting. Communication between the workflows and the publishing dashboard is done via AWS sqs queues, and this is why no direct relationship is shown in the diagram below, which only describes the modules that eLife has written.

![High level component overview][hl-components]

[hl-components]:https://raw.githubusercontent.com/elifesciences/ppp-project/continuum-user-docs/elife-continuum-docs/high-level-component-overview.jpg

## Component description

### [https://github.com/elifesciences/elife-dashboard](https://github.com/elifesciences/elife-dashboard)

The elife-dashboard is a small flask app that shows information about how an article has been processed through the system. By default articles are not published immediately in the system, and they require human approval. The publishing dashboard provides the mechanism for this approval. The publishing dashboard can trigger a workflow that sets the published state of an article on the Drupal site. The workflow communicates via a REST API that Drupal exposes for this purpose. The publishing dashboard can also be used to schedule articles for future publication. It does scheduling by setting information in the `elife-article-scheduler`

### [https://github.com/elifesciences/elife-article-scheduler](https://github.com/elifesciences/elife-article-scheduler)

This is a small Django app that stores information about when a particular article ought to be published in the future. Publishing times can be set to the minute. The scheduler currently only communicates with the dashboard, and that communication is two way. The scheduler tells the dashboard to publish when its the correct time, and the dashboard both tells the scheduler the expected publication dates and also queries it to find the currently scheduled times).

### [https://github.com/elifesciences/elife-bot](https://github.com/elifesciences/elife-bot)

Python app that encodes all publishing workflows and activities.

### [https://github.com/elifesciences/elife-metrics](https://github.com/elifesciences/elife-metrics)

Stores google analytics page view data on articles to support the altmetrics display on article pages. This is a small Django application.

### [https://github.com/elifesciences/jats-scraper](https://github.com/elifesciences/jats-scraper)

Maps metadata extracted from JATS XML into JSON.

### [https://github.com/elifesciences/elife-tools](https://github.com/elifesciences/elife-tools)

A set of utility tools, including a JATS scraper written in python, exposing JATS nodes in a pythonic way.

### [https://github.com/elifesciences/lax](https://github.com/elifesciences/lax)

Lax is a small Django project that contains metadata about versions of published articles. It exposes a REST API for creating new entires in Lax, and for querying lax for information about an article. The elife-bot checks against lax when a new article comes in to the system to see if a previous version of that articles has already been published.

### [https://github.com/elifesciences/elife-continuum-documentation](https://github.com/elifesciences/elife-continuum-documentation)

Documentation for the project.

### [https://github.com/elifesciences/builder](https://github.com/elifesciences/builder)

Infrastructure as code, a tool to build the machines that run the components of Continuum.

This tool can be used to deploy locally to a Vagrant machine, or to deploy to an AWS instance.

When deploying to AWS you will need to configure your local instance of builder with the appropriate private keys for AWS, along with other confidential information, such as database configuration.

### [https://github.com/elifesciences/builder-private-example](https://github.com/elifesciences/builder-private-example)

A support repository to help you get started with how to manage secrets and other confidential configuration information when building components of the system.

## Article processing flow

![Processing floiw][processing-flow]

[processing-flow]: https://raw.githubusercontent.com/elifesciences/elife-continuum-documentation/master/elife-continuum-docs/architecture-schematic.001.jpeg

Articles are processed through the system using workflows that are managed by Amazon Simple Workflow. These workflows are made up of activities that do the actual work. An activity can be configured to trigger another workflow, and this triggering is done by posting a message into a queue. Any activity can report into an event store, and the publishing dashboard reads from the event store to show the article status to the production team. The publishing dashboard can also trigger a specific workflow that will set the article to a published. This is done by communicating via API with the hosting platform - Drupal.

The diagram above gives a simplified overview of how the system operates. The initial workflow is triggered as soon as an article is sent to a named AWS S3 bucket, which has been configured to trigger a notification on a queue. In the initial workflow the system checks to see if the article has already been published, and if so what version number the article is on. It will then assign a new version number to the article. This information is kept in the lax metadata store.

A more detailed diagram of how workflows trigger other workflows can be [found here](https://github.com/elifesciences/elife-continuum-documentation/blob/master/elife-continuum-docs/workflow_starting_detail.jpg), and a more detailed diagram of the main publishing workflows with activities can be [found here](https://github.com/elifesciences/elife-continuum-documentation/blob/master/elife-continuum-docs/workflow_overview_detailed.jpg).  

# A note about file formats and file naming

The elife-bot expects files coming into the system from the content processor to have a specific structure. This is well documented in the [file naming specification](https://github.com/elifesciences/elife-continuum-documentation/blob/master/file-naming/file_naming_spec.md).  

Of particular note is that article files are expected to contain information indicating whether they contain Version of Record or Publish on Accept files, if containing an already published version, then what the version number is for an article, and if containing a article that has been updated, what the updated date was.

During the development of Continuum we debated whether all of this information ought to be held in a sidecar metadata file. It was close decision, but we proceeded to use the file naming route to indicate some state information. This is a decision that we may revisit in the future. If you wish to implement a different naming convention, or override the eLife Continuum naming convention, then the key place to do this is in the [article structure](https://github.com/elifesciences/elife-bot/blob/develop/provider/article_structure.py) class in the bot, which provides an abstract representation of the critical information about a file to the rest of the system.

For testing we have made available some [sample elife zip files](http://elife-continuum-test-content.s3.amazonaws.com/) which follow to our naming conventions.  

# A note about communication with Drupal

When we initially launched Continuum inside of eLife we encountered a problem with the way that the bot communicated with Drupal. We created an ingest API endpoint in Drupal, but we made it only accept connections in a serial fashion. In contrast the bot will process articles as they appear, and moreover the simple workflow engine will retry activities a number of times before failing. Some articles were taking a long time to ingest on the Drupal side, and the HTTTP connection to the bot was dropping, causing the bot to resend the article to Drupal, while the first request was still being processed. This led to a number of stability issues on the Drupal side.

In order to overcome this we re-engineered the way that the bot communicates with Drupal. Instead of communicating directly the bot places a message on a queue, the `website_ingest_queue`. Another process - [shimmy.py](https://github.com/elifesciences/elife-bot/blob/develop/shimmy.py), picks messages from this queue, and then communicates with Drupal. Shimmy only sends a new article to Drupal once the previous article has been fully ingested. As we tend to publish sever articles together, and then have a period of time between publishing, Drupal has plenty of time to work through the articles that are being sent to it. This also means that were you to create a different hosting system, the communication between that system and the bot can be managed by only modifying shimmy.py, for example if you had a system that could handle ingestion of articles in parallel, for scaling purposes.   

# Installation and Deployment - **DRAFT**
We use [builder](https://github.com/elifesciences/builder) for deployment of components of the system. Please refer to the  [deployment and configuration guide](https://github.com/elifesciences/elife-continuum-documentation/blob/master/deployment-and-configuration.md).

# Feedback and mailing list

We have setup a [mailing list](https://groups.google.com/forum/#!forum/elife-continuum-list) for this project. For feature requests bugs please file an issue in [this repository](https://github.com/elifesciences/elife-continuum-documentation/issues).  
