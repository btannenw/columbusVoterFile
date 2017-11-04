Code to extract Franklin County, OH voter file information, store in flat JSON or SQLite DB, and analyze patterns in voting behavior.

To create flat JSON for full voter file and sub-samples split every 100k voters, go to makeSamples/ and run

> $ python makeFlatVoterFileSplitSamplesJSON.py

Sub-samples to be used for calculating correlations and training voter likelihood algorithm. To test general content of subsample, run

> $ python testSubSamples.py

The same general output is created in a SQLite DB by going to sql/ and running

> $ python makeVoterTable.py

Voters are split into sub-samples identified in SUBSAMPLE column. To test general content, run

> $ python testTable.py

Code analyzing JSON or SQLite DB run by going to analysis/ and running

> $ python simpleAnalysis.py
