from lxml import objectify
import dateutil.parser
from enum import Enum
from decimal import *
import datetime

file_path = input(".tcs file path: ")

class TrackPoint:
	def __init__(self, time, distance):
		self.time = time
		self.distance = distance

	def __str__(self):
		return str(time, distance)

class Track:
	def __init__(self, tcx_file):
			tree = objectify.parse(tcx_file)
			root = tree.getroot()
			track = root.Activities.Activity.Lap.Track

			self.totaldistance = root.Activities.Activity.Lap.DistanceMeters.pyval
			self.totaltime = datetime.timedelta(seconds=root.Activities.Activity.Lap.TotalTimeSeconds.pyval)

			startdate = dateutil.parser.parse(track.Trackpoint.Time.text)
			
			self.trackpoints = []
			for trackpointObj in track.iterchildren():
				dist = trackpointObj.DistanceMeters.pyval
				date = dateutil.parser.parse(trackpointObj.Time.text)
				time = date - startdate
				self.trackpoints.append(TrackPoint(time, dist))

			note = root.Activities.Activity.Lap.Notes
			# ex: "1000m F, 110s S"

			intervals = []
			if note != None:
				interval_strs = note.text.split(", ")
				for i_str in interval_strs:
					try:
						contents = i_str.split(" ")
						amount = float(contents[0][0:-1])
						
						unit = contents[0][-1]
						pace = contents[1]

						pace_map = {"F": Pace.FAST, "M": Pace.MEDIUM, "S": Pace.SLOW}

						if unit == "m":
							intervals.append(Distance(amount,pace_map[pace]))
						if unit == "s":
							intervals.append(Duration(amount, pace_map[pace]))

					except Exception as e: pass

			self.workout = Workout(intervals)

	def __iter__(self):
		return iter(self.trackpoints)

	def analize(self):
		w = iter(self.workout)
		print("\nWORKOUT:")
		print("Total Distance:", str(self.totaldistance)+"m")
		print("Total Time:", self.totaltime)
		print("Pace:", self.totaltime /(self.totaldistance *0.001))

		try:
			interval = next(w)
			print("\nintervals:")
			zero = datetime.timedelta(seconds=0)
			time_sums = {Pace.FAST: zero, Pace.MEDIUM: zero, Pace.SLOW: zero}
			distance_sums = {Pace.FAST: 0.0, Pace.MEDIUM: 0.0, Pace.SLOW: 0.0}
			pace_count = {Pace.FAST: 0, Pace.MEDIUM: 0, Pace.SLOW: 0}
			for tp in self:
				if interval.process(tp):
					print(interval)
					time_sums[interval.pace] += interval.get_time()
					distance_sums[interval.pace] += interval.get_distance()
					pace_count[interval.pace] += 1

					interval = next(w)

					interval.process(tp) # process previous last as now first tp
			
			if interval.progress < 1:
				print("Not complete:")
				print(interval)

		except StopIteration as e: pass # workout complete

		print("\naverages:")
		for pace in Pace:
			if pace_count[pace] == 0: continue
			print("    " + pace.name + "_avg: ",
				"distance: " + str(distance_sums[pace] / pace_count[pace]) + ",",
				"time: ", time_sums[pace] / pace_count[pace],
				)

		print("\ntotals:")
		for pace in Pace:
			if pace_count[pace] == 0: continue
			print("    " + pace.name + "_total: ",
				"distance: " + str(distance_sums[pace]) + ",",
				"time: ", str(time_sums[pace]) + ",",
				"pace: ", time_sums[pace]/(distance_sums[pace]*0.001)
				)


class Interval:
	def __init__(self, pace):
		self.progress = 0.0
		self.currenttime = 0.0
		self.currentdistance = 0.0
		self.starttime = -1.0
		self.startdistance = -1.0
		self.type = 'Interval'
		self.pace = pace

	def process(self, trackpoint):
		pass

	def get_distance(self):
		return self.currentdistance - self.startdistance

	def get_time(self):
		return datetime.timedelta(seconds=self.currenttime - self.starttime)

	def __str__(self):
		header = "<" + self.type + ", " + self.pace.name + ">:"
		body = "\n     distance: " + str(self.get_distance()) + ", time: " + str(self.get_time())
		return header + body


class Pace(Enum):
	FAST = 'FAST'
	MEDIUM = 'MEDIUM'
	SLOW = 'SLOW'

class Duration(Interval):

	def __init__(self, duration: float, pace: Pace):
		# duration in seconds
		self.duration = duration
		super().__init__(pace)
		self.type = 'Duration'

	def process(self, trackpoint):
		if self.starttime == -1:
			self.starttime = trackpoint.time.total_seconds()
			self.startdistance = trackpoint.distance
		else:
			self.currenttime = trackpoint.time.total_seconds()
			self.currentdistance = trackpoint.distance
			self.progress = (self.currenttime - self.starttime) / self.duration

		return (self.progress >= 1)




class Distance(Interval):

	def __init__(self, distance: float, pace: Pace):
		# distance in metres
		self.distance = distance
		super().__init__(pace)
		self.type = 'Distance'

	def process(self, trackpoint):
		if self.startdistance == -1:
			self.starttime = trackpoint.time.total_seconds()
			self.startdistance = trackpoint.distance
		else:
			self.currenttime = trackpoint.time.total_seconds()
			self.currentdistance = trackpoint.distance
			self.progress = (trackpoint.distance - self.startdistance) / self.distance

		return (self.progress >= 1)


class Workout:
	def __init__(self, intervals):
		self.intervals = intervals

	def __iter__(self):
		return iter(self.intervals)

	def __str__(self):
		return str(self.intervals)

t = Track(file_path)
t.analize()