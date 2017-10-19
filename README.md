Code to extract Franklin County, OH voter file information, store in flat JSON, and analyze patterns in voting behavior.

Run

> $ python makeFlatVoterFileSplitSamplesJSON.py

to create flat JSON for full voter file and sub-samples split every 100k voters. Sub-samples to be used for calculating correlations and training voter likelihood algorithm. To test general content of subsample, run

> $ python testSubSamples.py
