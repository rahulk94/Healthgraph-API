import healthgraph

class Points:

	sports = {	
					'Mountain Biking': 1.1
					,'Competitive Rowing': 1
					,'Kickboxing': 1.5
					,'Soccer': 1
					,'Brazilian Jiu-Jitsu': 1.2
					,'Tennis': 1.4
					,'Swimming': 1.2
					,'Volleyball': 0.9
					,'Ice Hockey': 1.3
					,'Rock Climbing': 0.9
					,'Racquetball': 1
					,'Golf': 0.7
					,'Squash': 1
					,'Taekwondo': 1
					,'Baseball':1
					,'American Football':1
					,'Snowboarding':1
					,'Kayaking':1
					,'Krav Maga': 1.5
					,'Beach Volleyball': 1.1
					,'Ultimate Frisbee':1
					,'Wrestling': 0.9
					,'Street Hockey':1
					,'Roller Derby':1
					,'Ping-Pong':1
					,'Roller Skating':1
					,'Badminton':1
					,'Surfing':1
					,'Ice Skating':1
					,'Lacrosse':1
					,'Horseback Riding':1
					,'Fencing':1
					,'Water Polo':1
					,'Field Hockey':1
					,'Frisbee': 0.75
					,'Broomball':1
					,'Hand Ball':1

						}

	cardio = {	'Cycling':2
				,'Running':2
			
						}


	def __init__(self, fitness_iterator, strength_iterator):
		self.fitness_activity_iter = fitness_iterator
		self.strength_activity_iter = strength_iterator

	def test_method(self):
		print("jak is gay")

	def get_total_points(self):
		total_points = 0
		# for exercise in self.fitness_activity_iter:
		# 	exercise_points = self.get_points(exercise)
		# 	total_points += exercise_points

		for feed_item in self.strength_activity_iter:

			exercise_points = self.get_feed_points(feed_item)
		# 	total_points += exercise_points
		

		return total_points

	def get_feed_points(self, feed_item):
		# print(feed_item)
		tonnage = 0
		str_act = feed_item.get_activity_detail()
		info_set = str_act.get('exercises')[0].get('sets')

		for ex_set in info_set:
			weight = ex_set.get('weight')
			reps = ex_set.get('repetitions')
			tonnage += weight * reps
		return tonnage




	def get_points(self, exercise):
		activity = exercise.get("uri")[0]

		exercise_type = exercise.get("type")
		

		if activity == "FitnessActivity":

			duration = exercise.get("duration")/60

			if exercise_type == "Other":
				#sports. Requires going into URI for secondary_type field
				# points = self.sports[exercise_type] * duration
				# return points
				pass
			else:
				points = self.cardio[exercise_type] * duration
				print("POINTS FOR EX = " + str(points))
				print("duration = " + str(duration))
				return points
		elif activity == "StrengthActivity":
			#Get type of exercise
			exActivity = exercise.get_activity_detail()

			for ex_set in exActivity.get('exercises'):
				print(ex_set)
				# weight = ex_set.get('')
				# reps = activity.getReps()
				# sets = activity.getSets()
				# tonnage = weight * sets * reps
				# return tonnage/100
			pass

		# 	#do shit
		# 	activity = activity.getActivity()
		# 	time = activity.getDuration()
		# 	points = sports[activity] * time

		# 	return points

		# else if activity.getType() == strength Activity:
		# 	#do shit

		# 	weight = activity.getWeight()
		# 	reps = activity.getReps()
		# 	sets = activity.getSets()
		# 	tonnage = weight * sets * reps

		# 	return tonnage/100

		return 0
