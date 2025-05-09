import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("logger_name")
logger.debug("Это дебаг лог")
logger.info("Это инфо лог")
logger.warning("Это варнинг лог")
logger.error("Это лог про ошибку")
logger.critical("Этот лог про критическую ошибку")
