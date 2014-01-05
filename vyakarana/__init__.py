import logging
import sys

logger = logging.getLogger(__name__)
out = logging.StreamHandler(sys.stdout)
out.setLevel(logging.DEBUG)
logger.addHandler(out)
logger.setLevel(logging.DEBUG)
