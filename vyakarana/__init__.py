import logging
import sys

log = logging.getLogger(__name__)
out = logging.StreamHandler(sys.stdout)
out.setLevel(logging.DEBUG)
log.addHandler(out)
log.setLevel(logging.DEBUG)
