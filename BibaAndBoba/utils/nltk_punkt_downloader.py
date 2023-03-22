"""
Important! This module downloads the punkt tokenizer from NLTK.
"""
import nltk
import ssl

from BibaAndBoba.utils.logger import logger


def download_punkt():
    try:
        _create_unverified_https_context = ssl._create_unverified_context
    except AttributeError:
        logger.warning(
            "Warning, ssl unverified context is not available.\n"
            "Consider installing punkt tokenizer from NLTK manually. Help: https://www.nltk.org/data.html"
        )
    else:
        ssl._create_default_https_context = _create_unverified_https_context

    nltk.download("punkt")
    logger.info("Successfully downloaded punkt tokenizer from NLTK.")


if __name__ == "__main__":
    download_punkt()
