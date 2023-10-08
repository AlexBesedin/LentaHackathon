import logging

def setup_logging():
    _logger = logging.getLogger(__name__)
    _logger.setLevel(logging.DEBUG)
    handler_m = logging.StreamHandler()
    formatter_m = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")
    handler_m.setFormatter(formatter_m)
    _logger.addHandler(handler_m)
    
    handler_f = logging.FileHandler("ml-service.log", mode='a', encoding='utf-8')
    formatter_f = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")
    handler_f.setFormatter(formatter_f)
    _logger.addHandler(handler_f)
    
    return _logger

_logger = setup_logging()
