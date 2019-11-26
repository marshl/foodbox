# foodbox.py
Translates stdin by replacing any word with a forbidden character with a synonym of that word

# Installation

- Create the virtual environment
`python3 -m venv myvenv`
- Activate the virtual environment
`source <env_name>/bin/activate`
or
`<env_name>\scripts\activate.bat`
- Install the requirements
`pip install -r requirements.txt`
- Download the nltk data
```
> python3
>>> import nltk
>>> nltk.download()
```
- Download `wordnet` under `Copora` and `punkt` under `Models`

### Operation
foodbox.py takes a list of forbidden characters as the first command line argument
and replaces from stdin any words that have a characters
specified in the forbidden characters list and with a synonym
that doesn't use that character.

In this example, all the words with the letter 'e' in them have been replaced:
 ```
 > echo 'Hello, world! This is some text.' | python foodbox.py e
 'Hullo, world! This is part of wording.'
 ```