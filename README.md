# Columbus Voter File
Code to extract Franklin County, OH voter file information and analyze patterns in voting behavior. There are two versions of the code, one working with data stored in a flat JSON and one working with a SQLite DB.


## JSON
To create flat JSON for full voter file and sub-samples split every 100k voters, go to makeSamples/ and run

> $ python makeFlatVoterFileSplitSamplesJSON.py

Sub-samples to be used for calculating correlations and training voter likelihood algorithm. To test general content of subsample, run

> $ python testSubSamples.py

Code running analysis is accessed by going to analysis/ and running

> $ python simpleAnalysis.py

## SQLite
The same general output is created in a SQLite DB by going to sql/ and running

> $ python makeVoterTable.py

Voters are split into sub-samples identified in SUBSAMPLE column. To test general content, run

> $ python testTable.py

Code analyzing SQLite DB run by going to analysis/ and running

> $ python runAnalysisSQL.py
