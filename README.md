
# PPP project

The PPP project is the publishing workflow system used by elifesciences Ltd to
publish content to our journal site [elifesciences.org]().

At a high level we receive files into an AWS bucket via FTP from a content processor.
The arrival of these files trigger workflows written in python, and managed using Amazon Simple Workflow.
These processes prepare the content for display on the web, and push articles into
Drupal, the CMS we use for our website.

There is a publishing dashboard, which is a standalone application, which gives
our production team control over the publishing events, and a view into the
state of the system.

The project is spread across a number of repositories and this repo gives documents
the project at a high level.

## architecture-diagrams  

Documents the AWS processes and communication events between these processes and the
Drupal site.

## file-naming

Each article can be in a number of states (e.g. version of record, publish on accept,
	a variety of version numbers). Each article has a number of potential components (e.g. figures, videos, etc.).
	We document here the naming convention for our files.  

## metatags-and-urls

Articles and article components have specific paths when loaded onto the site. Those paths, and the
associated metatags for those pages, are documented here.  

## ppp-bot-documentation

This covers some documentation on how to confiture and deploy the core python processes
for the publishing workflow, along with how to deploy this code to AWS using our elife
tools.  

## publishing-dashboard-wireframes

This contains wireframes for the publishing dashboard.  

## publishing-workflows

We describe the workflows associated with publishing articles and videos. These are
the workflows that the system supports.  

## archive

Some redundant documentation. 
