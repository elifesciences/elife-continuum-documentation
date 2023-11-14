# eLife Continuum

- [eLife Continuum](#elife-continuum)
- [Introduction](#introduction)
- [Conceptual overview](#conceptual-overview)
- [A comment about the the technology](#a-comment-about-the-the-technology)
- [Components](#components)
- [Installation and Deployment - **DRAFT**](#installation-and-deployment---draft)
- [Feedback and mailing list](#feedback-and-mailing-list)
- [Licensing](#licensing)

# Introduction

Continuum is a set of software components that form a publishing and article hosting system.

This documentation describes these components and how they fit together, customised and deployed.

# Conceptual overview

Continuum takes article packages from a content processor and then transforms those packages so that they can be hosted on the web. It provides production teams with a dashboard to manage the publishing and scheduling of articles. It is built out of a number of software components and these components mostly interact through a set of well described APIs, meaning that individual parts of the system can be replaced or extended as necessary.

# A comment about the the technology

Most components are written in either Python or PHP, the preferred database is PostgreSQL and we make extensive use of Amazon Web Services, particularly CFN, EC2, S3 and RDS.

# Components

The actual software resides in the following repositories

* [https://github.com/elifesciences/elife-dashboard](https://github.com/elifesciences/elife-dashboard)
* [https://github.com/elifesciences/elife-article-scheduler](https://github.com/elifesciences/elife-article-scheduler)
* [https://github.com/elifesciences/elife-bot](https://github.com/elifesciences/elife-bot)
* [https://github.com/elifesciences/elife-tools](https://github.com/elifesciences/elife-tools)
* [https://github.com/elifesciences/lax](https://github.com/elifesciences/lax)
* [https://github.com/elifesciences/bot-lax-adaptor](https://github.com/elifesciences/bot-lax-adaptor)
* [https://github.com/elifesciences/elife-metrics](https://github.com/elifesciences/elife-metrics)
* [https://github.com/elifesciences/journal](https://github.com/elifesciences/journal)
* [https://github.com/elifesciences/annotations](https://github.com/elifesciences/annotations)
* [https://github.com/elifesciences/annual-reports](https://github.com/elifesciences/annual-reports)
* [https://github.com/elifesciences/bioprotocol](https://github.com/elifesciences/bioprotocol)
* [https://github.com/elifesciences/digests](https://github.com/elifesciences/digests)
* [https://github.com/elifesciences/journal-cms](https://github.com/elifesciences/journal-cms)
* [https://github.com/elifesciences/lens](https://github.com/elifesciences/lens)
* [https://github.com/elifesciences/personalised-covers](https://github.com/elifesciences/personalised-covers)
* [https://github.com/elifesciences/profiles](https://github.com/elifesciences/profiles)
* [https://github.com/elifesciences/recommendations](https://github.com/elifesciences/recommendations)
* [https://github.com/elifesciences/search](https://github.com/elifesciences/search)

# Feedback and mailing list

For feature requests bugs please file an issue in [this repository](https://github.com/elifesciences/elife-continuum-documentation/issues).

# Licensing

eLife Continuum is licensed under the [MIT License](https://github.com/elifesciences/elife-continuum-documentation/blob/master/LICENSE) unless otherwise indicated.
