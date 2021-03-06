import flask
from flask import render_template, request
from app import app
import viz
import psycopg2

conn = psycopg2.connect(dbname='Open_Policing')
cur = conn.cursor()

def generateQuery(stop_date_MIN, stop_date_MAX, driver_gender, driver_age_MIN, driver_age_MAX, \
driver_race_TUPLE, violation_TUPLE, search_conducted, search_type_TUPLE, stop_outcome_TUPLE, \
officer_gender,  officer_age_MIN,  officer_age_MAX,  officer_race_TUPLE,  officer_rank_TUPLE,  out_of_state):
    add_where = True
    query = 'select county_name, count(*) from fl_stops'
    if stop_date_MIN is not None:
        query = query + ' where stop_date >= ' + str(stop_date_MIN)
        add_where = False
    if stop_date_MAX is not None:
        if add_where:
            query = query + ' where'
            add_where = False
        else:
            query = query + ' AND'
        query = query + ' stop_date <= ' + str(stop_date_MAX)
    if driver_gender is not None:
        if add_where:
            query = query + ' where'
            add_where = False
        else:
            query = query + ' AND'
        query = query + ' driver_gender IS ' + driver_gender
    if driver_age_MIN is not None:
        if add_where:
            query = query + ' where'
            add_where = False
        else:
            query = query + ' AND'
        query = query + ' driver_age >= ' + driver_age_MIN
    if driver_age_MAX is not None:
        if add_where:
            query = query + ' where'
            add_where = False
        else:
            query = query + ' AND'
        query = query + ' driver_age <= ' + driver_age_MAX
    if driver_race_TUPLE is not None:
        if add_where:
            query = query + ' where'
            add_where = False
        else:
            query = query + ' AND'
        query = query + ' driver_race IN ' + driver_race_TUPLE
    if violation_TUPLE is not None:
        if add_where:
            query = query + ' where'
            add_where = False
        else:
            query = query + ' AND'
        query = query + ' violation SIMILAR TO ' + '%(' + '|'.join(violation_TUPLE) + ')%'
    if search_conducted is not None:
        if add_where:
            query = query + ' where'
            add_where = False
        else:
            query = query + ' AND'
        query = query + ' search_conducted = ' + search_conducted
    if search_type_TUPLE is not None:
        if add_where:
            query = query + ' where'
            add_where = False
        else:
            query = query + ' AND'
        query = query + ' search_type IN ' + search_type_TUPLE
    if stop_outcome_TUPLE is not None:
        if add_where:
            query = query + ' where'
            add_where = False
        else:
            query = query + ' AND'
        query = query + ' stop_outcome IN ' + stop_outcome_TUPLE
    if officer_gender is not None:
        if add_where:
            query = query + ' where'
            add_where = False
        else:
            query = query + ' AND'
        query = query + ' officer_gender = ' + officer_gender
    if officer_age_MIN is not None:
        if add_where:
            query = query + ' where'
            add_where = False
        else:
            query = query + ' AND'
        query = query + ' officer_age >= ' + officer_age_MIN
    if officer_age_MAX is not None:
        if add_where:
            query = query + ' where'
            add_where = False
        else:
            query = query + ' AND'
        query = query + ' officer_age <= ' + officer_age_MAX
    if officer_race_TUPLE is not None:
        if add_where:
            query = query + ' where'
            add_where = False
        else:
            query = query + ' AND'
        query = query + ' officer_race IN ' + officer_race_TUPLE
    if officer_rank_TUPLE is not None:
        if add_where:
            query = query + ' where'
            add_where = False
        else:
            query = query + ' AND'
        query = query + ' officer_rank IN ' + officer_rank_TUPLE
    if out_of_state is not None:
        if add_where:
            query = query + ' where'
            add_where = False
        else:
            query = query + ' AND'
        query = query + ' out_of_state = ' + out_of_state
    query = query + ' group by county_name order by county_name;'
    cur.execute(query)
    counties_counts = cur.fetchall()
    counties_dict = dict(counties_counts)
    return counties_dict

@app.route('/')
@app.route('/index')
def index():
    stop_date_MIN = request.args.get('stop_date_MIN', default=None, type=str)
    stop_date_MAX = request.args.get('stop_date_MAX', default=None, type=str)
    driver_gender = request.args.get('driver_gender', default=None, type=str)
    driver_age_MIN = request.args.get('driver_age_MIN', default=None, type=int)
    driver_age_MAX = request.args.get('driver_age_MAX', default=None, type=int)
    driver_race_TUPLE = request.args.getlist('driver_race_TUPLE', type=str)
    violation_TUPLE = request.args.getlist('violation_TUPLE', type=str)
    search_conducted = request.args.get('search_conducted', default=None, type=bool)
    search_type_TUPLE = request.args.get('search_type', default=None, type=tuple)
    stop_outcome_TUPLE = request.args.getlist('stop_outcome_TUPLE', type=str)
    officer_gender = request.args.get('officer_gender', default=None, type=str)
    officer_age_MIN = request.args.get('officer_age_MIN', default=None, type=int)
    officer_age_MAX = request.args.get('officer_age_MAX', default=None, type=int)
    officer_race_TUPLE = request.args.getlist('officer_race_TUPLE', type=str)
    officer_rank_TUPLE = request.args.getlist('officer_rank_TUPLE', type=str)
    out_of_state = request.args.get('out_of_state', default=None, type=bool)
    count_dict = generateQuery(stop_date_MIN, stop_date_MAX, driver_gender, driver_age_MIN, driver_age_MAX, \
    driver_race_TUPLE, violation_TUPLE, search_conducted, search_type_TUPLE, stop_outcome_TUPLE, \
    officer_gender,  officer_age_MIN,  officer_age_MAX,  officer_race_TUPLE,  officer_rank_TUPLE,  out_of_state)
    viz.generate(count_dict)#viz.generate(count_dict)
    #return str(stop_date_MIN) + str(stop_date_MAX) + str(driver_gender) + str(driver_age_MIN) + str(driver_age_MAX) + \
    #    str(driver_race_TUPLE) + str(violation_TUPLE) + str(search_conducted) + str(search_type_TUPLE) + \
    #    str(stop_outcome_TUPLE) + str(officer_gender) + str(officer_age_MIN) + str(officer_age_MAX) + \
    #    str(officer_race_TUPLE) + str(officer_rank_TUPLE) + str(out_of_state)
    return render_template('index.html')

#@app.route('/results/map.html')
#def show_map():
#    return flask.send_file('/Users/duffrind/ncf/data/project1/police-traffic-stop-explorer/PoliceStops/app/results/map.html')
