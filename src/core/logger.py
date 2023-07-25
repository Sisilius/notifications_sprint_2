import sentry_sdk
import structlog_sentry_logger
import structlog

sentry_sdk.init(
    dsn="https://8b8e5325f8f447e1b8b0bb347cd6708e@o4505591727980544.ingest.sentry.io/4505591777787904",

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production,
    traces_sample_rate=1.0,
)
sentry_sdk.utils.MAX_STRING_LENGTH = 8192


logger: structlog.stdlib.BoundLogger = structlog_sentry_logger.get_logger()
