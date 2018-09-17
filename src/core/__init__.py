import logging

logger = logging.getLogger()
# in Lambda, the root logger is pre-configured and the way to
# detect this is to check if it has any handlers;
# this check and the call to basicConfig ensures the root logger,
# for all means and purposes, works locally as well
if not logger.handlers:
    logging.basicConfig(level=logging.INFO)
logger.setLevel(logging.INFO)
