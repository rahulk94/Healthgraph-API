from HealthGraphPackage import Points
from datetime import datetime, timedelta
import os

class DataSyncObject:
    
    path_to_FISS = "C:\Program Files (x86)\Steam\steamapps\common\Skyrim\Data\SKSE\Plugins\FISS\\"
    file_name = "Exercise_data.txt"
    
    def __init__ (self, userToken):
        self.user_profile = userToken.get_profile()
        
        self.fitness_activity_iter = userToken.get_fitness_activity_iter()
        self.strength_activity_iter = userToken.get_strength_activity_iter()
        self.users_weight_iter = userToken.get_weight_measurement_iter()

        self.points_generator = Points.Points(self.fitness_activity_iter, self.strength_activity_iter, self.users_weight_iter)
    
    def sync(self):
        file_to_write = self.create_file_contents()
        self.write_file(file_to_write)
        print("Sync complete!")
        
    def create_file_contents(self):
        previous_file_data = []
        
        first_import_date = ""
        previous_import_date = ""
        first_weeks_points = 0
        first_weeks_points_not_found = True
        first_date = datetime.today()
     
        outstanding_strength_points = 0
        outstanding_fitness_points = 0
        outstanding_sport_points = 0
     
        if os.path.isfile(self.path_to_FISS + self.file_name):
            read_file = open(self.path_to_FISS + self.file_name)
            for i, line in enumerate(read_file):
                if i == 0:
                    #File being read has been written by FISS, therefore is all in one long line
                    try:
                        first_date_index = line.index("<First_import_date>")
                        first_date_in_format = line[first_date_index + 20:first_date_index + 46]
                        first_date = datetime.strptime(first_date_in_format, "%Y-%m-%d %H:%M:%S.%f")
                        # first_import_date = "" +  str("%02d" %first_date.day) + str("%02d" %first_date.month) + str(first_date.year)
     
                        first_week_points_start_index = line.index("<First week points>")
                        first_week_points_end_index = line.index("</First week points>")
                        first_weeks_points = line[first_week_points_start_index + 19: first_week_points_end_index]
                        if first_weeks_points != 0:
                            first_weeks_points_not_found = False
     
                        previous_import_date_index = line.index("<Last_update_date>")
                        previous_import_date = line[previous_import_date_index + 19: previous_import_date_index + 45]
     
                        outstanding_strength_points_start_index = line.index("<Outstanding_strength_points>")
                        outstanding_strength_points_end_index = line.index("</Outstanding_strength_points>")
                        outstanding_strength_points = line[outstanding_strength_points_start_index + 29:outstanding_strength_points_end_index]
                         
                        outstanding_fitness_points_start_index = line.index("<Outstanding_fitness_points>")
                        outstanding_fitness_points_end_index = line.index("</Outstanding_fitness_points>")
                        outstanding_fitness_points = line[outstanding_fitness_points_start_index + 28: outstanding_fitness_points_end_index]
     
                        outstanding_sport_points_start_index = line.index("<Outstanding_sport_points>")
                        outstanding_sport_points_end_index =  line.index("</Outstanding_sport_points>")
                        outstanding_sport_points = line[outstanding_sport_points_start_index + 26: outstanding_sport_points_end_index]
                    except ValueError:
                        print("File being read is from python not Skyrim")
                #File has been written by Python, therefore is nicely formatted into lines
                if i == 3:
                    first_date = line
                    first_date_in_format = first_date[20:46]
                    if first_date_in_format == " </Fst":
                        raise Exception("Please enter the first date the game was synced")
                    first_date = datetime.strptime(first_date_in_format, "%Y-%m-%d %H:%M:%S.%f")
                    first_import_date = "" +  str("%02d" %first_date.day) + str("%02d" %first_date.month) + str(first_date.year)
                if i == 4:
                    first_weeks_points_str = line
                    index = first_weeks_points_str.index("</First week points>") - 1
                    first_weeks_points_str = line[20:index]
                    first_weeks_points = int(first_weeks_points_str)
                    if first_weeks_points != 0:
                        first_weeks_points_not_found = False
                if i == 5:
                    previous_import_date = line
                    previous_import_date = previous_import_date[19:45]
                if i == 7:
                    outstanding_strength_points = line
                    outstanding_strength_points_end_index = outstanding_strength_points.index("</Outstanding_strength_points>") - 1
                    outstanding_strength_points = line[30:outstanding_strength_points_end_index]
                if i == 8:
                    outstanding_fitness_points = line
                    outstanding_fitness_points_end_index = outstanding_fitness_points.index("</Outstanding_fitness_points>") - 1
                    outstanding_fitness_points = line[29:outstanding_fitness_points_end_index]
                if i == 9:
                    outstanding_sport_points = line
                    outstanding_sport_points_end_index = outstanding_sport_points.index("</Outstanding_sport_points>") - 1
                    outstanding_sport_points = line[27:outstanding_sport_points_end_index]
            read_file.close()
        else:
            first_date = datetime.now()
             
    #     If no previous import date found, import exercises from the first of this month
    #     Else use what is in the file
        previous_import_date_object = datetime.now()
        if previous_import_date != "":
            previous_import_date_object = datetime.strptime(previous_import_date, "%Y-%m-%d %H:%M:%S.%f")
     
        previous_file_data.append("<fiss><Header><Version>1.2</Version><ModName>P4P</ModName></Header>\n<Data>\n\n")
        previous_file_data.append("<First_import_date> " + str(first_date) + " </First_import_date> \n")
        previous_file_data.append("<Last_update_date> " + str(datetime.now()) + " </Last_update_date> \n\n")
     
        previous_file_data.append("<Outstanding_strength_points> " + str(outstanding_strength_points) + " </Outstanding_strength_points>\n")
        previous_file_data.append("<Outstanding_fitness_points> " + str(outstanding_fitness_points) + " </Outstanding_fitness_points>\n")
        previous_file_data.append("<Outstanding_sport_points> " + str(outstanding_sport_points) + " </Outstanding_sport_points>\n\n")
     
        one_week_from_first_import = (first_date + timedelta(days = 7))
        first_week_completed = datetime.now() > one_week_from_first_import
        previous_file_data.append("<First_week_completed> " + str(first_week_completed) + " </First_week_completed> \n\n")
        
        last_import_data = last_import_data_object(first_date, first_weeks_points, 
                                                    first_weeks_points_not_found,one_week_from_first_import, 
                                                    previous_import_date_object)
        
        newly_synced_exercise_data = self.sync_with_latest_exercises(last_import_data) 
        
        previous_file_data.insert(2, newly_synced_exercise_data[len(newly_synced_exercise_data) - 1])
        newly_synced_exercise_data.pop(len(newly_synced_exercise_data) - 1)
        
        file_to_write = previous_file_data + newly_synced_exercise_data
        
        return file_to_write


    def sync_with_latest_exercises(self, pdo):
        #Format each exercise and add it to file
        #May want to create method to format strings as it's mostly boilerplate code
        latest_exercises = []
        first_weeks_points = pdo.first_weeks_points
        
        index = 1
        sport_exercises = []
        for exercise in self.fitness_activity_iter:
            exercise_date = exercise.get("start_time")
     
            if (pdo.first_weeks_points_not_found and (exercise_date >= pdo.first_date)
                and (exercise_date <= pdo.one_week_from_first_import)):
                
                exercise_points = self.points_generator.get_points(exercise)
                first_weeks_points += exercise_points
     
            if pdo.previous_import_date_object <= exercise_date:
                exercise_type = Points.get_exer_name(exercise)
                exercise_points = self.points_generator.get_points(exercise)
                     
                if Points.get_type(exercise) != 'Other':
                    fitness_exercise = "<fitness_exercise " + str(index) + "> "
                    fitness_exercise += "<type> " + exercise_type + " </type> "
                    fitness_exercise += "<points> " + str(exercise_points) + " </points> "
                    fitness_exercise += "<start_time> " + str(exercise_date) + " </start_time> "
                    fitness_exercise += "</fitness_exercise " + str(index) + ">"
                    latest_exercises.append(fitness_exercise + "\n")
                    index += 1
                else:
                    sport_exercises.append(exercise)
        latest_exercises.append("\n")
         
        index = 1
        for exercise in sport_exercises:
            exercise_type = Points.get_exer_name(exercise)
            exercise_points = self.points_generator.get_points(exercise)
             
            sport_exercise = "<sport_exercise " + str(index) + "> "
            sport_exercise += "<type> " + exercise_type + " </type> "
            sport_exercise += "<points> " + str(exercise_points) + " </points> "
            sport_exercise += "<start_time> " + str(exercise_date) + " </start_time> "
            sport_exercise += "</sport_exercise " + str(index) + ">"
            latest_exercises.append(sport_exercise + "\n")
            index += 1
        latest_exercises.append("\n")
         
        index = 1
        for exercise in self.strength_activity_iter:
            exercise_date = exercise.get("start_time")
     
            if (pdo.first_weeks_points_not_found and (exercise_date >= pdo.first_date) 
                and (exercise_date <= pdo.one_week_from_first_import)):
                
                exercise_points = self.points_generator.get_points(exercise)
                first_weeks_points += exercise_points
     
            if pdo.previous_import_date_object <= exercise_date:
                exercise_type = Points.get_exer_name(exercise)
                exercise_points = self.points_generator.get_points(exercise)
                 
                strength_exercise = "<strength_exercise " + str(index) + "> "
                strength_exercise += "<type> " + exercise_type + " </type> "
                strength_exercise += "<points> " + str(exercise_points) + " </points> "
                strength_exercise += "<start_time> " + str(exercise_date) + " </start_time> "
                strength_exercise += "</strength_exercise " + str(index) + ">"
                latest_exercises.append(strength_exercise + "\n")
                index += 1
         
        latest_exercises.append("\n")
        latest_exercises.append("\n")
        latest_exercises.append("\n</Data>\n</fiss>")
        latest_exercises.append("<First week points> " + str(first_weeks_points) + " </First week points>\n")

        return latest_exercises

    def write_file(self, file_contents):
        with open(self.path_to_FISS + self.file_name, "w") as fwrite:
            for line in file_contents:
                fwrite.write(line)
        
        print("Write to file complete")


class last_import_data_object:
    def __init__(self, first_date, first_weeks_points, first_weeks_points_not_found,
                  one_week_from_first_import, previous_import_date_object):
        
        self.first_date = first_date
        self.first_weeks_points = first_weeks_points
        self.first_weeks_points_not_found = first_weeks_points_not_found
        self.one_week_from_first_import = one_week_from_first_import
        self.previous_import_date_object = previous_import_date_object
