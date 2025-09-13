import json
from typing import Any


class JsonConfigManager:
	"""
	Context manager for working with JSON configuration files.
    On entry — reads data from the .json file.
    On exit — writes the updated configuration back to the .json file.
	"""
	
	def __init__(self, filepath: str) -> None:
		self.filepath = filepath
		self.config: dict[str, Any] = {}
	
	def __enter__(self) -> "JsonConfigManager":
		try:
			with open(self.filepath, "r", encoding="utf-8") as file:
				self.config = json.load(file)
		except FileNotFoundError:
			raise FileNotFoundError(f"ERROR: '{self.filepath}' config file "
			                        f"was not found. Check the file name.")
		except json.JSONDecodeError as e:
			raise ValueError(f"ERROR: Json decoding error: {e}")
		return self
	
	def __exit__(self, exc_type, exc_val, exc_tb) -> None:
		try:
			with open(self.filepath, "w", encoding="utf-8") as f:
				json.dump(self.config, f, indent=4, ensure_ascii=False)
			print(f"DONE: Configuration was saved in the file: {self.filepath}")
		except Exception as e:
			print(f"ERROR: Error writing to file: {e}")
	
	def add_param(self, key: str, value: Any) -> None:
		"""
		Adds a parameter to the configuration if it does not already exist.
		Parameters:
			key: the parameter name
			value: the parameter value
		"""
		self.config[key] = value
		print(f"DONE: Added the parameter '{key}' with the value: {value}")
	
	def update_param_values_list(self, key: str, value: Any) -> None:
		"""
		Adds a value to a list parameter if it is not already present.
		Parameters:
			key: Parameter name (must be a list)
			value: Value to add
		"""
		if key not in self.config:
			self.config[key] = [value]
			print(f"DONE: Created new list '{key}' with elements: {value}")
		elif not isinstance(self.config[key], list):
			print(f"WARNING: The '{key}' parameter exists, but it is NOT the list.")
		elif value in self.config[key]:
			print(
				f"WARNING:  The '{value}' value exists in the '{key}' parameter. "
				f"Adding was skipped.")
		else:
			self.config[key].append(value)
			print(f"DONE: Added '{value}' to the '{key}' list")
	
	def update_nested_param(self, section: str, key: str, value: Any) -> None:
		"""
		Updates the nested parameter in the configuration,
		for example: config[“database”][‘host’] = “newhost”
		Parameters:
            section: Name of the top-level key (for example, “database”)
            key: Nested key (for example, “host”)
            value: New value
		"""
		if section not in self.config:
			print(
				f"WARNING:  Section ‘{section}’ not found. Creating a new one.")
			self.config[section] = {}
		
		if not isinstance(self.config[section], dict):
			print(f"WARNING: Section ‘{section}’ is not a dictionary. "
			      f"Change is not possible.")
			return
		
		old_value = self.config[section].get(key, "<was not>")
		self.config[section][key] = value
		print(f"DONE: Changed '{section}.{key}': {old_value} → {value}")


config_path = "task_08_configuration.json"

with JsonConfigManager(config_path) as config:
	config.add_param("debug", True)
	config.add_param("version", "1.2.3")
	
	config.update_param_values_list("features", "logging")
	config.update_param_values_list("features", "metrics")
	
	config.update_nested_param("database", "host", "127.0.0.1")
	config.update_nested_param("database", "port", 3306)
	config.update_nested_param("security", "token_expiry", 3600)
