import argparse, fileinput, re, random, sys
from PyDictionary import PyDictionary

dictionary = PyDictionary()


def foodbox_translate(text, missing_letters):
    result = ''

    for token in re.split('(\w+)(?=\W)?', text):
        if 'e' not in token:
            result += token
            continue

        synonyms = [x for x in dictionary.synonym(token) or [None] if x]

        synonyms = [word for word in synonyms if not any(char in word for char in missing_letters)]

        if not synonyms:
            result += token
            continue

        synonym = random.choice(synonyms)
        if token[0].isupper():
            synonym = synonym[0].upper() + synonym[1:]
        result += synonym

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
