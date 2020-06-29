# covid19-spc
An SPC approach to viewing COVID 19 cases in Allegheny County

The code: covid-19.py and step-covid-19.py. 
Written by Justine Galbraith, 2020/06/27

I wrote this python script to draw and plot data from the NYT Covid-19 data set that they maintain online. 
Link: https://github.com/nytimes/covid-19-data

In particular, I am interested in Pennsylvania counties, and how important dates within the state (mask requirement, red, green, yellow phases) affect the number of cases.

The description of the phases can be found at the following link:
https://www.governor.pa.gov/process-to-reopen-pennsylvania/

My goal was to treat the spread of the coronavirus as if it were a statistical process, according to lean six sigma methodology. Important note: this is a really simplistic approach/analysis is not perfect. It doesn't take virology and the spread of a virus into account.  What it is trying to do, however, is to visualize the impact of 1) wearing a mask and 2) social distancing. 

To this effect, I considered the first "un-controlled" set to be the date range in the "red" phase prior to masks being required. 
The control data for this set started at 14 days after the red phase began - this was done to account for the 2-14 day incubation period prior to symptoms occuring. 
The idea is to discard any cases that could be attributed to uncontrolled "pre-red" data. 
The control data for this phase ended on the date that masks were required in Pennsylvania. 

Next, I considered the second "controlled" set to be the date range in the "red" phase after masks were required, prior to the "yellow" phase and loosesed social and business restrictions. 
Again, the control data for this set started at 14 days after the masks were required - this was done to account for the 2-14 day incubation period prior to symptoms occuring. 
The idea is to discard any cases that could be attributed to a maskless red phase. 
The control data for this set ended on the date that the county went to Yellow phase. 

For each of these two sets, I calculated the average and standard deviation, and plotted the important statisitical zones: Zone C (+/- 1 sigma around the average), Zone B (+/- 2 sigma around the average), and Zone A (+/- 3 sigma around the average).
If the data set represents a controlled, statistical process (i.e. has a normal distribution), then we'd expect 68% of cases to fall in Zone C, 95% of cases to fall in Zone B, and 99% of cases to fall in Zone A. 

Additionally, there are seven rules that identify when the process is out-of-control - either for the better (reduced # of cases!) or for the worse (increased # of cases!).
These represent non-random variation, or statistically unlikely variation, that should prompt investigation.
	1. OOC1: Any data point falls outside of Zone A. 
	2. OOC2: There are 7 or more consecutive points in an increasing or decreasing pattern (no up/down).
	3. OOC3: There are 8 or more consecutive points on one side of the average. 
	4. OOC4: There are 14 consecutive points in an "up/down" or "down/up" pattern.
	5. OOC5: At least 2 out of 3 consecutive points are in or above Zone A. 
	6. OOC6: At least 4 out of 5 consecutive points are in or above Zone B.
	7. OOC7: There are 15 or more consecutive points in Zone C. 
I included some conditions to identify and plot these OOC cases.

The end result in "covid-19.py" is a plot with two seperate areas or sets. The first for the maskless red phase data, and the second for the masked red phase data. The OOC conditions are considered only for the second data set - i.e. the best control scenario. Also, you can type in the county that you're intereted in.

If you want to see the step-by-step plots that show how this data was considered and built, I've also included a file called "step-covid-19.py". It outputs 6 figures:
	1. Just the plot with the raw data
	2. Includes vertical lines to indicate important dates in Pennsylvania for that county.
	3. Includes an indication for the 1st set's control data. 
	4. Includes the statistical zones, and OOC results for the 1st set.
	5. Takes away the 1st set's OOC results, and shows the 2nd set's control data
	6. Includes the 2nd set's statistical zones, and OOC results for the 2nd set. 
 

Again for emphasis: this is a pretty simplistic model. 
It doesn't consider the population density.
It doesn't consider the number of tests. 
It's just meant to show how we're doing compared with the "full control" phase of red & mask. 

Feedback on code or stastical methods/assumptions is appreciated :)
