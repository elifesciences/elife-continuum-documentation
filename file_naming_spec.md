# eLife file naming proposal 2015-05-28

## File naming pattern

>
	`elife-<eid>-<status>(-<asset><a-id>)(-<sub-asset><sa-id>)(-data<did>)((-r<revision>)|(-v<version>)).<ext>`

Brackets represent optional components. Pipe represents a choice on component, depending on state in the publishing system.


### components

###### `<eid>`

This is the eLife id, and is the numerical digit that is used to make up part of the DOI for an article. For example an eLife article with the following DOI `/10.7554/eLife.06659` will have an eid of `06659`.

###### `<status>`

This is either `poa` (publish on accept) or `vor` (version of record).

###### `<asset>`

This refers to an asset file related to an article, for example a figure, sub-figure, data file, media, or supplementary file.

###### `<a-id>`

The `a-id` is the asset id, and indicates the order of an asset in the article. For example an
article with three figures will have the following asset files:

- elife-00012-vor-fig1.tiff
- elife-00012-vor-fig2.tiff
- elife-00012-vor-fig3.tiff

###### `<sub-asset>`

Some assets will have sub-assets, and these are indicated by the sub-asset component.

###### `<sa-id>`

Some assets have sub-asset ids, for example, an aritcle with three main figures, where one
figure has three sub figures, and one figure has two sub figures will have the following:

- elife-00012-vor-fig1.tiff
- elife-00012-vor-fig1-subfig1.tiff
- elife-00012-vor-fig1-subfig2.tiff
- elife-00012-vor-fig1-subfig3.tiff
- elife-00012-vor-fig2.tiff
- elife-00012-vor-fig3.tiff
- elife-00012-vor-fig3-subfig1.tiff
- elife-00012-vor-fig3-subfig2.tiff
- elife-00012-vor-fig3-subfig3.tiff

###### data

Some assets will have data files associated with them. These data files are indicated by the
presence of a `data` in the filename.

###### `<d-id>`

Assets can have multiple data files associated with them, and these are distinguished with the
data id.

For example, an article with three main figures, where one figure has three sub figures, and one figure has two sub figures, and all have associated data with some of them having multiple data files, could have the following:

- elife-00012-vor-fig1.tiff
- elife-00012-vor-fig1-data1.csv
- elife-00012-vor-fig1-data2.csv
- elife-00012-vor-fig1-subfig1.tiff
- elife-00012-vor-fig1-subfig1-data1.csv
- elife-00012-vor-fig1-subfig2.tiff
- elife-00012-vor-fig1-subfig2-data1.csv
- elife-00012-vor-fig1-subfig3.tiff
- elife-00012-vor-fig1-subfig3-data1.mol
- elife-00012-vor-fig2.tiff
- elife-00012-vor-fig2-data1.txt
- elife-00012-vor-fig3.tiff
- elife-00012-vor-fig3-data.csv
- elife-00012-vor-fig3-subfig1.tiff
- elife-00012-vor-fig3-subfig1-data1.csv
- elife-00012-vor-fig3-subfig1-data2.csv
- elife-00012-vor-fig3-subfig1-data3.csv
- elife-00012-vor-fig3-subfig2.tiff
- elife-00012-vor-fig3-subfig3-data1.csv
- elife-00012-vor-fig3-subfig3.tiff
- elife-00012-vor-fig3-subfig3-data1.csv


###### r `<revision>`

Before reaching the publishing workflow an article may go through a number of revisions at any one of a number of steps with the content processor. We indicate updates to the article with a revision number. If no revisions have happened, there will be no revision number on the article. Each further revision is indicated by a revision number. The revision number will also increment for each asset of the article.

For example, if one image needs to be updated within an article, the revision number increases for all files associated with the article. If a change is needed in the xml of the article, the revision number increments for all files assocaited with the article.

Inital content of an article zip file, with no revisions having occurred

- elife-00012-vor.xml
- elife-00012-vor.pdf
- elife-00012-vor-figures.pdf
- elife-00012-vor-fig1.tiff
- elife-00012-vor-fig1-data1.csv
- elife-00012-vor-fig1-data2.csv
- elife-00012-vor-fig1-subfig1.tiff
- elife-00012-vor-fig1-subfig1-data1.csv
- elife-00012-vor-fig1-subfig2.tiff
- elife-00012-vor-fig1-subfig2-data1.csv
- elife-00012-vor-fig1-subfig3.tiff
- elife-00012-vor-fig1-subfig3-data1.mol
- elife-00012-vor-fig2.tiff
- elife-00012-vor-fig2-data1.txt
- elife-00012-vor-fig3.tiff
- elife-00012-vor-fig3-data.csv
- elife-00012-vor-fig3-subfig1.tiff
- elife-00012-vor-fig3-subfig1-data1.csv
- elife-00012-vor-fig3-subfig1-data2.csv
- elife-00012-vor-fig3-subfig1-data3.csv
- elife-00012-vor-fig3-subfig2.tiff
- elife-00012-vor-fig3-subfig3-data1.csv
- elife-00012-vor-fig3-subfig3.tiff
- elife-00012-vor-fig3-subfig3-data1.csv

One revision occurring in the content processing stage, requireing a resupply to the publishing system:

- elife-00012-vor-r1.xml
- elife-00012-vor-r1.pdf
- elife-00012-vor-figures-r1.pdf
- elife-00012-vor-fig1-r1.tiff
- elife-00012-vor-fig1-data1-r1.csv
- elife-00012-vor-fig1-data2-r1.csv
- elife-00012-vor-fig1-subfig1-r1.tiff
- elife-00012-vor-fig1-subfig1-data1-r1.csv
- elife-00012-vor-fig1-subfig2-r1.tiff
- elife-00012-vor-fig1-subfig2-data1-r1.csv
- elife-00012-vor-fig1-subfig3-r1.tiff
- elife-00012-vor-fig1-subfig3-data1-r1.mol
- elife-00012-vor-fig2-r1.tiff
- elife-00012-vor-fig2-data1-r1.txt
- elife-00012-vor-fig3-r1.tiff
- elife-00012-vor-fig3-data-r1.csv
- elife-00012-vor-fig3-subfig1-r1.tiff
- elife-00012-vor-fig3-subfig1-data1-r1.csv
- elife-00012-vor-fig3-subfig1-data2-r1.csv
- elife-00012-vor-fig3-subfig1-data3-r1.csv
- elife-00012-vor-fig3-subfig2-r1.tiff
- elife-00012-vor-fig3-subfig3-data1-r1.csv
- elife-00012-vor-fig3-subfig3-r1.tiff
- elife-00012-vor-fig3-subfig3-data1-r1.csv

5 revisions having occurred:

- elife-00012-vor-r5.xml
- elife-00012-vor-r5.pdf
- elife-00012-vor-figures-r5.pdf
- elife-00012-vor-fig1-r5.tiff
- elife-00012-vor-fig1-data1-r5.csv
- elife-00012-vor-fig1-data2-r5.csv
- elife-00012-vor-fig1-subfig1-r5.tiff
- elife-00012-vor-fig1-subfig1-data1-r5.csv
- elife-00012-vor-fig1-subfig2-r5.tiff
- elife-00012-vor-fig1-subfig2-data1-r5.csv
- elife-00012-vor-fig1-subfig3-r5.tiff
- elife-00012-vor-fig1-subfig3-data1-r5.mol
- elife-00012-vor-fig2-r5.tiff
- elife-00012-vor-fig2-data1-r5.txt
- elife-00012-vor-fig3-r5.tiff
- elife-00012-vor-fig3-data-r5.csv
- elife-00012-vor-fig3-subfig1-r5.tiff
- elife-00012-vor-fig3-subfig1-data1-r5.csv
- elife-00012-vor-fig3-subfig1-data2-r5.csv
- elife-00012-vor-fig3-subfig1-data3-r5.csv
- elife-00012-vor-fig3-subfig2-r5.tiff
- elife-00012-vor-fig3-subfig3-data1-r5.csv
- elife-00012-vor-fig3-subfig3-r5.tiff
- elife-00012-vor-fig3-subfig3-data1-r5.csv


##### v`<version>`

When the article finally gets published, it gets assigned a version number for public consumption. These version numbers are incremented only when a new version of the article makes it to the published state on the website. The publishing system has to take on the job
of checking on the current version number of any prior published versions of the article, and then appropriately incrementing the version number. Unlike with revision numbers, as soon as an article is published it gets a version v1, whereas revisions only get a revision
number when there is a change to the originally submitted manuscript.

We propose that the publishing system should prepare files to send to the Drupal layer, with
the anticipated version number applied to the file names, and on a successful publihsing event
that version of the article bundle is archived with the appropriate version number.

In this process revision numbers get stripped from the public version of the article, as we do
not want to expose revision numbers.

As examples, we might have the following situations:

###### example 1

Article makes it all the way from submission, through first round of content processing to being published.

Bundle that appears in the publishing system looks like this:

- elife-00012-vor.xml
- elife-00012-vor.pdf
- elife-00012-vor-figures.pdf
- elife-00012-vor-fig1.tiff
- elife-00012-vor-fig1-data1.csv
- elife-00012-vor-fig1-data2.csv
- elife-00012-vor-fig1-subfig1.tiff
- elife-00012-vor-fig1-subfig1-data1.csv
- elife-00012-vor-fig1-subfig2.tiff
- elife-00012-vor-fig1-subfig2-data1.csv
- elife-00012-vor-fig1-subfig3.tiff
- elife-00012-vor-fig1-subfig3-data1.mol
- elife-00012-vor-fig2.tiff
- elife-00012-vor-fig2-data1.txt
- elife-00012-vor-fig3.tiff
- elife-00012-vor-fig3-data.csv
- elife-00012-vor-fig3-subfig1.tiff
- elife-00012-vor-fig3-subfig1-data1.csv
- elife-00012-vor-fig3-subfig1-data2.csv
- elife-00012-vor-fig3-subfig1-data3.csv
- elife-00012-vor-fig3-subfig2.tiff
- elife-00012-vor-fig3-subfig3-data1.csv
- elife-00012-vor-fig3-subfig3.tiff
- elife-00012-vor-fig3-subfig3-data1.csv

On publishing event files and internal XML links get renamed and updated to:

- elife-00012-vor-v1.xml
- elife-00012-vor-v1.pdf
- elife-00012-vor-figures-v1.pdf
- elife-00012-vor-fig1-v1.tiff
- elife-00012-vor-fig1-data1-v1.csv
- elife-00012-vor-fig1-data2-v1.csv
- elife-00012-vor-fig1-subfig1-v1.tiff
- elife-00012-vor-fig1-subfig1-data1-v1.csv
- elife-00012-vor-fig1-subfig2-v1.tiff
- elife-00012-vor-fig1-subfig2-data1-v1.csv
- elife-00012-vor-fig1-subfig3-v1.tiff
- elife-00012-vor-fig1-subfig3-data1-v1.mol
- elife-00012-vor-fig2-v1.tiff
- elife-00012-vor-fig2-data1-v1.txt
- elife-00012-vor-fig3-v1.tiff
- elife-00012-vor-fig3-data-v1.csv
- elife-00012-vor-fig3-subfig1-v1.tiff
- elife-00012-vor-fig3-subfig1-data1-v1.csv
- elife-00012-vor-fig3-subfig1-data2-v1.csv
- elife-00012-vor-fig3-subfig1-data3-v1.csv
- elife-00012-vor-fig3-subfig2-v1.tiff
- elife-00012-vor-fig3-subfig3-data1-v1.csv
- elife-00012-vor-fig3-subfig3-v1.tiff
- elife-00012-vor-fig3-subfig3-data1-v1.csv

Bundle gets archived.

###### example 2

One revision comes in before article gets published to the Drupal site, and that revision is the revision that gets published.

"Live" version of bundle that enters the publishing system is

- elife-00012-vor-r1.xml
- elife-00012-vor-r1.pdf
- elife-00012-vor-figures-r1.pdf
- elife-00012-vor-fig1-r1.tiff
- elife-00012-vor-fig1-data1-r1.csv
- elife-00012-vor-fig1-data2-r1.csv
- elife-00012-vor-fig1-subfig1-r1.tiff
- elife-00012-vor-fig1-subfig1-data1-r1.csv
- elife-00012-vor-fig1-subfig2-r1.tiff
- elife-00012-vor-fig1-subfig2-data1-r1.csv
- elife-00012-vor-fig1-subfig3-r1.tiff
- elife-00012-vor-fig1-subfig3-data1-r1.mol
- elife-00012-vor-fig2-r1.tiff
- elife-00012-vor-fig2-data1-r1.txt
- elife-00012-vor-fig3-r1.tiff
- elife-00012-vor-fig3-data-r1.csv
- elife-00012-vor-fig3-subfig1-r1.tiff
- elife-00012-vor-fig3-subfig1-data1-r1.csv
- elife-00012-vor-fig3-subfig1-data2-r1.csv
- elife-00012-vor-fig3-subfig1-data3-r1.csv
- elife-00012-vor-fig3-subfig2-r1.tiff
- elife-00012-vor-fig3-subfig3-data1-r1.csv
- elife-00012-vor-fig3-subfig3-r1.tiff
- elife-00012-vor-fig3-subfig3-data1-r1.csv

On publishing event files and internal XML links get renamed and updated to:

- elife-00012-vor-v1.xml
- elife-00012-vor-v1.pdf
- elife-00012-vor-figures-v1.pdf
- elife-00012-vor-fig1-v1.tiff
- elife-00012-vor-fig1-data1-v1.csv
- elife-00012-vor-fig1-data2-v1.csv
- elife-00012-vor-fig1-subfig1-v1.tiff
- elife-00012-vor-fig1-subfig1-data1-v1.csv
- elife-00012-vor-fig1-subfig2-v1.tiff
- elife-00012-vor-fig1-subfig2-data1-v1.csv
- elife-00012-vor-fig1-subfig3-v1.tiff
- elife-00012-vor-fig1-subfig3-data1-v1.mol
- elife-00012-vor-fig2-v1.tiff
- elife-00012-vor-fig2-data1-v1.txt
- elife-00012-vor-fig3-v1.tiff
- elife-00012-vor-fig3-data-v1.csv
- elife-00012-vor-fig3-subfig1-v1.tiff
- elife-00012-vor-fig3-subfig1-data1-v1.csv
- elife-00012-vor-fig3-subfig1-data2-v1.csv
- elife-00012-vor-fig3-subfig1-data3-v1.csv
- elife-00012-vor-fig3-subfig2-v1.tiff
- elife-00012-vor-fig3-subfig3-data1-v1.csv
- elife-00012-vor-fig3-subfig3-v1.tiff
- elife-00012-vor-fig3-subfig3-data1-v1.csv

This version gets archived.

###### example 3

A first version gets successfully published, but three revisions are needed to address
a tricky author issue, and this third revision makes it to version 2 on the website.

The version that exists in the archive and on the website is the following:

- elife-00012-vor-v1.xml
- elife-00012-vor-v1.pdf
- elife-00012-vor-figures-v1.pdf
- elife-00012-vor-fig1-v1.tiff
- elife-00012-vor-fig1-data1-v1.csv
- elife-00012-vor-fig1-data2-v1.csv
- elife-00012-vor-fig1-subfig1-v1.tiff
- elife-00012-vor-fig1-subfig1-data1-v1.csv
- elife-00012-vor-fig1-subfig2-v1.tiff
- elife-00012-vor-fig1-subfig2-data1-v1.csv
- elife-00012-vor-fig1-subfig3-v1.tiff
- elife-00012-vor-fig1-subfig3-data1-v1.mol
- elife-00012-vor-fig2-v1.tiff
- elife-00012-vor-fig2-data1-v1.txt
- elife-00012-vor-fig3-v1.tiff
- elife-00012-vor-fig3-data-v1.csv
- elife-00012-vor-fig3-subfig1-v1.tiff
- elife-00012-vor-fig3-subfig1-data1-v1.csv
- elife-00012-vor-fig3-subfig1-data2-v1.csv
- elife-00012-vor-fig3-subfig1-data3-v1.csv
- elife-00012-vor-fig3-subfig2-v1.tiff
- elife-00012-vor-fig3-subfig3-data1-v1.csv
- elife-00012-vor-fig3-subfig3-v1.tiff
- elife-00012-vor-fig3-subfig3-data1-v1.csv

Three revisions occur, and the new "live" bundle that comes in to the publsihing system contains the following:

- elife-00012-vor-r3.xml
- elife-00012-vor-r3.pdf
- elife-00012-vor-figures-r3.pdf
- elife-00012-vor-fig1-r3.tiff
- elife-00012-vor-fig1-data1-r3.csv
- elife-00012-vor-fig1-data2-r3.csv
- elife-00012-vor-fig1-subfig1-r3.tiff
- elife-00012-vor-fig1-subfig1-data1-r3.csv
- elife-00012-vor-fig1-subfig2-r3.tiff
- elife-00012-vor-fig1-subfig2-data1-r3.csv
- elife-00012-vor-fig1-subfig3-r3.tiff
- elife-00012-vor-fig1-subfig3-data1-r3.mol
- elife-00012-vor-fig2-r3.tiff
- elife-00012-vor-fig2-data1-r3.txt
- elife-00012-vor-fig3-r3.tiff
- elife-00012-vor-fig3-data-r3.csv
- elife-00012-vor-fig3-subfig1-r3.tiff
- elife-00012-vor-fig3-subfig1-data1-r3.csv
- elife-00012-vor-fig3-subfig1-data2-r3.csv
- elife-00012-vor-fig3-subfig1-data3-r3.csv
- elife-00012-vor-fig3-subfig2-r3.tiff
- elife-00012-vor-fig3-subfig3-data1-r3.csv
- elife-00012-vor-fig3-subfig3-r3.tiff
- elife-00012-vor-fig3-subfig3-data1-r3.csv

On publishing event files and internal XML links get renamed and updated to:

- elife-00012-vor-v2.xml
- elife-00012-vor-v2.pdf
- elife-00012-vor-figures-v2.pdf
- elife-00012-vor-fig1-v2.tiff
- elife-00012-vor-fig1-data1-v2.csv
- elife-00012-vor-fig1-data2-v2.csv
- elife-00012-vor-fig1-subfig1-v2.tiff
- elife-00012-vor-fig1-subfig1-data1-v2.csv
- elife-00012-vor-fig1-subfig2-v2.tiff
- elife-00012-vor-fig1-subfig2-data1-v2.csv
- elife-00012-vor-fig1-subfig3-v2.tiff
- elife-00012-vor-fig1-subfig3-data1-v2.mol
- elife-00012-vor-fig2-v2.tiff
- elife-00012-vor-fig2-data1-v2.txt
- elife-00012-vor-fig3-v2.tiff
- elife-00012-vor-fig3-data-v2.csv
- elife-00012-vor-fig3-subfig1-v2.tiff
- elife-00012-vor-fig3-subfig1-data1-v2.csv
- elife-00012-vor-fig3-subfig1-data2-v2.csv
- elife-00012-vor-fig3-subfig1-data3-v2.csv
- elife-00012-vor-fig3-subfig2-v2.tiff
- elife-00012-vor-fig3-subfig3-data1-v2.csv
- elife-00012-vor-fig3-subfig3-v2.tiff
- elife-00012-vor-fig3-subfig3-data1-v2.csv

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

All files associated with an article get updated too, either the revision number, or
the eventual published version number. Although this means that we may end up
incrementing files that don't change, what is important is that their file names
now refer to the globally updated version of the published article.

#### How do we update a version number?

We check to see if any version are already published, and if they are, before
publishing, we prepare a new set of file names with the new version number. The
Drupal layer gets notified with a request to publish this new version, and on
reciept of success we allow the system to update it's records to indicate a
new version has been published.  

#### What paths needs to be retained in the XML to assetts?

Some components in the aritcle XML will point to file assetts. On creating a new version of
an article thse paths in the XML will need to get updated.

#### How do we update a revision number?

It is up to the content processor to handle revisions, and to send us the correctly
named new revision.

#### How do we bootstrap a new instance of the site that respects all previous versioned published articles?

When we archive a package after successfully publishing, then we should archive all versions.
If we bootstrap a new version of the site we need to be able to utilize this archive to
be able to create a new version of the site. Ideally when sending an instruction to the
Drupal layer the publishing API will include indicators of the version that is currently
being published, and the url path on which these versions should be published.

If we loose our archive we will be unable to accurately recreate a previous state of our published
site, and we will have to do a best effort, and publish what we have using the lowest
 version numbers available to us at that time.

#### Why are revision numbers not exposed on the final published version?

If we expose revision numbers on the final published version then we can end up with
situations in which the revision number is greater than the version number, the version number
is greater than the revision number, or situations in which they are the same. This is considered
a bad user and developer experience, and rather than revealing this information we have decided that this map needs to be maintained at the metadata level. Ultimately the only business critical information is how many version have been made publicly available, and what are they?

#### How do we update a `run` number in the production system?

Each time we receive a package from the content processor we may end up running an article
through the production system. If any steps in the system fall over we may need to
run the package through the system again. If the Drupal layer fails to publish
we may need to run the package through the system again Rather than tracking these
production runs in any file names, these runs will be tracked internally by the production system.
This informaion will be made avaialle on the production dashboard. Each time a package
comes through the production system, the number of times it has to run through
the production system will be tacked per package, along with whether that package
resulted in a published version. That means that for a given article - elife-01122 we may see the  information similar to the following on a production dashboard

	- elife-01122 | POA | revision 0 | 6 runs | not published  
	- elife-01122 | POA | revision 1 | 3 runs | version 1
	- elife-01122 | POA | revision 2 | 3 runs | not published
	- elife-01122 | POA | revision 3 | 2 runs | version 2
	- elife-01122 | VOR | revision 0 | 2 runs | not published  
	- elife-01122 | VOR | revision 1 | 1 runs | version 1
	- elife-01122 | VOR | revision 2 | 4 runs | version 2

#### Why don't we store run number information in the file name?

The first rule of run club, is that we don't talk about run club.  

#### Wait, are we really updating all the names of all the files if only one figure gets updated?

Yes, yes, we are really doing that.


#### Do we want to keep track of all the things that happen to a file before it hits the production system, and include a record of those things somehow in the file name?

At this point no.


#### Do we increment VOR version numbers if there was a POA version number before, or do we start over again with a new version number for the article, as it's name has changed to reflect the new status?

We start again, I've included even more examples below.  


#### How do we prevent an old packet of an article entering the publishing system, and creating a new published version?

If the content processor screws up and sends a copy of an already submitted package into the
production system, but for some godforsaken reason increments the revision number by one,
then this has the potential to run through the production system and create a newly published
version of the article that is actually not different from previously published versions
of the article.

We could either, not care about this, or we could put in place some roadblack to publishing
provably similar content again. At this point my recommendation is to not care about this.

If the content processor sends in a copy of a revision that we have already seen before we could
end up publsing a new version of the article that is actually a copy of an older crappier
version of the article. We could either not care, or we could put in place some block
to prevent revisions entering the production system again that have already resulted in a
successful publising event. I think we might want to consider this story.

#### In this document have you sneakilly concatenated the names of things like figures? Why, and do you have a full specification list?

I have, mainly as I felt that file names for sub components were becoming unweildy. Here is the start of a specification list

- figure -> fig
- table -> table  (tab is ambigious)
- figuresupplement -> subfig
- supplementaryfile -> suppfile
- media -> media
- sourcecode -> code  
- sourcedata -> data  
- supplimentarymaterial ->


## Tying POA and VOR packets in our workflow and their naming convention.


#### example 1

poa come in and gets published immediately

package in the production system contains the following (after being generated
	via the POA process.)

- elife-00012-poa.xml  (not complete article XML)
- elife-00012-poa.pdf
- elife-00012-poa-suppfiles.zip

On publication these get renamed to:

- elife-00012-poa-v1.xml
- elife-00012-poa-v1.pdf
- elife-00012-poa-suppfiles-v1.zip

An update is required on the POA articles and in the production system we recieve

- elife-00012-poa-r1.xml  (not complete article XML)
- elife-00012-poa-r1.pdf
- elife-00012-poa-suppfiles-r1.zip

On publication these get renamed to:

- elife-00012-poa-v2.xml  (not complete article XML)
- elife-00012-poa-v2.pdf
- elife-00012-poa-suppfiles-v2.zip

The article goes through the full content processing step and gets a VOR status.

Package comes in to the production system as:

- elife-00012-vor.xml
- elife-00012-vor.pdf
- elife-00012-vor-figures.pdf
- elife-00012-vor-fig1.tiff
- elife-00012-vor-fig1-data1.csv
- elife-00012-vor-fig1-data2.csv
- elife-00012-vor-fig1-subfig1.tiff
- elife-00012-vor-fig1-subfig1-data1.csv
- elife-00012-vor-fig1-subfig2.tiff
- elife-00012-vor-fig1-subfig2-data1.csv
- elife-00012-vor-fig1-subfig3.tiff
- elife-00012-vor-fig1-subfig3-data1.mol
- elife-00012-vor-fig2.tiff
- elife-00012-vor-fig2-data1.txt
- elife-00012-vor-fig3.tiff
- elife-00012-vor-fig3-data.csv
- elife-00012-vor-fig3-subfig1.tiff
- elife-00012-vor-fig3-subfig1-data1.csv
- elife-00012-vor-fig3-subfig1-data2.csv
- elife-00012-vor-fig3-subfig1-data3.csv
- elife-00012-vor-fig3-subfig2.tiff
- elife-00012-vor-fig3-subfig3-data1.csv
- elife-00012-vor-fig3-subfig3.tiff
- elife-00012-vor-fig3-subfig3-data1.csv

no modifications are needed and this gets published as:

- elife-00012-vor-v1.xml
- elife-00012-vor-v1.pdf
- elife-00012-vor-figures-v1.pdf
- elife-00012-vor-fig1-v1.tiff
- elife-00012-vor-fig1-data1-v1.csv
- elife-00012-vor-fig1-data2-v1.csv
- elife-00012-vor-fig1-subfig1-v1.tiff
- elife-00012-vor-fig1-subfig1-data1-v1.csv
- elife-00012-vor-fig1-subfig2-v1.tiff
- elife-00012-vor-fig1-subfig2-data1-v1.csv
- elife-00012-vor-fig1-subfig3-v1.tiff
- elife-00012-vor-fig1-subfig3-data1-v1.mol
- elife-00012-vor-fig2-v1.tiff
- elife-00012-vor-fig2-data1-v1.txt
- elife-00012-vor-fig3-v1.tiff
- elife-00012-vor-fig3-data-v1.csv
- elife-00012-vor-fig3-subfig1-v1.tiff
- elife-00012-vor-fig3-subfig1-data1-v1.csv
- elife-00012-vor-fig3-subfig1-data2-v1.csv
- elife-00012-vor-fig3-subfig1-data3-v1.csv
- elife-00012-vor-fig3-subfig2-v1.tiff
- elife-00012-vor-fig3-subfig3-data1-v1.csv
- elife-00012-vor-fig3-subfig3-v1.tiff
- elife-00012-vor-fig3-subfig3-data1-v1.csv

So the version hisotry of the PDF of this article will look like the following, from oldest to newest:

- elife-00012-poa-v1.pdf
- elife-00012-poa-v2.pdf
- elife-00012-vor-v1.pdf
