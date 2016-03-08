# Bot activities for PPP workflows

## PublishPerfectArticle

####ExpandArchive

- Downloads zip from S3
- Unzips
- Determines pub date and version if present in zip filename
- Creates unique run number
- Uploads to "expanded folder" in S3
- Stores expanded folder path and run in session


####ApplyVersionNumber

- Renames assets in expanded folder to include the version (expand)


####ConvertJATS

- Determines JATS XML path in expanded folder
- Downloads JATS file
- Converts to EIF JSON format with jats-scraper/elife-tools
- Stores eif path in session


####SetPublicationStatus

- Sets Publish property in eif file to 1 or 0 depending on publication_settings.yaml and article scheduling service.


####ResizeImages

- Downloads each file in expanded folder that matches Figure Image definition
- Creates multiple versions according to formats.yaml file.
- Uploads these to CDN


####DepositAssets

- Copies each file in expanded folder to CDN


####PostEIF

- POSTs the EIF file to drupal for ingest
- If ingest successful
	- Creates messge required to initiate PostPerfectPublication workflow.
	- checks the value on Publish returned by drupal and
		- if 1, send message to workflow starter queue
		- if 0, send as property to dashboard for later sending

##PostPerfectPublication

####ArchiveArticle

- archive contents of expanded folder
- uploads archive to archive folder

####UpdateLax

- update LAX with the JSON so it updates the published version number

##ApproveArticlePublication

####ApprovePublication

- call service on drupal site to publically publish nodes for article version
- initiate PostPerfectPublication workflow