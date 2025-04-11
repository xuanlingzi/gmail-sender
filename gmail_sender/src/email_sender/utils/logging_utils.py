import logging


def setup_logging(log_file_path, log_level):
    """设置日志记录"""
    logging.basicConfig(filename=log_file_path,
                        level=log_level,
                        format='%(asctime)s - %(levelname)s - %(message)s')
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    console.setFormatter(
        logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    logging.getLogger('').addHandler(console)
