# Runtastic Interval Stats

A simple to use python script, which lets you analyse your interval training from a runtastic workout.

## How to use
Write your intervals as note as follows:

	[meters]m [pace], [duration]s [pace], ...
where pace is

	F - fast
	M - medium
	S - slow

![](https://github.com/markus7800/RuntasticIntervalStats/blob/master/Readme1.jpg)


Download the .tcx file from runtastic.com
![](https://github.com/markus7800/RuntasticIntervalStats/blob/master/Readme2.jpg)

Run the script and pass in your .tcx file path
>.tcs file path: [your file path]

## Stats

The script calculates the total distance, total time, pace, the distance and duration for each interval and the average/total distance/time for each pace.  

    WORKOUT:
	Total Distance: 6230m
	Total Time: 0:34:46
	Pace: 0:05:34.831461

	intervals:
	<Distance, FAST>:
	     distance: 1002, time: 0:04:42
	<Duration, SLOW>:
	     distance: 127, time: 0:01:10
	<Distance, FAST>:
	     distance: 1005, time: 0:04:38
	<Duration, SLOW>:
	     distance: 112, time: 0:01:10
	<Distance, FAST>:
	     distance: 1000, time: 0:04:52
	<Duration, SLOW>:
	     distance: 115, time: 0:01:10
	<Distance, FAST>:
	     distance: 1005, time: 0:04:56
	<Duration, SLOW>:
	     distance: 112, time: 0:01:11
	<Distance, FAST>:
	     distance: 1000, time: 0:04:45

	averages:
	    FAST_avg:  distance: 1002.4, time:  0:04:46.600000
	    SLOW_avg:  distance: 116.5, time:  0:01:10.250000

	totals:
	    FAST_total:  distance: 5012.0, time:  0:23:53, pace:  0:04:45.913807
	    SLOW_total:  distance: 466.0, time:  0:04:41, pace:  0:10:03.004292
