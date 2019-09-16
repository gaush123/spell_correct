# spell_correct


To replicate results using vanilla python use 'requirments.txt' file

To replicate results using anaconda run:

`conda env create -f spellcorrect.yml`


Launch Flask app:
`python spell_correct.py`

Run using post request:
`curl localhost:5000/spellCorrect -d '{"word": "thew"}' -H 'Content-Type: application/json'`

