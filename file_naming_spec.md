# eLife file naming proposal 2015-05-28

## File naming pattern

>
	elife-<eid>-<status>(-<asset><a-id>)(-<sub-asset><sa-id>)(-data<did>)((-r<revision>)|(-v<version>)).<ext>

Brackets represent optional components. Pipe represents a choice on component, depending on state in the publishing system.


### components

###### `<eid>`

This is the eLife id, and is the numerical digit that is used to make up part of the DOI for an article. For example an eLife article with the following DOI `/10.7554/eLife.06659` will have an eid of `06659`.

###### `<status>`

This is either `poa` (publish on accept) or `vor` (version of record).

###### `<asset>`

This refers to an asset file related to an article, for example a figure, sub-figure, data file, video or supplimentary file.

###### `<a-id>`

The `a-id` is the asset id, and idicates the order of an asset in the article. For example an
article with three figures will have the following asset files:

- elife-00012-vor-fig1.tiff
- elife-00012-vor-fig2.tiff
- elife-00012-vor-fig3.tiff

###### `<sub-asset>`

Some assets will have sub-assets, and these are indicated by the sub-asset component.

###### `<sa-id>`

Sume assets have sub-asset ids, for example, an aritcle with three main figures, where one
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

For example, an aritcle with three main figures, where one figure has three sub figures, and one figure has two sub figures, and all have associated data with some of them having multiple data files, could have the following:

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

Before reaching the publishing workflow an article may go through a number of revisions at any one of a number of steps with the content processor. We indicate updates to the article with a revision number. If no revisions have happened, there will be no revision number on the article. Each further revision is indicated by a revision number. The revision number will increment for each asset of the article, in addition to the article, so for example we might have:

inital content of an article zip file, with no revisions having occured

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

One revision occuring in the content processing stage, requireing a resupply to the publishing system:

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

5 revisions having occured:

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
of chcking on the current version number of any prior published versions of the article, and then appropriatly incrementing the version number. Unlike with revision numbers, as soon as an article is publised it gets a version v1, wheras revisions only get a revision
number when there is a change to the originally submitted manuscript.

We propose that the publishing system should prepare files to send to the Drupal layer, with
the anticipated version number applied to the file names, and on a successful publihsing event
that version of the article bundle is archived with the approriate version number.

In this process revision numbers get stripped from the public version of the article, as we do
not want to expose revision numbers. 

If something fails in the publishing event that instance of version naming for that revision bundle may need to be scrapped, as between when the publishing event failed, and when a retry is about to occur, a new revision may enter the system, invalidating the last revision that was to be pushed into a published state.

As examples, we might have the following situations:

Article makes it all the way from submission, through first round of content processing to being published.

###### example 1

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

- elife-00012-vor-r1-v1.xml
- elife-00012-vor-r1-v1.pdf
- elife-00012-vor-figures-r1-v1.pdf
- elife-00012-vor-fig1-r1-v1.tiff
- elife-00012-vor-fig1-data1-r1-v1.csv
- elife-00012-vor-fig1-data2-r1-v1.csv
- elife-00012-vor-fig1-subfig1-r1-v1.tiff
- elife-00012-vor-fig1-subfig1-data1-r1-v1.csv
- elife-00012-vor-fig1-subfig2-r1-v1.tiff
- elife-00012-vor-fig1-subfig2-data1-r1-v1.csv
- elife-00012-vor-fig1-subfig3-r1-v1.tiff
- elife-00012-vor-fig1-subfig3-data1-r1-v1.mol
- elife-00012-vor-fig2-r1-v1.tiff
- elife-00012-vor-fig2-data1-r1-v1.txt
- elife-00012-vor-fig3-r1-v1.tiff
- elife-00012-vor-fig3-data-r1-v1.csv
- elife-00012-vor-fig3-subfig1-r1-v1.tiff
- elife-00012-vor-fig3-subfig1-data1-r1-v1.csv
- elife-00012-vor-fig3-subfig1-data2-r1-v1.csv
- elife-00012-vor-fig3-subfig1-data3-r1-v1.csv
- elife-00012-vor-fig3-subfig2-r1-v1.tiff
- elife-00012-vor-fig3-subfig3-data1-r1-v1.csv
- elife-00012-vor-fig3-subfig3-r1-v1.tiff
- elife-00012-vor-fig3-subfig3-data1-r1-v1.csv

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

- elife-00012-vor-r3-v2.xml
- elife-00012-vor-r3-v2.pdf
- elife-00012-vor-figures-r3-v2.pdf
- elife-00012-vor-fig1-r3-v2.tiff
- elife-00012-vor-fig1-data1-r3-v2.csv
- elife-00012-vor-fig1-data2-r3-v2.csv
- elife-00012-vor-fig1-subfig1-r3-v2.tiff
- elife-00012-vor-fig1-subfig1-data1-r3-v2.csv
- elife-00012-vor-fig1-subfig2-r3-v2.tiff
- elife-00012-vor-fig1-subfig2-data1-r3-v2.csv
- elife-00012-vor-fig1-subfig3-r3-v2.tiff
- elife-00012-vor-fig1-subfig3-data1-r3-v2.mol
- elife-00012-vor-fig2-r3-v2.tiff
- elife-00012-vor-fig2-data1-r3-v2.txt
- elife-00012-vor-fig3-r3-v2.tiff
- elife-00012-vor-fig3-data-r3-v2.csv
- elife-00012-vor-fig3-subfig1-r3-v2.tiff
- elife-00012-vor-fig3-subfig1-data1-r3-v2.csv
- elife-00012-vor-fig3-subfig1-data2-r3-v2.csv
- elife-00012-vor-fig3-subfig1-data3-r3-v2.csv
- elife-00012-vor-fig3-subfig2-r3-v2.tiff
- elife-00012-vor-fig3-subfig3-data1-r3-v2.csv
- elife-00012-vor-fig3-subfig3-r3-v2.tiff
- elife-00012-vor-fig3-subfig3-data1-r3-v2.csv

###### example 4

An inital successful clean run happens on publishing to create a v1 with no revisions. One revision comes in, and gets pushed straight to the website, causing the version number of the public artifact to be incremented by one.

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

One revision occurs and the "live" bundle that enters the publising system becomes

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

On publishing event files get renamed, and XML links updated to

- elife-00012-vor-r1-v2.xml
- elife-00012-vor-r1-v2.pdf
- elife-00012-vor-figures-r1-v2.pdf
- elife-00012-vor-fig1-r1-v2.tiff
- elife-00012-vor-fig1-data1-r1-v2.csv
- elife-00012-vor-fig1-data2-r1-v2.csv
- elife-00012-vor-fig1-subfig1-r1-v2.tiff
- elife-00012-vor-fig1-subfig1-data1-r1-v2.csv
- elife-00012-vor-fig1-subfig2-r1-v2.tiff
- elife-00012-vor-fig1-subfig2-data1-r1-v2.csv
- elife-00012-vor-fig1-subfig3-r1-v2.tiff
- elife-00012-vor-fig1-subfig3-data1-r1-v2.mol
- elife-00012-vor-fig2-r1-v2.tiff
- elife-00012-vor-fig2-data1-r1-v2.txt
- elife-00012-vor-fig3-r1-v2.tiff
- elife-00012-vor-fig3-data-r1-v2.csv
- elife-00012-vor-fig3-subfig1-r1-v2.tiff
- elife-00012-vor-fig3-subfig1-data1-r1-v2.csv
- elife-00012-vor-fig3-subfig1-data2-r1-v2.csv
- elife-00012-vor-fig3-subfig1-data3-r1-v2.csv
- elife-00012-vor-fig3-subfig2-r1-v2.tiff
- elife-00012-vor-fig3-subfig3-data1-r1-v2.csv
- elife-00012-vor-fig3-subfig3-r1-v2.tiff
- elife-00012-vor-fig3-subfig3-data1-r1-v2.csv

and this bundle gets archived.


###### ext

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


### workflow


### WTFAQs (Wait, These Fiddly Awkard Questions)


#### What happens when only a figure gets updated?


#### How do we upate a version number?


#### What paths needs to be retained in the XML to assetts?


#### How do we update a revision number?


#### Do all version updates require an update on the revision number?


#### They do? Surely that's a but dumb?


#### Why are revision numbers exposed on the final published version?


#### How do we update a `run` number in the production system?


#### Why don't we store run number information in the file name?


#### Wait, are we really updating all the names of all the files if only one figure gets updated?


#### Do we want to keep track of all the things that happen to a file before it hits the production system, and include a record of those things somehow in the file name?

#### Do we increment VOR version numbers if there was a POA version number before, or do we start over again with a new version number for the article, as it's name has changed to reflect the new status?

#### How do we prevent an old packet of an article entering the publising system, and creating a new published version?
