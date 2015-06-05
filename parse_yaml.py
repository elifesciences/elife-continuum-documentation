import yaml
import yaml_settings as settings

yaml_file = settings.YAML_FILE

yaml_content = open(yaml_file, "r").read()

yaml.load(yaml_content)
