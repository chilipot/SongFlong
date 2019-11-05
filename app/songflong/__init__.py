import logging

log_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)

logger = logging.getLogger('songflong_builder')
logger.addHandler(handler)
