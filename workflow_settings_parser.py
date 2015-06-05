import logging
import yaml

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.propagate = False # stops logger logging to stdout

handler = logging.FileHandler('settings_parser.log')
handler.setLevel(logging.DEBUG)

formatter= logging.Formatter("%(created)f - %(levelname)s - [%(filename)s:%(lineno)s - %(funcName)20s() ] - %(name)s - %(message)s")

handler.setFormatter(formatter)
logger.addHandler(handler)

logger.info("")

def load_yaml(yaml_file):
	logger.info("")
	file_content = open(yaml_file, "r").read()
	structured_content = yaml.load(file_content)
	logger.debug(structured_content)
	return structured_content

def name(yaml_data):
	logger.info("")
	name = yaml_data["NAME"]
	return name

def get_article_types(yaml_data):
	article_types = yaml_data["article types"]
	return article_types

def get_processing_stages(yaml_data):
	stages = yaml_data["valid stages"]
	return stages
