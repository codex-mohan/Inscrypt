import logging
from rich.logging import RichHandler


def setup_logging():
    """Set up logging with RichHandler that shows file name & line number."""
    logging.basicConfig(
        level="DEBUG",
        # %(name)s = logger name (module path)
        # %(pathname)s:%(lineno)d = file & line
        format="[%(asctime)s] %(levelname)s %(pathname)s:%(lineno)d - %(message)s",
        datefmt="%H:%M:%S",
        handlers=[RichHandler(rich_tracebacks=True, show_path=True)],
    )

    # Optional: shorten module names (e.g. "app.v1.routes.stenography" -> "routes.stenography")
    class ShortNameFilter(logging.Filter):
        def filter(self, record):
            record.name = record.name.split(".")[-1]  # last part only
            return True

    root = logging.getLogger()
    for h in root.handlers:
        h.addFilter(ShortNameFilter())

    return logging.getLogger("rich")


logger = setup_logging()
