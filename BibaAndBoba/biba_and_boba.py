import pandas as pd
from nltk.probability import FreqDist

from BibaAndBoba.utils.reader import FileInput
from BibaAndBoba.utils.reader import Reader
from BibaAndBoba.utils.tokenizer import tokenize

from BibaAndBoba.utils.logger import logger


class BibaAndBoba:
    """
    BibaAndBoba is a class that for analyzing two Telegram chat history files.
    It provides a methods to get the difference words, the frequency distribution of the difference words,
    and other parameters. Uses NLTK library to tokenize the messages. :class:`BibaAndBoba.Reader` class is used to read
    the files.
    """

    def __init__(
        self,
        file_1: FileInput,
        file_2: FileInput,
        subtraction_threshold: int = 3,
        use_cache: bool = True,
        flush_cache: bool = False,
    ):
        """
        The __init__ function is called when an instance of the class is created.
        It initializes all the variables that are unique to each instance.

        :param self: Reference the object itself
        :param file_1: Specify the first file
        :param file_2: Specify the second file
        :param subtraction_threshold: The threshold for the subtraction function, defaults to 3. It's not
            recommended to use a value bigger than 3 unless you need to.
        :type subtraction_threshold: int (optional)
        :param use_cache: Whether to use the cache or not, defaults to True
        :type use_cache: bool (optional)
        :param flush_cache: Whether to flush the cache or not, defaults to False
        :type flush_cache: bool (optional)
        :raises: ValueError: If files are identical
        """
        if not use_cache:
            logger.warning(
                "Warning, cache is disabled. This may significantly slow down the process.\n"
            )

        file_1 = Reader(file_1)
        file_2 = Reader(file_2)
        file_1_companion_id = file_1.get_companion_id()
        file_2_companion_id = file_2.get_companion_id()

        if file_1_companion_id == file_2_companion_id:
            raise ValueError("Interlocutors must be different")

        self.__person_1_name = file_1.get_companion_name()
        self.__person_2_name = file_2.get_companion_name()

        self.__tokenized_person_1 = tokenize(
            file_1.get_messages(),
            file_1_companion_id,
            self.__person_1_name,
            use_cache=use_cache,
            flush_cache=flush_cache,
        )

        self.__tokenized_person_2 = tokenize(
            file_2.get_messages(),
            file_2_companion_id,
            self.__person_2_name,
            use_cache=use_cache,
            flush_cache=flush_cache,
        )

        self.__difference_words = self.__subtraction(threshold=subtraction_threshold)

    def __subtraction(self, threshold: int) -> list[str]:
        """
        The __subtraction function takes two lists of strings as input.
        It returns a list of words that are in the first list but not in the second.

        :param self: Access variables that belongs to the class
        :return: A list of words that are present in the minuend but not in the subtrahend
        """
        messages_minuend = self.__tokenized_person_1
        subtrahend_freq_dist = FreqDist(self.__tokenized_person_2)

        difference_words = []

        for word in messages_minuend:
            if subtrahend_freq_dist.get(word, 0) < threshold:
                difference_words.append(word)

        return difference_words

    def parasite_words(self, limit: int = 10) -> pd.DataFrame:
        """
        Takes a list of words, counts the frequency of each word, and returns a :class:`pd.DataFrame` with the most
        frequent ones.

        :param limit: The number of words to return, defaults to 10
        :type limit: int (optional)
        :return: A dataframe with the most common words and their counts.
        """
        fdist = FreqDist(self.__difference_words)
        df = pd.DataFrame(fdist.most_common(limit), columns=["Word", "Count"])

        df["Quotient"] = df["Count"] / df.sum(axis=0)["Count"]

        return df

    def get_tokenized_words_person_1(self) -> list[str]:
        """
        Returns a list of all words in the message
        sent by person 1.

        :param self: Refer to the object of the class
        :return: A list of all the words in the person 1 messages
        """
        return self.__tokenized_person_1

    def get_tokenized_words_person_2(self) -> list[str]:
        """
        Returns a list of all words in the message
        sent by person 2.

        :param self: Access the class attributes and methods
        :return: A list of all the words in the person 2 messages
        """
        return self.__tokenized_person_2

    def get_name(self) -> str:
        """
        Returns the name of the object.

        :param self: Refer to the object itself
        :return: The name of the object
        """
        return self.__person_1_name

    def get_difference_words(self) -> list[str]:
        """
        Returns a list of words that are in the first text but not in the second.

        :param self: Access the attributes and methods of the class
        :return: A list of words that are unique to the first person document
        """
        return self.__difference_words
