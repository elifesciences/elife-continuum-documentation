eLife Continuum

** DRAFT DOCUMENTATION **

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
* [https://github.com/elifesciences/elife-website](https://github.com/elifesciences/elife-website)
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

Flask app publishing dashboard that can trigger article publication, the scheduling of future publication, and the previewing of articles.

### [https://github.com/elifesciences/elife-article-scheduler](https://github.com/elifesciences/elife-article-scheduler)

Django app that stores information about when an article should be published in the future.

### [https://github.com/elifesciences/elife-bot](https://github.com/elifesciences/elife-bot)

Python app that encodes all publishing workflows and activities.

### [https://github.com/elifesciences/elife-metrics](https://github.com/elifesciences/elife-metrics)

Stores google analytics page view data on articles to support the altmetrics display on article pages.

### [https://github.com/elifesciences/elife-website](https://github.com/elifesciences/elife-website)

Drupal instance of the eLife website.

### [https://github.com/elifesciences/jats-scraper](https://github.com/elifesciences/jats-scraper)

Maps metadata extracted from JATS XML into JSON.

### [https://github.com/elifesciences/elife-tools](https://github.com/elifesciences/elife-tools)

A set of utility tools, including a JATS scraper written in python, exposing JATS nodes in a pythonic way.

### [https://github.com/elifesciences/lax](https://github.com/elifesciences/lax)

Metadata store used to keep track of article versions, and other article related metadata.

### [https://github.com/elifesciences/elife-continuum-documentation](https://github.com/elifesciences/elife-continuum-documentation)

Documentation for the project.

### [https://github.com/elifesciences/builder](https://github.com/elifesciences/builder)

Infrastructure as code, a tool to build the machines that run the components of Continuum.

### [https://github.com/elifesciences/builder-private-example](https://github.com/elifesciences/builder-private-example)

A support repository to help you get started with how to manage secrets and other confidential configuration information when building components of the system.

## Article processing flow

![Processing floiw][processing-flow]

[processing-flow]: https://raw.githubusercontent.com/elifesciences/elife-continuum-documentation/master/elife-continuum-docs/architecture-schematic.001.jpeg

Articles are processed through the system using workflows that are managed by Amazon Simple Workflow. These workflows are made up of activities that do the actual work. An activity can be configured to trigger another workflow, and this triggering is done by posting a message into a queue. Any activity can report into an event store, and the publishing dashboard reads from the event store to show the article status to the production team. The publishing dashboard can also trigger a specific workflow that will set the article to a published. This is done by communicating via API with the hosting platform - Drupal.

The diagram above gives a simplified overview of how the system operates. The initial workflow is triggered as soon as an article is sent to a named AWS S3 bucket, which has been configured to trigger a notification on a queue. In the initial workflow the system checks to see if the article has already been published, and if so what version number the article is on. It will then assign a new version number to the article. This information is kept in the lax metadata store.

A more detailed diagram of how workflows trigger other workflows can be [found here](https://github.com/elifesciences/elife-continuum-documentation/blob/master/elife-continuum-docs/workflow_starting_detail.jpg), and a more detailed diagram of the main publishing workflows with activities can be [found here](https://github.com/elifesciences/elife-continuum-documentation/blob/master/elife-continuum-docs/workflow_overview_detailed.jpg).  

# A note about file formats and file naming

- point to documentation
- mention metadata contained in file naming
- point to example articles that you can use to drive your projects with

# A note about communication with Drupal

# Installation and Deployment - **DRAFT**
We use [builder](https://github.com/elifesciences/builder) for deployment of components of the system. (More details to follow).
