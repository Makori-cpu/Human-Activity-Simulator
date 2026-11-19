
from settings_manager import SettingsManager

settings = SettingsManager()

print("Current settings:")
print(settings.get_all_settings())

settings.update_setting("mouse_speed", 7)

print("\nUpdated mouse speed:")
print(settings.get_setting("mouse_speed"))
