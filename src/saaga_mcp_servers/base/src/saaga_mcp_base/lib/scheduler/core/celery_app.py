"""
Celery application configuration.
"""

from celery import Celery
import os
from saaga_mcp_base.config.env import CELERY, REDIS

# Create Celery app
app = Celery(
    CELERY.APP_NAME,
    broker=CELERY.get_broker_url(),
    backend=CELERY.get_backend_url(),
    # mybe i need include her
)

# TODO: This might have to be renabled.
# # Enable autodiscovery of tasks
# app.autodiscover_tasks(
#     packages=[
#         "src.services.mcp.scheduler",
#         "src.services.mcp.social",
#     ],  # Add social package
#     related_name="tasks",
# )

# Configure Celery
app.conf.update(
    result_expires=CELERY.RESULT_EXPIRES,
    task_serializer=CELERY.TASK_SERIALIZER,
    accept_content=CELERY.ACCEPT_CONTENT,
    result_serializer=CELERY.RESULT_SERIALIZER,
    timezone=CELERY.TIMEZONE,
    enable_utc=CELERY.ENABLE_UTC,
    broker_connection_retry_on_startup=True,
)

# # Optional: Configure periodic tasks
# app.conf.beat_schedule = {
#     # Example periodic task:
#     # 'run-every-30-seconds': {
#     #     'task': 'src.services.mcp.scheduler.tasks.base_tasks.example_periodic_task',
#     #     'schedule': 30.0,
#     # },
# }

if __name__ == "__main__":  # pragma: no cover
    app.start()
