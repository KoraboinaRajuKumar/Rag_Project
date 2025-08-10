import yaml
import os

def load_config(config_path:str="config/config.yaml") -> dict:
    """
    Load configuration from a YAML file.

    Args:
        config_path (str): Path to the YAML configuration file.

    Returns:
        dict: Configuration data loaded from the YAML file.
    """
    # Resolve path relative to project root
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    print(f"Base directory for config: {base_dir}")
    abs_path = os.path.join(base_dir, config_path)
    print(f"Absolute path to config file: {abs_path}")
    with open(abs_path, 'r', encoding='utf-8') as file:
        config = yaml.safe_load(file)
    return config

data = load_config("config/config.yaml")
print(data)