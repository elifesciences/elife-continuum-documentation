
**This document has been superceded by the [eLife file naming and asset IDs](https://github.com/elifesciences/XML-mapping/blob/master/elife_file_naming_2016_08_25.md) document.**

---

# eLife file naming specification

## File naming and workflow

eLife receives articles from a content processor as a zip package delivered to
an Amazon S3 bucket via FTP. Our production system recognises certain metadata
in the name of the zip file, and expects files within the zip file to be named
according to the specification laid out in this document.

Some files are processed and sent to a CDN for access from the main site.

The S3 bucket for inbound content, and the location of the CDN that we populate are specified in a settings file for our production workflow. An [example settings file is available](https://github.com/elifesciences/elife-bot/blob/exp/settings-example.py).

The relevant variables in that settings file are:

> S3_monitor_queue # location of the inbound files

> ppp_cdn_bucket  # location of the CDN

In this documentation we will indicate whether a specific filetype needs to be
placed in the CDN.

## Files and the CDN

### File Types that need to be placed on the CDN

As a rule of thumb all files associated with the article need to be placed directly on the CDN.
The only exception to this rule is in relation to the figures, which need to be processed first,
and then placed on the CDN. Movies are not served by eLife, but we have no reason not to palce them on the CDN.

| Asset Type  | Example Asset Namespaces  | Example File Name | Example Extensions | DOI? |example DOI | landing page? | example landing page |
|---|---|---|---|---|---|---|---|
| Figures |  fig1, app1-fig2, fig1-figsupp1 | elife-07178-fig1-v2.gif  |  .tiff, .gif  | always | 10.7554/eLife.07178.003 | always | http://elifesciences.org/content/4/e07178v2/figure1 |
| article pdf |  - | elife-07178-v2.pdf | .pdf | always | 10.7554/eLife.07178  | always | http://elifesciences.org/content/4/e07178v2  |
| figures pdf | figures  | elife-07178-figures-v2.pdf | .pdf  | never | - | never |  - |
| xml | - | elife-07178-v2.xml  |.xml | always |10.7554/eLife.07178  | always | http://elifesciences.org/content/4/e07178v2  |
| code | code1, fig1-code1, fig1-figsupp3-code1 | elife-00230-fig1-code2-v2.m | .py, .zip, .m | always| 10.7554/eLife.00230.027 | always | http://elifesciences.org/content/2/e00288v4/figure1/figure-supp3/source-code1 |
| data | data1, fig1-data2, fig1-figsupp3-code1-data1 | elife-00230-fig1-figsupp3-code1-data1-v2.zip | .csv, .zip  | always| 10.7554/eLife.06426.014 | always |  http://elifesciences.org/content/2/e00288v4/figure4/source-data1	|
| reporting standards |  repstand1 | elife-00230-repstand1-v2.pdf  | .pdf, .docx | always | 10.7554/eLife.04525.021 | always | http://elifesciences.org/content/2/e00288v4/reporting-standard1 |
| inline media | inf1 | elife-00230-inf2-v2.gif  | .gif, .tex, .mov | never | - | never | - |
| media | fig1-figsupp2-media3, media1, fig2-media2 | elife-00012-fig1-figsupp3-media.mov | .wav, .flac | always | 10.7554/eLife.06426.012 | always | http://elifesciences.org/content/2/e00288v4/media7 |
| supplementary file | supp2, resp-supp2, app3-supp3, dec-fig2-suppfig3-supp1  |  elife-00012-supp2-v2.pdf | .docx, .pdf | always | 10.7554/eLife.01239.011 | always | http://elifesciences.org/content/2/e00288v4/supplemental-file1	|


#### Comment on non-file parents

Any given file can have as a parent one of the following items:

- the base article  
- an appendix `app`
- the decision letter `dec`   
- the author response `resp`
- another file, particularly a figure or figgure suppliment  


#### Comments on some specific file types

**inline media**

- Inline media does not have it's own landing page  
- Inline media does need to be served from the cdn  
- The tagging for inline media in the XML overlaps with the tagging for inline figures  

Example article with inline media: [http://elifesciences.org/content/4/e05169](), This article is an insight, but it
has all four article tabs, and the inline media is an image in the boxed section at the top of the artilce, and the image does not have a DOI.


**media**  

Video files are not hosted on our CDN, but any other media file that we publish will need to be hosted on our CDN. For simplicity
we are going to place all media files onto our CDN. We currently have no examples of media that are not video.


**reporting standards**s

[http://elifesciences.org/content/4/e04525/DC5]() is an example of an article with a reporting standard.


**images**

We receive images as .tiff files, and these are converted to gif files as part of the hte publication process. These gif files need to be sent to the CDN.


**data**

[http://elifesciences.org/content/4/e06426/article-data#fig-data-additional-files]() is an example of a published article with associated data.

**code**

[http://elifesciences.org/content/2/e00631]() is an example of an article with source code.


#### Processing file names

The elife bot has an [`ArticleInfo` Class](https://github.com/elifesciences/elife-bot/blob/exp/provider/article_structure.py) that encapsulates the information that we can infer from an artilce ile name.


#### Processing files to the CDN  

Currently XML files are sent to the CDN with the [DepositXML Activity](https://github.com/elifesciences/elife-bot/blob/exp/activity/activity_DepositXML.py). we anticipate that this will be extended to send all content to the CDN.

This activity runs as part of the PPP projecss, and takes the location of the CDN from the bot `settings.py` file.


#### CDN path names

The CDN base path is set by the variable  

> `ppp_cdn_bucket`  # location of the CDN

in the `settings.py` file of the [elife-bot](https://github.com/elifesciences/elife-bot).

To access a specific file, e.g. `elife-00230-inf2-v2.gif` for a specific article `e00123` in the CDN then you can infer the CDN path from the article number via

> `ppp_cdn_bucket`/00123/elife-00230-inf2-v2.gif

All versions of files for a given article are placed into the same CDN directory:

> `ppp_cdn_bucket`/00123/

So for example in this directory you may have the following

> `ppp_cdn_bucket`/00123/elife-00230-inf2-v1.gif  
> `ppp_cdn_bucket`/00123/elife-00230-inf2-v2.gif  
> `ppp_cdn_bucket`/00123/elife-00230-inf2-v3.gif  


# File naming pattern

>
	`elife-<f-id>-<status>(-<revision><r-id>)(-<asset><a-id>)(-<sub-asset><sa-id>)(-<data><d-id>)(-<code><c-id>)(-<media><m-id>)(-<reporting standard><repstand-id>)(-<supplementary file><supp-id>)|(-v<version>)(-YYYYMMDD).<ext>`

Brackets represent optional components. A pipe represents a choice on component, which may vary depending on it's state in the publishing system.

This pattern covers both inbound zip files and the contents of those zip files. We can break it out into two branches, one for the zip files and one for the assets inside the zip files.

#### Zip File naming pattern

Inbound zip files will be of the form

>
	`elife-<f-id>-<status>(-r<revision>)(-v<version>).zip`

After processing revision numbers will be dropped and zip files will be of the form

>
	`elife-<f-id>-<status>(-v<version>)(-YYYYMMDDHHMMSS).zip`


#### Assets naming pattern

>
	`elife-<f-id>-<status>(-<asset><a-id>)(-<sub-asset><sa-id>)(-<data><d-id>)(-<code><c-id>)(-<media><m-id>)(-<reporting standard><repstand-id>)(-<supplementary file><supp-id>)|(-v<version>).<ext>`


### Components

###### `<f-id>`

This is the file id and is the numerical digit that is used to make up part of the DOI for an article (`<article-id pub-id-type="doi">`). For example an eLife article with the following DOI `/10.7554/eLife.06659` will have an f-id of `06659`.


###### `<status>`

This is either `poa` (publish on accept) or `vor` (version of record).

###### `<asset>`

This refers to an asset file related to an article, ie a figure (fig), source code (code), source data (data), media (includes videos, audio and animation) (media), supplementary file (supp), (figures) the figures pdf, reporting standards (repstand).

<span style="color:red">NOTE: Change on 27th July 2015:</span>

Decision letter, author response and Appendix are now at the level of assets:
dec - decision letter
resp - author response
app - appendix

dec and resp do not require a number, but app does as there could be multiple appendices.
These assets could have any sub assets as below. They will never exist in the file naming heirachy with no sub assets.

###### `<a-id>`

The `a-id` is the asset id, and indicates the order of an asset in the article. For example an
article with three figures will have the following asset files:

- elife-00012-fig1.tiff
- elife-00012-fig2.tiff
- elife-00012-fig3.tiff


###### `<sub-asset>`

Some assets will have sub-assets, eg figure supplements (figsupp), source data (data), or source code (code). These are indicated by the sub-asset component.

###### `<sa-id>`

Some assets have sub-asset ids, for example, an article with three main figures, where one
figure has three figure supplements, and one figure has two figure supplements will have the following:

- elife-00012-fig1.tiff
- elife-00012-fig1-figsupp1.tiff
- elife-00012-fig1-figsupp2.tiff
- elife-00012-fig1-figsupp3.tiff
- elife-00012-fig2.tiff
- elife-00012-fig3.tiff
- elife-00012-fig3-figsupp1.tiff
- elife-00012-fig3-figsupp2.tiff
- elife-00012-app1-fig1


Some assets only have sub-asset ids, for example, an article with 3 appendices, where appendix 2 has 3 figures, and figure 2 has two figure supplements will have the following:

- elife-00012-app2-fig1.tiff
- elife-00012-app2-fig2.tiff
- elife-00012-app2-fig2-figsupp1.tiff
- elife-00012-app2-fig2-figsupp2.tiff
- elife-00012-app2-fig3.tiff


###### data

Sometimes there is source data at a parent level, but sometimes assets will have source data files associated with them. These data files are indicated by the presence of a `data` in the filename.

###### `<d-id>`

Assets can have multiple source data files associated with them, and these are distinguished with the
data id.

For example, an article with three main figures, where one figure has three figure supplements, and one figure has two figure supplements, and all have associated data, with some of them having multiple data files, could have the following:

- elife-00012-fig1.tiff
- elife-00012-fig1-data1.csv
- elife-00012-fig1-data2.csv
- elife-00012-fig1-figsupp1.tiff
- elife-00012-fig1-figsupp1-data1.csv
- elife-00012-fig1-figsupp2.tiff
- elife-00012-fig1-figsupp2-data1.csv
- elife-00012-fig1-figsupp3.tiff
- elife-00012-fig1-figsupp3-data1.mol
- elife-00012-fig2.tiff
- elife-00012-fig2-data1.txt
- elife-00012-fig3.tiff
- elife-00012-fig3-data.csv
- elife-00012-fig3-figsupp1.tiff
- elife-00012-fig3-figsupp1-data1.csv
- elife-00012-fig3-figsupp1-data2.csv
- elife-00012-fig3-figsupp1-data3.csv
- elife-00012-fig3-figsupp2.tiff
- elife-00012-fig3-figsupp2-data1.csv
- elife-00012-fig3-figsupp3.tiff
- elife-00012-fig3-figsupp3-data1.csv


###### code

Sometimes there is source code at a parent level, but sometimes assets will have source code files associated with them. These source code files are indicated by the presence of a `code` in the filename.

###### `<c-id>`

Assets can have multiple source code files associated with them, and these are distinguished with the
code id.

For example, an article with a top level source code, two main figures, where one figure has source code, and one figure has one figure supplement with source code:

- elife-00012-fig1.tiff
- elife-00012-fig1-code1.py
- elife-00012-fig1-code2.zip
- elife-00012-fig2.tiff
- elife-00012-fig2-figsupp1.tiff
- elife-00012-fig2-figsupp1-code1.zip
- elife-00012-code1.r

##### v`<version>`

When the article finally gets published, it gets assigned a version number for public consumption. These version numbers are incremented only when a new version of the article makes it to the published state on the website. The publishing system has to take on the job of checking on the current version number of any prior published versions of the article, and then appropriately incrementing the version number.

We propose that the publishing system should prepare files to send to the Drupal layer, with
the anticipated version number applied to the file names, and on a successful publishing event
that version of the article bundle is archived with the appropriate version number.

As examples, we might have the following situations:

###### example 1

Article makes it all the way from submission, through first round of content processing to being published, without a PoA version.

Bundle that appears in the publishing system looks like this:

elife-00012-vor-r1.zip contains:  
- elife-00012.xml
- elife-00012.pdf
- elife-00012-figures.pdf
- elife-00012-fig1.tiff
- elife-00012-fig1-data1.csv
- elife-00012-fig1-data2.csv
- elife-00012-fig1-figsupp1.tiff
- elife-00012-fig1-figsupp1-data1.csv
- elife-00012-fig1-figsupp2.tiff
- elife-00012-fig1-figsupp2-data1.csv
- elife-00012-fig1-figsupp3.tiff
- elife-00012-fig1-figsupp3-data1.mol
- elife-00012-fig2.tiff
- elife-00012-fig2-data1.txt
- elife-00012-fig3.tiff
- elife-00012-fig3-data.csv
- elife-00012-fig3-figsupp1.tiff
- elife-00012-fig3-figsupp1-data1.csv
- elife-00012-fig3-figsupp1-data2.csv
- elife-00012-fig3-figsupp1-data3.csv
- elife-00012-fig3-figsupp2.tiff
- elife-00012-fig3-figsupp2-data1.csv
- elife-00012-fig3-figsupp3.tiff
- elife-00012-fig3-figsupp3-data1.csv

Note: -r1 could be -r2, r3, r-n. This reflects production processes and is ignored by the publishing platform (with the exception of knowing which zip file to take from the production bucket when ready for publication).

On publishing event files and internal XML links get renamed and updated to (zip retains status indicator):

elife-00012-vor-v1.zip contains:  
- elife-00012-v1.xml
- elife-00012-v1.pdf
- elife-00012-figures-v1.pdf
- elife-00012-fig1-v1.tiff
- elife-00012-fig1-data1-v1.csv
- elife-00012-fig1-data2-v1.csv
- elife-00012-fig1-figsupp1-v1.tiff
- elife-00012-fig1-figsupp1-data1-v1.csv
- elife-00012-fig1-figsupp2-v1.tiff
- elife-00012-fig1-figsupp2-data1-v1.csv
- elife-00012-fig1-figsupp3-v1.tiff
- elife-00012-fig1-figsupp3-data1-v1.mol
- elife-00012-fig2-v1.tiff
- elife-00012-fig2-data1-v1.txt
- elife-00012-fig3-v1.tiff
- elife-00012-fig3-data-v1.csv
- elife-00012-fig3-figsupp1-v1.tiff
- elife-00012-fig3-figsupp1-data1-v1.csv
- elife-00012-fig3-figsupp1-data2-v1.csv
- elife-00012-fig3-figsupp1-data3-v1.csv
- elife-00012-fig3-figsupp2-v1.tiff
- elife-00012-fig3-figsupp2-data1-v1.csv
- elife-00012-fig3-figsupp3-v1.tiff
- elife-00012-fig3-figsupp3-data1-v1.csv

We have appended the version number to each file.

The following JSON is sent to the Drupal container (I've redacted specifics in the call to just highlight the components related to the article versions and identifiers)


```json
{
"force": "1",  
"title": " ... ",
"impact-statement": " ... ",  
"version": "1",
"doi": "10.7554/eLife.00012",
"publish": "1",
"volume": " ... ",
"article-id": "10.7554/eLife.00012",
"article-version-id": "00012.1",
"pub-date": "2014-02-28",
"path": "content/2/e00012",
"article-type": "research-article",
"status": "VOR",
"categories": {},
"keywords": {},
"contributors": [],
"referenced": {},
"related-articles": [],
"children": {},
"citations": {}  
}
```

On getting a success message from the Drupal layer that the publishing event has happened then the bundle gets archived under the zip file elife-00012-vor-v1.zip.


###### example 2

Production delivers an article twice to the Drupal site, and the second is the one that gets published.
The first version

#TODO: flesh out this example a bit better.

"Live" version of bundle that enters the publishing system is

elife-00012-vor-r4.zip contains:  
- elife-00012.xml
- elife-00012.pdf
- elife-00012-figures.pdf
- elife-00012-fig1.tiff
- elife-00012-fig1-data1.csv
- elife-00012-fig1-data2.csv
- elife-00012-fig1-figsupp1.tiff
- elife-00012-fig1-figsupp1-data1.csv
- elife-00012-fig1-figsupp2.tiff
- elife-00012-fig1-figsupp2-data1.csv
- elife-00012-fig1-figsupp3.tiff
- elife-00012-fig1-figsupp3-data1.mol
- elife-00012-fig2.tiff
- elife-00012-fig2-data1.txt
- elife-00012-fig3.tiff
- elife-00012-fig3-data.csv
- elife-00012-fig3-figsupp1.tiff
- elife-00012-fig3-figsupp1-data1.csv
- elife-00012-fig3-figsupp1-data2.csv
- elife-00012-fig3-figsupp1-data3.csv
- elife-00012-fig3-figsupp2.tiff
- elife-00012-fig3-figsupp2-data1.csv
- elife-00012-fig3-figsupp3.tiff
- elife-00012-fig3-figsupp3-data1.csv  

On publishing event files and internal XML links get renamed and updated to:

elife-00012-vor-v1.zip contains:  
- elife-00012-v1.xml
- elife-00012-v1.pdf
- elife-00012-figures-v1.pdf
- elife-00012-fig1-v1.tiff
- elife-00012-fig1-data1-v1.csv
- elife-00012-fig1-data2-v1.csv
- elife-00012-fig1-figsupp1-v1.tiff
- elife-00012-fig1-figsupp1-data1-v1.csv
- elife-00012-fig1-figsupp2-v1.tiff
- elife-00012-fig1-figsupp2-data1-v1.csv
- elife-00012-fig1-figsupp3-v1.tiff
- elife-00012-fig1-figsupp3-data1-v1.mol
- elife-00012-fig2-v1.tiff
- elife-00012-fig2-data1-v1.txt
- elife-00012-fig3-v1.tiff
- elife-00012-fig3-data-v1.csv
- elife-00012-fig3-figsupp1-v1.tiff
- elife-00012-fig3-figsupp1-data1-v1.csv
- elife-00012-fig3-figsupp1-data2-v1.csv
- elife-00012-fig3-figsupp1-data3-v1.csv
- elife-00012-fig3-figsupp2-v1.tiff
- elife-00012-fig3-figsupp2-data1-v1.csv
- elife-00012-fig3-figsupp3-v1.tiff
- elife-00012-fig3-figsupp3-data1-v1.csv

We have appended the version number to each file.

The following JSON is sent to the Drupal container (I've redacted specifics in the call to just highlight the components related to the article versions and identifiers)


```json
{
"force": "1",  
"title": " ... ",
"impact-statement": " ... ",  
"version": "1",
"doi": "10.7554/eLife.00012",
"publish": "1",
"volume": " ... ",
"article-id": "10.7554/eLife.00012",
"article-version-id": "00012.1",
"pub-date": "2014-02-28",
"path": "content/2/e00012",
"article-type": "research-article",
"status": "VOR",
"categories": {},
"keywords": {},
"contributors": [],
"referenced": {},
"related-articles": [],
"children": {},
"citations": {}  
}
```

On getting a success message from the Drupal layer that the publishing event has happened then the bundle gets archived under the zip file elife-00012-v1.zip.


###### example 3

A first version gets successfully published. Postpublication three revisions are needed to address
a tricky author issue, and the third revision makes it to version 2 on the website.

The version that exists in the archive and on the website is the following:

elife-00012-vor-v1.zip contains
- elife-00012-v1.xml
- elife-00012-v1.pdf
- elife-00012-figures-v1.pdf
- elife-00012-fig1-v1.tiff
- elife-00012-fig1-data1-v1.csv
- elife-00012-fig1-data2-v1.csv
- elife-00012-fig1-figsupp1-v1.tiff
- elife-00012-fig1-figsupp1-data1-v1.csv
- elife-00012-fig1-figsupp2-v1.tiff
- elife-00012-fig1-figsupp2-data1-v1.csv
- elife-00012-fig1-figsupp3-v1.tiff
- elife-00012-fig1-figsupp3-data1-v1.mol
- elife-00012-fig2-v1.tiff
- elife-00012-fig2-data1-v1.txt
- elife-00012-fig3-v1.tiff
- elife-00012-fig3-data-v1.csv
- elife-00012-fig3-figsupp1-v1.tiff
- elife-00012-fig3-figsupp1-data1-v1.csv
- elife-00012-fig3-figsupp1-data2-v1.csv
- elife-00012-fig3-figsupp1-data3-v1.csv
- elife-00012-fig3-figsupp2-v1.tiff
- elife-00012-fig3-figsupp2-data1-v1.csv
- elife-00012-fig3-figsupp3-v1.tiff
- elife-00012-fig3-figsupp3-data1-v1.csv

Three revisions occur, and the new "live" bundle that comes in to the publishing system contains the following:

elife-00012-vor-r6.zip contains:  
- elife-00012.xml
- elife-00012.pdf
- elife-00012-figures.pdf
- elife-00012-fig1.tiff
- elife-00012-fig1-data1.csv
- elife-00012-fig1-data2.csv
- elife-00012-fig1-figsupp1.tiff
- elife-00012-fig1-figsupp1-data1.csv
- elife-00012-fig1-figsupp2.tiff
- elife-00012-fig1-figsupp2-data1.csv
- elife-00012-fig1-figsupp3.tiff
- elife-00012-fig1-figsupp3-data1.mol
- elife-00012-fig2.tiff
- elife-00012-fig2-data1.txt
- elife-00012-fig3.tiff
- elife-00012-fig3-data.csv
- elife-00012-fig3-figsupp1.tiff
- elife-00012-fig3-figsupp1-data1.csv
- elife-00012-fig3-figsupp1-data2.csv
- elife-00012-fig3-figsupp1-data3.csv
- elife-00012-fig3-figsupp2.tiff
- elife-00012-fig3-figsupp2-data1.csv
- elife-00012-fig3-figsupp3.tiff
- elife-00012-fig3-figsupp3-data1.csv  

On publishing event files and internal XML links get renamed and updated to:

elife-00012-vor-v2.zip contains:
- elife-00012-v2.xml
- elife-00012-v2.pdf
- elife-00012-figures-v2.pdf
- elife-00012-fig1-v2.tiff
- elife-00012-fig1-data1-v2.csv
- elife-00012-fig1-data2-v2.csv
- elife-00012-fig1-figsupp1-v2.tiff
- elife-00012-fig1-figsupp1-data1-v2.csv
- elife-00012-fig1-figsupp2-v2.tiff
- elife-00012-fig1-figsupp2-data1-v2.csv
- elife-00012-fig1-figsupp3-v2.tiff
- elife-00012-fig1-figsupp3-data1-v2.mol
- elife-00012-fig2-v2.tiff
- elife-00012-fig2-data1-v2.txt
- elife-00012-fig3-v2.tiff
- elife-00012-fig3-data-v2.csv
- elife-00012-fig3-figsupp1-v2.tiff
- elife-00012-fig3-figsupp1-data1-v2.csv
- elife-00012-fig3-figsupp1-data2-v2.csv
- elife-00012-fig3-figsupp1-data3-v2.csv
- elife-00012-fig3-figsupp2-v2.tiff
- elife-00012-fig3-figsupp2-data1-v2.csv
- elife-00012-fig3-figsupp3-v2.tiff
- elife-00012-fig3-figsupp3-data1-v2.csv

The following JSON is sent to the Drupal container (I've redacted specifics in the call to just highlight the components related to the article versions and identifiers)

```json
{
"force": "1",  
"title": " ... ",
"impact-statement": " ... ",  
"version": "2",
"doi": "10.7554/eLife.00012",
"publish": "1",
"volume": " ... ",
"article-id": "10.7554/eLife.00012",
"article-version-id": "00012.2",
"pub-date": "2014-02-28",
"path": "content/2/e00012",
"article-type": "research-article",
"status": "VOR",
"categories": {},
"keywords": {},
"contributors": [],
"referenced": {},
"related-articles": [],
"children": {},
"citations": {}  
}
```

###### `<ext>``

This is the file extention, common extensions are

- zip
- pdf
- xml
- tiff
- csv
- xml
- py
- sql
- docx

### WTFAQs (Wait, These Fiddly Awkard Questions)


#### What happens when only a figure gets updated?

All files associated with an article get updated too. Although this means that we may end up
incrementing files that don't change, what is important is that on publication their file names
now refer to the globally updated version of the published article. This also means that
if we need a new file to replace an existing file, we do not run into file naming conflicts. From the point of view of the CDN we now refer to a new file with a new file name, rather than having to wait for a file replacement to propogate through the CDN, meaning these kinds of changes should happen instantaneiously.

#### How do we update a version number?

We check to see if any version are already published, and if they are, before
publishing, we prepare a new set of file names with the new version number. The
Drupal layer gets notified with a request to publish this new version, and on
reciept of success we allow the system to update it's records to indicate a
new version has been published.  

#### What paths need to be retained in the XML to assets?

Some components in the article XML will point to file assets. On creating a new version of
an article thse paths in the XML will need to get updated.

#### How do we update a revision number?

It is up to the content processor to handle revisions, and to send us the correctly
named new revision. Revision numbers do not affect the publishing platform.

#### How do we bootstrap a new instance of the site that respects all previous versioned published articles?

When we archive a package after successfully publishing, then we should archive all versions.
If we bootstrap a new version of the site we need to be able to utilize this archive to
be able to create a new version of the site. Ideally when sending an instruction to the
Drupal layer the publishing API will include indicators of the version that is currently
being published, and the url path on which these versions should be published.

If we loose our archive we will be unable to accurately recreate a previous state of our published
site, and we will have to do a best effort, and publish what we have using the lowest
 version numbers available to us at that time.

 We have an open question about where the date of published versions live. We don't have an answer to that yet.

#### Why are revision numbers not exposed on the final published version?

As revision numbers are no longer tracked in the system, there would be no need to expose them
in the final pubilshed version.


#### How do we update a `run` number in the production system?

Each time we receive a package from the content processor we may end up running an article
through the production system. If any steps in the system fall over we may need to
run the package through the system again. If the Drupal layer fails to publish
we may need to run the package through the system again rather than tracking these
production runs in any file names, these runs will be tracked internally by the production system.
This information will be made available on the production dashboard. Each time a package
comes through the production system, the number of times it has to run through
the production system will be tracked per package, along with whether that package
resulted in a published version. That means that for a given article - elife-01122 we may see the information similar to the following on a production dashboard

	- elife-01122 | POA | 9 runs | version 1  
	- elife-01122 | POA | 5 runs | version 2
	- elife-01122 | VOR | 1 runs | version 3
	- elife-01122 | VOR | 4 runs | version 4

#### Why don't we store run number information in the file name?

The first rule of run club, is that we don't talk about run club.  

#### Wait, are we really updating all the names of all the files if only one figure gets updated?

Yes, yes, we are really doing that.


#### Do we want to keep track of all the things that happen to a file before it hits the production system, and include a record of those things somehow in the file name?

At this point no.


#### Do we increment VOR version numbers if there was a POA version number before, or do we start over again with a new version number for the article, as it's name has changed to reflect the new status?

We increment the versions from PoA thorugh VoR  


#### How do we prevent an old packet of an article entering the publishing system, and creating a new published version?

In good funtimes news for the publishing platform, we have decided that this is the responsability of production. The publishing platform is going to implicity trust production, and will do as it's owers bid. We would like to enable a block in the production system on publishing any v2 or higher content, pending a production manual check, with the ability to remove this block at a later date.


#### The `"article-version-id": "00013.1",` now no longer contains any reference to "VOR", why is that?

The `"article-version-id": "00013.1",` is an id internal to the JSON that gets sent to the Drupal layer and is not part of the file naming convention.

The main requirement from the Drupal side is that articles can be sorted on the article-version-id, so the presence of a `VOR` or `POA` label in this id would require logic in the Drupal layer to
be able to correctly sort the article versions, as the app would have to know which of these
kinds of state of the came before which other kinds of state. If we drop this name in the id, then
the app does not have to carry this logic, and we make the API call to the Drupal layer
less eLife specific, meaning that in future this system could be more easily adopted
by other publishers, or used in other workflows that do not have POA or VOR in them.


#### In this document have you sneakilly concatenated the names of things like figures? Why, and do you have a full specification list?

I have, mainly as I felt that file names for sub components were becoming unweildy. Here is the start of a specification list

- figure -> fig
- figuresupplement -> figsupp
- supplementary file -> supp
- media (includes videos, audio and animation) -> media
- inline-media -> inf
- source code -> code  
- source data -> data
- figures (PDF if the figures) -> figures
- reporting standards -> repstand [note: not inu se as at October, 2015]
- decision letter file, for example figure -> dec-fig
- appendix asset file, for example figure (each appendix gets a unique number X) -> appX-fig
- author response asset file, for example figure -> resp-fig


## Tying POA and VOR packets in our workflow and their naming convention.


#### example 1

poa comes in and gets published immediately

package in the production system contains the following (after being generated
	via the POA process.)

elife-00012-poa.zip contains
- elife-00012-poa.xml  (not complete article XML)
- elife-00012-poa.pdf
- elife-00012-poa-supp.zip

On publication these get renamed to:

elife-00012-poa-v1.zip contains
- elife-00012-v1.xml
- elife-00012-v1.pdf
- elife-00012-supp-v1.zip

The following JSON is sent to the Drupal container

```json
{
"force": "1",  
"title": " ... ",
"impact-statement": " ... ",  
"version": "1",
"doi": "10.7554/eLife.00012",
"publish": "1",
"volume": " ... ",
"article-id": "10.7554/eLife.00012",
"article-version-id": "00012.1",
"pub-date": "2014-02-28",
"path": "content/2/e00012",
"article-type": "research-article",
"status": "POA",
"categories": {},
"keywords": {},
"contributors": [],
"referenced": {},
"related-articles": [],
"children": {},
"citations": {}  
}
```


An update is required on the POA articles and in the production system we receive

elife-00012-poa-r1.zip contains
- elife-00012-poa.xml  (not complete article XML)
- elife-00012-poa.pdf
- elife-00012-poa-supp.zip

On publication these get renamed to:

elife-00012-poa-v2.zip contains
- elife-00012-v2.xml  (not complete article XML)
- elife-00012-v2.pdf
- elife-00012-supp-v2.zip


The following JSON is sent to the Drupal container

```json
{
"force": "1",  
"title": " ... ",
"impact-statement": " ... ",  
"version": "2",
"doi": "10.7554/eLife.00012",
"publish": "1",
"volume": " ... ",
"article-id": "10.7554/eLife.00012",
"article-version-id": "00012.2",
"pub-date": "2014-03-02",
"path": "content/2/e00012",
"article-type": "research-article",
"status": "POA",
"categories": {},
"keywords": {},
"contributors": [],
"referenced": {},
"related-articles": [],
"children": {},
"citations": {}  
}
```

On publishing `elife-00012-poa-v2.zip` gets archived.

Later the article goes through the full content processing step and gets a VOR status.

Package comes in to the production system as:

elife-00012-vor-r4.zip contains
- elife-00012.xml
- elife-00012.pdf
- elife-00012-figures.pdf
- elife-00012-fig1.tiff
- elife-00012-fig1-data1.csv
- elife-00012-fig1-data2.csv
- elife-00012-fig1-figsupp1.tiff
- elife-00012-fig1-figsupp1-data1.csv
- elife-00012-fig1-figsupp2.tiff
- elife-00012-fig1-figsupp2-data1.csv
- elife-00012-fig1-figsupp3.tiff
- elife-00012-fig1-figsupp3-data1.mol
- elife-00012-fig2.tiff
- elife-00012-fig2-data1.txt
- elife-00012-fig3.tiff
- elife-00012-fig3-data.csv
- elife-00012-fig3-figsupp1.tiff
- elife-00012-fig3-figsupp1-data1.csv
- elife-00012-fig3-figsupp1-data2.csv
- elife-00012-fig3-figsupp1-data3.csv
- elife-00012-fig3-figsupp2.tiff
- elife-00012-fig3-figsupp2-data1.csv
- elife-00012-fig3-figsupp3.tiff
- elife-00012-fig3-figsupp3-data1.csv

no modifications are needed and on publishing these files get renamed as:

elife-00012-vor-v3.zip contains
- elife-00012-v3.xml
- elife-00012-v3.pdf
- elife-00012-figures-v3.pdf
- elife-00012-fig1-v3.tiff
- elife-00012-fig1-data1-v3.csv
- elife-00012-fig1-data2-v3.csv
- elife-00012-fig1-figsupp1-v3.tiff
- elife-00012-fig1-figsupp1-data1-v3.csv
- elife-00012-fig1-figsupp2-v3.tiff
- elife-00012-fig1-figsupp2-data1-v3.csv
- elife-00012-fig1-figsupp3-v3.tiff
- elife-00012-fig1-figsupp3-data1-v3.mol
- elife-00012-fig2-v3.tiff
- elife-00012-fig2-data1-v3.txt
- elife-00012-fig3-v3.tiff
- elife-00012-fig3-data-v3.csv
- elife-00012-fig3-figsupp1-v3.tiff
- elife-00012-fig3-figsupp1-data1-v3.csv
- elife-00012-fig3-figsupp1-data2-v3.csv
- elife-00012-fig3-figsupp1-data3-v3.csv
- elife-00012-fig3-figsupp2-v3.tiff
- elife-00012-fig3-figsupp2-data1-v3.csv
- elife-00012-fig3-figsupp3-v3.tiff
- elife-00012-fig3-figsupp3-data1-v3.csv

The following JSON is sent to the Drupal container  


```json
{
"force": "1",  
"title": " ... ",
"impact-statement": " ... ",  
"version": "3",
"doi": "10.7554/eLife.00012",
"publish": "1",
"volume": " ... ",
"article-id": "10.7554/eLife.00012",
"article-version-id": "00012.3",
"pub-date": "2014-03-15",
"path": "content/2/e00012",
"article-type": "research-article",
"status": "VOR",
"categories": {},
"keywords": {},
"contributors": [],
"referenced": {},
"related-articles": [],
"children": {},
"citations": {}  
}
```

And on successful publising `elife-00012-vor-v3.zip` gets archived.

So the version history of the PDF of this article will look like the following, from oldest to newest, for files have have been published

- elife-00012-v1.pdf  (a POA pdf)
- elife-00012-v2.pdf  (a POA pdf)
- elife-00012-v3.pdf  (a VOR pdf)
