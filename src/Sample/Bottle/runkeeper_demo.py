#!/usr/bin/env python
"""Demo Application for HealthGraph-API Python Library developed using Bottle 
fast, simple and lightweight WSGI micro web-framework for Python.

The configuration file runkeeper_demo.conf must be edited to set the client_id 
and client_secret. The client_id and client_secret is generated upon registration
in the Applications Portal of Health Graph (http://runkeeper.com/partner).

Running the demo: python runkeeper_demo.py
Point the web browser to the following URL: http://127.0.0.1:8000 """

import sys
import os
import time
from datetime import datetime, date, timedelta
import optparse
import ConfigParser
import bottle
import HealthGraphPackage
import HealthGraphPackage.Points
from beaker.middleware import SessionMiddleware
from Canvas import Line

__author__ = "Ali Onur Uyar"
__copyright__ = "Copyright 2012, Ali Onur Uyar"
__credits__ = []
__license__ = "GPL"
__version__ = "0.3.0"
__maintainer__ = "Ali Onur Uyar"
__email__ = "aouyar at gmail.com"
__status__ = "Development"


# Defaults
conf = {'baseurl': 'http://127.0.0.1:8000',
        'bindaddr': '127.0.0.1',
        'bindport': 8000,
        }
defaultConfFilename = 'runkeeper_demo.conf'


# Session Options
sessionOpts = {
    'session.type': 'file',
    'session.cookie_expires': 1800,
    'session.data_dir': '/tmp/cache/data',
    'session.lock_dir': '/tmp/cache/data',
    'session.auto': False,
}


class ConfigurationError(Exception):
    """Base classs for Configuration Errors"""
    pass


@bottle.route('/')
def index():
    sess = bottle.request.environ['beaker.session']
    if sess.has_key('rk_access_token'):
        bottle.redirect('/welcome')
    else:
        rk_auth_mgr = HealthGraphPackage.AuthManager(conf['client_id'], conf['client_secret'], 
                                          '/'.join((conf['baseurl'], 'login',)))
        rk_auth_uri = rk_auth_mgr.get_login_url()
        rk_button_img = rk_auth_mgr.get_login_button_url('blue', 'black', 300)
        return bottle.template('index.html', {'rk_button_img': rk_button_img,
                                              'rk_auth_uri': rk_auth_uri,})


@bottle.route('/login')
def login():
    sess = bottle.request.environ['beaker.session']
    code = bottle.request.query.get('code')
    if code is not None:
        rk_auth_mgr = HealthGraphPackage.AuthManager(conf['client_id'], conf['client_secret'], 
                                              '/'.join((conf['baseurl'], 'login',)))
        access_token = rk_auth_mgr.get_access_token(code)
        sess['rk_access_token'] = access_token
        sess.save()
        bottle.redirect('/welcome')
        

@bottle.route('/welcome')
def welcome():
    sess = bottle.request.environ['beaker.session']
    access_token = sess.get('rk_access_token')
    
    if access_token is not None:
        user = HealthGraphPackage.User(session=HealthGraphPackage.Session(access_token))
        profile = user.get_profile()
        records = user.get_records()

        act_iter = user.get_fitness_activity_iter()
        strength_act_iter = user.get_strength_activity_iter()
        weight_iter = user.get_weight_measurement_iter()
        
        points = HealthGraphPackage.Points.Points(act_iter,strength_act_iter,weight_iter)
        write_to_file(user, points)
        
#         total_points = points.get_total_points()
#         print("Total points for the past week was: " + str(total_points))

        activities = [act_iter.next() for _ in range(1)] 
        return bottle.template('welcome.html', 
                               profile=profile,
                               activities=activities, 
                               records=records.get_totals())
    else:
        bottle.redirect('/')


def write_to_file(userToken, points):    
    #Overwrites myFile.txt if it exists cause of w flag. Creates if it does not
    path_to_FISS = "C:\Program Files (x86)\Steam\steamapps\common\Skyrim\Data\SKSE\Plugins\FISS\\"
    file_name = "Exercise_data.txt"
    
    first_import_date = ""
    previous_import_date = ""
    first_weeks_points = 0
    first_date = datetime.today()
    
    file_to_write = []

    if os.path.isfile(path_to_FISS + file_name):
        #TODO Read in only files later than the previous import date
        read_file = open(path_to_FISS + file_name)
        for i, line in enumerate(read_file):
            if i == 3:
                first_date = line
                first_date_in_format = first_date[20:24] + first_date[26:28]
                first_date = datetime.strptime(first_date_in_format, "%d%m%y")
                first_import_date = "" +  str("%02d" %first_date.day) + str("%02d" %first_date.month) + str(first_date.year)
            if i == 4:
                previous_import_date = line
                previous_import_date = previous_import_date[19:27]
        read_file.close()
    else:
        first_date = datetime.today()
        first_import_date = time.strftime("%d%m%Y")
        
#     If no previous import date found, import exercises from the first of this month
#     Else use what is in the file
    previous_import_date_object = date(date.today().year, date.today().month, 1)
    if previous_import_date != "":
        previous_import_date_object = datetime.strptime(previous_import_date, "%d%m%Y").date()
        
    file_to_write.append("<fiss><Header><Version>1.2</Version><ModName>P4P</ModName></Header>\n<Data>\n\n")
    todays_date = time.strftime("%d%m%Y")
    file_to_write.append("<First_import_date> " + first_import_date + " </First_import_date> \n")
    file_to_write.append("<Last_update_data> " + todays_date + " </Last_update_data> \n\n")

    one_week_from_first_import = (first_date + timedelta(days = 7)).date()
    
    #Format each exercise and add it to file
    #May want to create method to format strings as it's mostly boilerplate code
    index = 1
    fitness_act_iter = userToken.get_fitness_activity_iter()
    sport_exercises = []
    for exercise in fitness_act_iter:
        exercise_date = exercise.get("start_time").date()
        
        if previous_import_date_object <= exercise_date:
            exercise_type = HealthGraphPackage.Points.get_exer_name(exercise)
                
            exercise_points = points.get_points(exercise)
            if exercise_date <= one_week_from_first_import:
                first_weeks_points += exercise_points    
                
            if HealthGraphPackage.Points.get_type(exercise) != 'Other':
                fitness_exercise = "<fitness_exercise " + str(index) + "> "
                fitness_exercise += "<type> " + exercise_type + " </type> "
                fitness_exercise += "<points> " + str(exercise_points) + " </points> "
                fitness_exercise += "<start_time> " + str(exercise_date) + " </start_time> "
                fitness_exercise += "</fitness_exercise " + str(index) + ">"
                file_to_write.append(fitness_exercise + "\n")
                index += 1
            else:
                sport_exercises.append(exercise)
    file_to_write.append("\n")
    
    index = 1
    for exercise in sport_exercises:
        exercise_type = HealthGraphPackage.Points.get_exer_name(exercise)
        
        exercise_points = points.get_points(exercise)
        if exercise_date <= one_week_from_first_import:
            first_weeks_points += exercise_points

        sport_exercise = "<sport_exercise " + str(index) + "> "
        sport_exercise += "<type> " + exercise_type + " </type> "
        sport_exercise += "<points> " + str(exercise_points) + " </points> "
        sport_exercise += "<start_time> " + str(exercise_date) + " </start_time> "
        sport_exercise += "</sport_exercise " + str(index) + ">"
        file_to_write.append(sport_exercise + "\n")
        index += 1
    file_to_write.append("\n")
    
    index = 1
    strength_act_iter = userToken.get_strength_activity_iter()
    for exercise in strength_act_iter:
        exercise_date = exercise.get("start_time").date()
        
        if previous_import_date_object <= exercise_date:
            exercise_type = HealthGraphPackage.Points.get_exer_name(exercise)
            
            exercise_points = points.get_points(exercise)
            if exercise_date <= one_week_from_first_import:
                first_weeks_points += exercise_points
            
            strength_exercise = "<strength_exercise " + str(index) + "> "
            strength_exercise += "<type> " + exercise_type + " </type> "
            strength_exercise += "<points> " + str(exercise_points) + " </points> "
            strength_exercise += "<start_time> " + str(exercise_date) + " </start_time> "
            strength_exercise += "</strength_exercise " + str(index) + ">"
            file_to_write.append(strength_exercise + "\n")
            index += 1
    
    file_to_write.append("\n")
    file_to_write.insert(2, "<First week points> " + str(first_weeks_points) + " </First week points>\n")
    file_to_write.append("\n")
    file_to_write.append("\n</Data>\n</fiss>")
    
    with open(path_to_FISS + file_name, "w") as fwrite:
        for line in file_to_write:
            fwrite.write(line)
    
    print("Write to file method complete")
    

@bottle.route('/logout')
def logout():
    sess = bottle.request.environ['beaker.session']
    sess.delete()
    bottle.redirect('/')
    
    
@bottle.route('/view_access_token')
def view_access_token():
    sess = bottle.request.environ['beaker.session']
    access_token = sess.get('rk_access_token')
    if access_token is not None:
        remote_addr = bottle.request.get('REMOTE_ADDR')
        return bottle.template('access_token.html',
                               remote_addr=remote_addr,
                               access_token=(access_token 
                                             if remote_addr == '127.0.0.1'
                                             else None))
    else:
        bottle.redirect('/')
    

def parse_cmdline(argv=None):
    """Parse command line options.
    
    @param argv: List of command line arguments. If None, get list from system.
    @return:     Tuple of Option List and Argument List.
    
    """
    parser = optparse.OptionParser()
    parser.add_option('-c', '--conf', help='Configuration file path.',
                      dest='confpath',default=None)
    parser.add_option('-p', '--bindport',
                      help='Bind to TCP Port. (Default: %d)' % conf['bindport'],
                      dest='bindport', type='int', default=None, action='store')
    parser.add_option('-b', '--bindaddr',
                      help='Bind to IP Address. (Default: %s)' % conf['bindaddr'],
                      dest='bindaddr', default=None, action='store')
    parser.add_option('-u', '--baseurl', 
                      help='Base URL. (Default: %s)' % conf['baseurl'],
                      dest='baseurl', default=None, action='store')
    parser.add_option('-D', '--devel', help='Enable development mode.',
                      dest='devel', default=False, action='store_true')
    if argv is None:
        return parser.parse_args()
    else:
        return parser.parse_args(argv[1:])
    
     
def parse_conf_files(conf_paths):
    """Parse the configuration file and return dictionary of configuration 
    options.
    
    @param conf_paths: List of configuration file paths to parse.
    @return:           Dictionary of configuration options.
    
    """
    conf_file = ConfigParser.RawConfigParser()
    conf_read = conf_file.read(conf_paths)
    conf = {}
    try:
        if conf_read:
            conf['client_id'] = conf_file.get('runkeeper', 'client_id')
            conf['client_secret'] = conf_file.get('runkeeper', 'client_secret')
            if conf_file.has_option('runkeeper', 'bindport'):
                conf['bindport'] = conf_file.getint('runkeeper', 'bindport')
            if conf_file.has_option('runkeeper', 'bindaddr'):
                conf['bindaddr'] = conf_file.get('runkeeper', 'bindaddr')
            if conf_file.has_option('runkeeper', 'baseurl'):
                conf['baseurl'] = conf_file.get('runkeeper', 'baseurl')
            return conf
    except ConfigParser.Error:
        raise ConfigurationError("Error parsing configuration file(s): %s\n" 
                                 % sys.exc_info()[1])
    else:
        raise ConfigurationError("No valid configuration file (%s) found." 
                                 % defaultConfFilename)


def main(argv=None):
    """Main Block - Configure and run the Bottle Web Server."""
    cmd_opts = parse_cmdline(argv)[0]
    if cmd_opts.confpath is not None:
        if os.path.exists(cmd_opts.confpath):
            conf_paths = [cmd_opts.confpath,]
        else:
            return "Configuration file not found: %s" % cmd_opts.confpath
    else:
        conf_paths = [os.path.join(path, defaultConfFilename) 
                      for path in ('/etc', '.',)]
    try:
        conf.update(parse_conf_files(conf_paths))
    except ConfigurationError:
        return(sys.exc_info()[1])
    if cmd_opts.bindport is not None:
        conf['bindport'] = cmd_opts.bindport
    if cmd_opts.bindaddr is not None:
        conf['bindaddr'] = cmd_opts.bindaddr
    if cmd_opts.baseurl is not None:
        conf['baseurl'] = cmd_opts.baseurl
    if cmd_opts.devel:
        from bottle import debug
        debug(True)
    app = SessionMiddleware(bottle.app(), sessionOpts)
    bottle.run(app=app, host=conf['bindaddr'], port=conf['bindport'], 
               reloader=cmd_opts.devel)
    #

if __name__ == "__main__":
    sys.exit(main())