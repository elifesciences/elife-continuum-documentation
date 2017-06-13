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

# Installation and Deployment - **DRAFT**
We use [builder](https://github.com/elifesciences/builder) for deployment of components of the system. Please refer to the  [deployment and configuration guide](https://github.com/elifesciences/elife-continuum-documentation/blob/master/deployment-and-configuration.md).

# Feedback and mailing list

We have setup a [mailing list](https://groups.google.com/forum/#!forum/elife-continuum-list) for this project. For feature requests bugs please file an issue in [this repository](https://github.com/elifesciences/elife-continuum-documentation/issues).  
