def create_user_setting():
	setting = {"theme": "dark", "language": "ukr", "notification": "note 1"}
	
	def control_setting(action: str,
	                    setting_key: str = None,
	                    setting_value: str = None):
		if action == "get":
			if setting_key in setting:
				return setting.get(setting_key, f"'{setting_key}' is not found "
				                                f"for 'get' action!!!")
			return setting
		elif action == "set":
			if setting_key in setting:
				setting[setting_key] = setting_value
				return (f"Setting '{setting_key}' was changed "
				        f"on the '{setting_value}'")
			return (f"Specify the key to change the setting!!! "
			        f"The '{setting_key}' is not expected!!!")
		else:
			return ("Unexpected action with the setting!!! Use 'get' "
			        "or 'set' actions.")
	
	return control_setting


user_setting = create_user_setting()
print(user_setting("get"))
print(user_setting("get", "language"))
print(user_setting("set", "theme", "light"))
print(user_setting("get", "theme"))
print(user_setting("delete", "language"))
print(user_setting("get"))
print(user_setting("set", "language", "en"))
print(user_setting("get"))
print(user_setting("set", "notification", "note 2"))
print(user_setting("get"))
