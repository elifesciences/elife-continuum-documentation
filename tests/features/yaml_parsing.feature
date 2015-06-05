Feature: Parse a pub workflow yaml file
	In order to understand workflow settings
	As the bot code
	I need to parse the settings yaml file

	@types
	Scenario Outline: Get article types:
		Given I have the settings file "<file>"
		And I get a list of article types
		Then I should have the artice types "<types>"

		Examples:
		| file | types |
		| elife_pub_workflow_testfile.YAML | ['research vor', 'research poa', 'feature', 'editorial', 'correction', 'insight'] |

  @stages
	Scenario Outline: Get processing stages:
		Given I have the settings file "<file>"
		And I get a list of processing stages
		Then I should have the stages "<stages>"

		Examples:
		| file | stages |
		| elife_pub_workflow_testfile.YAML | ['assembly', 'publish', 'downstream', 'archive'] |

	@name
	Scenario Outline: Get document name:
		Given I have the settings file "<file>"
		And I get the name of the of the document
		Then I should have the name "<name>"

		Examples:
		| file | name |
		| elife_pub_workflow_testfile.YAML | PPP workflow descrption |

	Scenario Outline: Check attribute values:
		Given I have the settings file "<file>"
		And I am given the attribute "<attribute>"
		Then I should have the value "<value>"

		Examples:
		| file | attribute | value |
		| elife_pub_workflow_testfile.YAML | NAME | PPP workflow descrption |
		| elife_pub_workflow_testfile.YAML | SPEC-VERSION | 0.1 |
		| elife_pub_workflow_testfile.YAML | journal | eLife |

	Scenario: Get publishing workflow
		Given I have the settings file "<file>"
		And I am given the attribute "<attribute>"
		Then I should have the value "<value>"
