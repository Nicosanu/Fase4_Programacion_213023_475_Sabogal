import logging


def configurar_logger():
    logger = logging.getLogger("SoftwareFJ")
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        formato = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s"
        )

        archivo_handler = logging.FileHandler("software_fj.log", encoding="utf-8")
        archivo_handler.setFormatter(formato)

        consola_handler = logging.StreamHandler()
        consola_handler.setFormatter(formato)

        logger.addHandler(archivo_handler)
        logger.addHandler(consola_handler)

    return logger