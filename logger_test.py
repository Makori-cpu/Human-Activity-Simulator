
from activity_logger import ActivityLogger

logger = ActivityLogger()

logger.log_activity("Simulator started")
logger.log_activity("Mouse movement tested")
logger.log_activity("Keyboard input tested")

print("\nActivity History:")
print(logger.get_activities())
