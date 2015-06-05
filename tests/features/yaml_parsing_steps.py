from lettuce import step, world
from workflow_settings_parser import *
import test_settings as settings

YAML_ROOT_DIR = settings.YAML_ROOT_DIR

@step(u'Given I have the settings file "([^"]*)"')
def given_i_have_the_settings_file_group1(step, file):
	yaml = load_yaml(YAML_ROOT_DIR + file)
	world.yaml = yaml
	return world.yaml



@step(u'And I get a list of article types')
def and_i_get_a_list_of_article_types(step):
	yaml = world.yaml
	world.article_types = get_article_types(yaml)

@step(u'Then I should have the artice types "(.*)"')
def then_i_should_have_the_artice_types_group1(step, types):
	assert str(types) == str(world.article_types)



@step(u'And I get a list of processing stages')
def and_i_get_a_list_of_processing_stages(step):
	yaml = world.yaml
	world.processing_stages = get_processing_stages(yaml)

@step(u'Then I should have the stages "([^"]*)"')
def then_i_should_have_the_stages_group1(step, stages):
	assert str(world.processing_stages) == str(stages)



@step(u'And I get the name of the of the document')
def and_i_get_the_name_of_the_of_the_document(step):
	yaml = world.yaml
	world.name = name(yaml)

@step(u'Then I should have the name "([^"]*)"')
def then_i_should_have_the_name_group1(step, name):
	assert str(name) == str(world.name)



@step(u'And I am given the attribute "([^"]*)""')
def and_i_am_given_the_attribute_group1(step, attribute):
	world.attribute = attribute

@step(u'Then I should have the value "([^"]*)"')
def then_i_should_have_the_value_group1(step, value):
	yaml = world.yaml
	yaml_value = yaml[world.attribute]
	print yaml_value
	print value
	assert str(yaml_value) == str(value)
