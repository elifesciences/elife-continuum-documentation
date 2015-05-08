# PPP config file specification v0.1
### Background

As we develop an internal production system we want to be able to configure aspects of how the system operates. This is a draft proposal for a set of configuration files created in YAML to allow control of the publishing system. 

### Draft files 
##### main config file - draft 
[elife_pub_workflow.yaml](https://gist.github.com/IanMulvany/fcb03b477dcc8525c0b1) 

##### article exceptions file - draft 
[article_exceptions.yaml](https://gist.github.com/IanMulvany/389f2bdc6b7d59b1bf3a)

#### main config file - specification 

`NAME: PPP workflow descrption`
name of the config file. 

`SPEC-VERSION: 0.1`
version of the specificaiton (this doc) 

`MODIFIED: 2015-04-29`
last modification date of the config file 

`domain: publish # vs dev, vs staging, etc.`
our system works on AWS. We want a way to sepearate test dev and live instances of the system. We could look to create namespaces in which the context of these processes happens. We _could_ specify a domain in this config file, and that would trigger our production system to use the named domain. The advantage to this is that it would allow us to setup a version of our production system to run in a dev or test state without writing into the data for the live production system. If we were allowed to freely name the domain then we could also potentially use this for setting up arbitary test harnesses. 

`publishing policy: automatic # vs manual, vs time-delayed`  
Sets the default publishing policy for the publishing platform. 

`exceptions list: /var/config/ppp/article_exceptions.yaml`
Provides a list of article identfiers, whose publishing behaviour defined in this config file should override the default publishing behviour for the platform. 

One of the requirments of the production system is to be able to set content to publish when ready, or to be able to choose to preview content, or to be able to set a specific pubilshing time for specific items of content. (see [https://trello.com/c/3vxvWcEO](https://trello.com/c/3vxvWcEO), [https://trello.com/c/zloXOQIN](https://trello.com/c/zloXOQIN)). The proposal here is that we provide a config option that can set the default behavior for the entire platform. We propose that we offer two kinds of publishing behaviour as default options: `automatic` and `manual`. Automatic mode will publish content according to business rules without any human intervention. (an example of a business rule could be that if the content vendor supplies an article file with the publication date set in the XML then the production system should endevour to publish that content on that date, or throw an error). The `manual` mode will require a person to push a publish button for every piece of content coming through the system. This mode can be useful when testing the sysetem, or testing a move to a new vendor where we want to have a high degree of quality control. 

The exceptions list is a list of article identifiers that take behaviour that overwrites the default pubilshing behaviour. It's proposed that two kinds of overriding behaviour can be specified: `manual` in which case a human is requried to publish this article, or by specifying a date.

The file might look like the following:

>	00013: 2015-04-29 12:00:01 
	00014: manual  
	00015: manual 
	00016: 2015-06-29 12:00:01 

This approach raises a couple of questions:

- can the operator manually override publsihing dates, even for articles that have a date set in the exeptions file?  
- what happens if an article has a date specified in the XML, and a different date set in the execptoins file? 
- what happens if the operator manually overrides publication of an article, such that it conflicts with the date set in the XML file? 
- how do we add items to the execptions file (web interface perhaps?)
- how do items get removed from the exeptions file? (automatically removed on successful publication?) 

> journal: eLife
  
It's proposed that we can specify the journal title within the config file, and options below that apply to that journal. For eLife we only have one journal, but adopting this convention now could allow us to think about extending the platform to be a multi-journal platform in the future. 

`article types:
    - research vor
    - research poa
    - feature
    - editorial
    - correction
    - insight
`
Article types lists the known article variants in the workflow. Weonly need to be able to distinguish how to identify article types that have different workflows.


`article workflows:
    research vor: research poa workflow
    research poa: research vor workflow
    feature: research vor workflow
    editorial: research vor workflow
    correction: research vor workflow
    insight: research vor workflow 
` 
 
This maps our article types onto our defined workflows. Different article types can share the same workflow. 


`valid stages:
  - assembly
  - publish
  - downstream
  - archive
`

This only lists conceptual groupings for steps in the workflows in order to potentially aid in the layout of the production dashboard. These steps have no other effect on the production process. 

` 
workflows:
  research poa workflow:
    assembly:
      prepare poa content:
        order: strict
        timing: cron
          cron directive: 11:00 GMT
    publish:
      publish to drupal:
        order: strict
      crossref:
        config: default
      pub email:
        config: default
      pubmed:
        config: default
    archive:
      s3 archive:
        config: default
 ` 

A workflow is named and the steps in the workflow are slotted into the differnt approriate stages. We have not specificed any exlusionary behaviour here, so it could be possible to attempt to create a workflow that has the same step in different stages, or indeed to assemble a workflow that could never complete. It's assumed that the person creating the workflow will have enough understanding of the underlying system to be able to specify valid workflows. 

Let's have a look at one example step:

`    assembly:
      prepare poa content:
        order: strict
        timing: cron
          cron directive: 11:00 GMT
`

Assembly is the publishing stage. `preapre poa content` is a grouping of individual steps that are listed later in the config file. Each of these stages can either define their own configuration, or  are described on their own at the bottom of the config file, and in that description the default configuration for that step is listed. I was thinking that anywhere that the step is invoked a default configuration option could be overwritten for the specific instance of that step in a given workflow. This could be confusing, and I'm not 100% happy with the way that it has been described here. 

In this example we override the order for this step and the timeing, however `prepare poa content` is composed of a number of steps, and so it's not clear immediatly whether the override applies to each step in that grouping, or just to the completion order of all of the steps taken toghether. I may well be adding too much complexity in here. 

`# some convienience steps
prepare poa content:
  xml_generation:
    config: default
  img_generation:
    config: detault `

This is an example of a number of workflow steps being rolled up into a handy to use alias, however for the first iteration perahps we want to keep the workflow definitions fairly linear, and not allow for this kind of summarisation? It will lead to more verbose settings files, but potentially make them easier to parse. 


`# default options
default config options:
  ---
  xml_generation:
    order: strict
    timer: immediate
    overwrite: true
    append: false
  --- `

This is an example of a publishing workflow step definition. 

`order` determins the order in which steps should be complted. `strict` means that the given step has to complete before subsequent steps are attempted in the workflow. `loose` means that this step is not blocking on attempting subseqent steps. 

`timer` indicates when a step should be run. `immediate` means a step should be run as soon as it has all of the resrouces that it needs to complete. `cron` means that the step needs to wait for a specific time window before it is allowed to be run. If a cron is required then a new line is supplied in the config, giving the cron directive that should be used for this setp. 

`overwrite` determines whether this step will attempt to replace any output that it has previously generated. A good example of an `overwrite: false` directive would be the email to published authors. If we reprocess their content we do not want to resend an email to these authors.

`append` determins whether the process will attempt to deposit a new version of it's output at the step destination. 
 

`workflow mappings:
  crossref: activity_DepositCrossref
  lens: activity_LensArticle 
  pub_router: activity_PubRouterDeposit
  pub email: activity_PublicationEmail
  s3 archive: ??` 

This is a suggestion to potentially map workflow steps to the named SWF activity that is responsible for those steps. 