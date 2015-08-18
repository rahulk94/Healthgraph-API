import HealthGraphPackage

class Points:

	sports = {	
					'Mountain Biking': 2.1
					,'Competitive Rowing': 2
					,'Kickboxing': 2.5
					,'Soccer': 2
					,'Brazilian Jiu-Jitsu': 2.1
					,'Tennis': 2.4
					,'Swimming': 2.1
					,'Volleyball': 1.8
					,'Ice Hockey': 2.2
					,'Rock Climbing': 1.8
					,'Racquetball': 2
					,'Golf': 1.2
					,'Squash': 2
					,'Rugby': 2
					,'Softball': 1.5
					,'Taekwondo': 1.3
					,'Baseball': 1.5
					,'American Football': 1.9
					,'Snowboarding': 1.7
					,'Kayaking': 2
					,'Krav Maga': 2.3
					,'Beach Volleyball': 1.9
					,'Ultimate Frisbee': 2
					,'Wrestling': 2
					,'Street Hockey':2
					,'Roller Derby': 1.7
					,'Ping-Pong': 1.5
					,'Roller Skating': 1.7
					,'Badminton': 2
					,'Surfing': 2.3
					,'Ice Skating': 1.7
					,'Lacrosse': 2
					,'Horseback Riding': 1.2
					,'Fencing': 1.5
					,'Water Polo': 2
					,'Field Hockey': 2
					,'Frisbee': 1.3
					,'Broomball': 1.6
					,'Hand Ball': 2
					,'Basketball': 2

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
		
		for feed_item in self.fitness_activity_iter:
			
			print(get_start_time(feed_item))
			exercise_points = self.get_points(feed_item)
			total_points += exercise_points

		for feed_item in self.strength_activity_iter:

			
			#may need to do a check here for date before adding points of a feed
			exercise_points = self.get_points(feed_item)
# 			print (exercise_points)
			total_points += exercise_points
		

		return total_points



	#pass this an activity feed item and it will return points, it will iterate through exercies if it is a strength feed item
	def get_points(self, feed):
		activity = get_activity_type(feed)

		exercise_type = get_type(feed)
		

		if activity == "FitnessActivity":

			duration = feed.get("duration")/60

			if exercise_type == "Other":
				sport_act = feed.get_activity_detail()
				sport_type = get_secondary_type(sport_act)
				points = self.sports[sport_type] * duration
# 				print("POINTS FOR " + get_exer_name(feed) + " = " + str(points))
				return points
			else:
				points = self.cardio[exercise_type] * duration
				# print("POINTS FOR " + get_exer_name(feed) + " = " + str(points))
				return points
		elif activity == "StrengthActivity":
			#Get type of exercise
			tonnage = 0
			str_act = feed.get_activity_detail()
			info_set = get_exercise_set(str_act)
# 			print(str_act.get('exercises'))
			for ex_set in info_set:
				weight = get_weight(ex_set)
				reps = get_weight(ex_set)
				tonnage += weight * reps
				
				# print("POINTS FOR " + get_exer_name(feed) + " = "+ str(weight * reps))
				
			return int(round(tonnage))

	

		# else if activity.getType() == strength Activity:
		# 	#do shit

		# 	weight = activity.getWeight()
		# 	reps = activity.getReps()
		# 	sets = activity.getSets()
		# 	tonnage = weight * sets * reps

		# 	return tonnage/100

		return 0
	
	
	

#WRAPPER METHODS FOR DICTIONARY INFO RETRIEVAL	
def get_exercise_type(act):
	pass

def get_type(feed_item):
	return feed_item.get("type")

def get_secondary_type(act):
	return act.get('secondary_type')

#Give me a feed item and I will return the activity name!
def get_exer_name(feed_item):
	#cardio activity
	if ((get_activity_type(feed_item) == 'FitnessActivity') and not (get_type(feed_item) == 'Other')):
		return get_type(feed_item)
	#sport activity
	elif get_type(feed_item) == 'Other':
		sport_act = feed_item.get_activity_detail()
		return get_secondary_type(sport_act)
	#strength activity
	elif get_activity_type(feed_item) == 'StrengthActivity':
		str_act = feed_item.get_activity_detail()
		return get_secondary_type(str_act.get('exercises')[0])


#returning the list of the sets of a particular strength exercise
def get_exercise_set(str_act):
	return str_act.get('exercises')[0].get('sets')

def get_weight(str_act):
	return str_act.get('weight')

def get_reps(str_act):
	return str_act.get('repetitions')

#gets the activity type of a feed item (strength or fitness)
def get_activity_type(feed_item):
	return feed_item.get("uri")[0]
	
def get_start_time(act):
	return act.get("start_time")
	
	
