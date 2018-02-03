import argparse, random, re, sys, warnings
from nltk.corpus import wordnet as wn
from PyDictionary import PyDictionary

warnings.simplefilter('ignore')
dictionary = PyDictionary()

def get_pydictionary_synonyms(word, missing_letters):
    synonyms = [x for x in dictionary.synonym(word) or [None] if x]
    return reduce_synonyms(word, synonyms, missing_letters)


def get_wordnet_synonyms(word, missing_letters):
    if not wn.synsets(word):
        return []
    synonyms = [x for x in wn.synsets(word)[0].lemma_names()]
    return reduce_synonyms(word, synonyms, missing_letters)


def reduce_synonyms(word, synonyms, missing_letters):
    # Remove words that are the same as the actual token
    synonyms = [x for x in synonyms if x.lower() != word.lower()]
    # Remove synonyms that have the forbidden letters
    synonyms = [x for x in synonyms if not any(char in x for char in missing_letters)]
    return synonyms


def foodbox_translate_word(word, missing_letters):
    if not any(char in word for char in missing_letters):
        return word

    synonyms = get_wordnet_synonyms(word, missing_letters) or get_pydictionary_synonyms(word, missing_letters)

    if not synonyms:
        return word

    synonym = random.choice(synonyms)
    if word[0].isupper():
        synonym = synonym[0].upper() + synonym[1:]

    return synonym


def foodbox_translate(text, missing_letters):
    result = ''

    for token in re.split('(\w+)(?=\W)?', text):
        result += foodbox_translate_word(token, missing_letters)

    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Translates stdin by replacing any word with a forbidden character with a synonym of that word')

    parser.add_argument('infile', nargs='?', type=argparse.FileType('r'), default=sys.stdin)
    parser.add_argument('forbidden_letters', type=str,
                        help='The letters that can\'t be used')

    args = parser.parse_args()

    for line in sys.stdin:
        print(foodbox_translate(line, args.forbidden_letters), end=None)
