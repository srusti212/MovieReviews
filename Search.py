from tkinter import *
from tkinter.ttk import Separator, Combobox

from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")

############################# Checking if database already exists ####################
my_db_name = "ImdbRottenSearch"

db_names = client.list_database_names()
if my_db_name in db_names:
    print("Database exists..We are good to go")
    mydb = client[my_db_name]
else:
    print("Database does not exist !!! Populate database first before proceeding.")
    sys.exit()

################################# Global Variables ##################################

or_flag = 0
and_flag = 1

my_genre_list = list()
my_genre_movie_id = list()
and_my_genre_movie_id = list()
or_my_genre_movie_id = set()

selected_y1 = 1920
selected_y2 = 2011

year_movie_id_results = list()
year_movie_id = list()

my_country_list = list()
distinct_countries = list()
my_country_movie_id = list()
and_my_country_movie_id = list()
or_my_country_movie_id = set()

temp = 0

seleccion_country = tuple()
seleccion_cast = tuple()
seleccion_director = tuple()
seleccion_tag = tuple()

distinct_cast = list()
distinct_director = list()

distinct_tag_id = list()
distinct_tag_value = list()

my_cast_list = list()
distinct_cast = list()
my_cast_movie_id = list()
and_my_cast_movie_id = list()
or_my_cast_movie_id = set()

my_director_list = list()
distinct_director = list()
my_director_movie_id = list()
and_my_director_movie_id = list()
or_my_director_movie_id = set()

my_tag_list = list()
distinct_tags = list()
my_tags_value_tag_id = list()
my_tags_movie_id = list()
and_my_tags_movie_id = list()
or_my_tags_movie_id = set()

my_movie_list = list()
my_movie_id_list = list()

new_country_id_list = list()
new_cast_id_list = list()
new_director_id_list = list()
new_tags_id_list = list()
new_movies_id_list = list()

cast_condition_flag = 1
director_condition_flag = 1

sel_weight = 1
selected_tag_op = "="

my_user_id = list()

movie_details = []
movie_description = []

mystring = ""

######################################################################################################################


def update_country_facet(year_movie_id=[]):
    mycol = "movie_countries"
    countries_list.delete(0, 'end')
    global distinct_countries
    distinct_countries.clear()
    global my_country_movie_id
    my_country_movie_id.clear()
    for i in year_movie_id:
        for testy in mydb.movie_countries.find({'$and': [{"movieID": {'$eq': i}}, {"country": {'$nin': ["", None]}}]}):
            distinct_countries.append(testy["country"])
            my_country_movie_id.append(testy["movieID"])
    distinct_countries = set(distinct_countries)
    distinct_countries = list(distinct_countries)
    distinct_countries = sorted(distinct_countries)
    for c in distinct_countries:
        countries_list.insert(END, c)
    return my_country_movie_id


def selectMovie(event):
    text.delete(1.0, END)
    global movie_details
    seleccion = movie_results_list.curselection()
    movie_details.clear()
    for i in seleccion:
        entrada = movie_results_list.get(i)
        movie_details.append(entrada)
    for j in movie_details:
        print(j)
    global movie_description
    movie_description.clear()
    global mystring
    for i in movie_details:
        for testy in mydb.movies.find({"title": i}):
            movie_description.append(testy["rtAudienceNumRatings"])
            mystring = ""
            mystring = "\nID : " + str(testy["id"]) + "   Title : " + testy["title"] + "   Year : " + str(testy["year"]) + "   Average Rating : " + str(testy["rtAudienceRating"]) + "   Number of Ratings : " + str(testy["rtAudienceNumRatings"]) + "   Genre : "
            for k in mydb.movie_genres.find({"movieID": {'$eq': testy["id"]}}):
                mystring = mystring + k["genre"] + " "
            for l in mydb.movie_countries.find({"movieID": {'$eq': testy["id"]}}):
                mystring = mystring + "   Country : " + l["country"]
            text.insert(END, mystring)


def update_cast_facet(country_movie_id=[]):
    cast_list.delete(0, 'end')
    global distinct_cast
    distinct_cast.clear()
    global my_cast_movie_id
    my_cast_movie_id.clear()
    for i in country_movie_id:
        for testy in mydb.movie_actors.find({'$and': [{"movieID": {'$eq': i}}, {"actorName": {'$nin': ["", None]}}]}):
            distinct_cast.append(testy["actorName"])
            my_cast_movie_id.append(testy["movieID"])
    distinct_cast = set(distinct_cast)
    distinct_cast = list(distinct_cast)
    distinct_cast = sorted(distinct_cast)
    for c in distinct_cast:
        cast_list.insert(END, c)
    return my_cast_movie_id


def update_director_facet(cast_movie_id=[]):
    director_list.delete(0, 'end')
    global distinct_director
    distinct_director.clear()
    global my_director_movie_id
    my_director_movie_id.clear()
    for i in cast_movie_id:
        for testy in mydb.movie_directors.find({'$and': [{"movieID": {'$eq': i}}, {"directorName": {'$nin': ["", None]}}]}):
            distinct_director.append(testy["directorName"])
            my_director_movie_id.append(testy["movieID"])
    distinct_director = set(distinct_director)
    distinct_director = list(distinct_director)
    distinct_director = sorted(distinct_director)
    for c in distinct_director:
        director_list.insert(END, c)
    return my_director_movie_id


def update_tags_facet(d_movie_id=[]):
    global distinct_tag_id
    global distinct_tag_value
    global my_tags_movie_id
    tag_list.delete(0, 'end')

    ########################################## Fetching tag ids for fetched movie ids ##################################

    distinct_tag_id.clear()
    for i in d_movie_id:
        for testy in mydb.movie_tags.find({'$and': [{"movieID": {'$eq': i}}, {"tagID": {"$exists": True}}]}):
            distinct_tag_id.append(testy["tagID"])
            my_tags_movie_id.append(testy["movieID"])
    ########################################## Fetching tag ids for fetched movie ids ##################################

    distinct_tag_value.clear()
    for i in distinct_tag_id:
        for testy in mydb.tags.find({'$and': [{"id": {'$eq': i}}, {"value": {"$exists": True}}]}):
            distinct_tag_value.append(testy["value"])

    distinct_tag_value = set(distinct_tag_value)
    distinct_tag_value = list(distinct_tag_value)
    distinct_tag_value = sorted(distinct_tag_value)
    if len(distinct_tag_value) == 0:
        tag_list.insert(END, "No tags attached")
    else:
        for c in distinct_tag_value:
            tag_list.insert(END, c)
    return my_tags_movie_id


def update_movie_results(tags_list=[]):                     # Update Movie Results
    global my_movie_list
    my_movie_list.clear()
    movie_results_list.delete(0, 'end')

    for i in tags_list:
        for testy in mydb.movies.find({'$and': [{"id": {'$eq': i}}, {"title": {"$exists": True}}]}):
            my_movie_list.append(testy["title"])
            my_movie_id_list.append(testy["id"])
    my_movie_list = set(my_movie_list)
    my_movie_list = list(my_movie_list)
    for c in my_movie_list:
        movie_results_list.insert(END, c)
    return my_movie_id_list

######################################################################################################################


def selectedOperatorIs(event):                              # When Inter Attribute logical operator is selected
    selected = selectedOperator.get()
    if (selected) == "AND":
        global and_flag
        and_flag = 1
    else:
        global or_flag
        or_flag = 1
    print(selected)


def selectGenre(event):                                      # When Genre is selected from a list of resultant Genres
    global or_my_genre_movie_id
    seleccion = genre_list.curselection()
    my_genre_list.clear()
    for i in seleccion:
        entrada = genre_list.get(i)
        my_genre_list.append(entrada)
    print("\n")
    for j in my_genre_list:
        print(j)
    my_genre_movie_id.clear()
    for i in my_genre_list:
        for k in mydb.movie_genres.find({"genre": i}):
            my_genre_movie_id.append(k["movieID"])
    print(len(my_genre_movie_id))

    or_my_genre_movie_id.clear()
    or_my_genre_movie_id = set(my_genre_movie_id)
    or_my_genre_movie_id = list(or_my_genre_movie_id)

    if and_flag == 1:
        and_my_genre_movie_id.clear()
        for i in or_my_genre_movie_id:
            if my_genre_movie_id.count(i) == len(my_genre_list):
                and_my_genre_movie_id.append(i)
        print(len(and_my_genre_movie_id))

    if or_flag == 1:
        print(len(or_my_genre_movie_id))


def selectedYear1(event):                                       # When min limit for time period is selected from a list of resultant Tags
    global selected_y1
    selected_y1 = int(sel_year_1.get())
    print(str(selected_y1))


def selectedYear2(event):                                       # When max limit for time period is selected from a list of resultant Tags
    global selected_y2
    selected_y2 = int(sel_year_2.get())
    print(selected_y2)
    global selected_y1
    if selected_y2 < selected_y1:
        global temp
        temp = selected_y1
        selected_y1 = selected_y2
        selected_y2 = temp

    year_movie_id.clear()
    if and_flag == 1:
        for m in and_my_genre_movie_id:
            for t in mydb.movies.find(
                    {'$and': [{"id": {'$eq': m}}, {"year": {'$lte': selected_y2, '$gte': selected_y1}}]}):
                year_movie_id.append(t["id"])

    if or_flag == 1:
        for m in or_my_genre_movie_id:
            for t in mydb.movies.find(
                    {'$and': [{"id": {'$eq': m}}, {"year": {'$lte': selected_y2, '$gte': selected_y1}}]}):
                year_movie_id.append(t["id"])

    print(len(year_movie_id))

    global new_country_id_list                                       # Update other facets
    new_country_id_list.clear()
    new_country_id_list = update_country_facet(year_movie_id)
    global new_cast_id_list
    new_cast_id_list.clear()
    new_cast_id_list = update_cast_facet(new_country_id_list)
    global new_director_id_list
    new_director_id_list.clear()
    new_director_id_list = update_director_facet(new_cast_id_list)
    global new_tags_id_list
    new_tags_id_list.clear()
    new_tags_id_list = update_tags_facet(new_director_id_list)


def selectCountry(event):                                             # When Country is selected from a list of resultant Tags
    global or_my_country_movie_id
    global seleccion_country
    seleccion_country = countries_list.curselection()
    if len(seleccion_country) == 1:
        my_country_list.clear()
        for i in seleccion_country:
            entrada = countries_list.get(i)
            my_country_list.append(entrada)
        print("\n")
        for j in my_country_list:
            print(j)
        my_country_movie_id.clear()
        and_my_country_movie_id.clear()
        for m in year_movie_id:
            for j in my_country_list:
                for t in mydb.movie_countries.find({'$and': [{"movieID": {'$eq': m}}, {"country": j}]}):
                    my_country_movie_id.append(t["movieID"])
        print(len(my_country_movie_id))

    global new_cast_id_list
    new_cast_id_list.clear()
    new_cast_id_list = update_cast_facet(my_country_movie_id)
    global new_director_id_list
    new_director_id_list.clear()
    new_director_id_list = update_director_facet(my_country_movie_id)
    global new_tags_id_list
    new_tags_id_list.clear()
    new_tags_id_list = update_tags_facet(my_country_movie_id)
    global new_movies_id_list
    new_movies_id_list.clear()
    new_movies_id_list = update_movie_results(my_country_movie_id)


def selectCast(event):                                  # When Cast is selected from a list of resultant Cast
    global or_my_country_movie_id
    global seleccion_cast
    seleccion_cast = cast_list.curselection()

    my_cast_list.clear()
    for i in seleccion_cast:
        entrada = cast_list.get(i)
        my_cast_list.append(entrada)
    print("\n")
    for j in my_cast_list:
        print(j)
    my_cast_movie_id.clear()
    for m in my_country_movie_id:
        for j in my_cast_list:
            for t in mydb.movie_actors.find({'$and': [{"movieID": {'$eq': m}}, {"actorName": j}]}):
                my_cast_movie_id.append(t["movieID"])
    print(len(my_cast_movie_id))

    global or_my_cast_movie_id
    or_my_cast_movie_id.clear()
    or_my_cast_movie_id = set(my_cast_movie_id)
    or_my_cast_movie_id = list(or_my_cast_movie_id)

    if and_flag == 1:
        global cast_condition_flag
        cast_condition_flag = 1
        and_my_cast_movie_id.clear()
        for i in or_my_cast_movie_id:
            if my_cast_movie_id.count(i) == len(my_cast_list):
                and_my_cast_movie_id.append(i)
        print(len(and_my_cast_movie_id))

        global new_director_id_list
        new_director_id_list.clear()
        new_director_id_list = update_director_facet(and_my_cast_movie_id)
        global new_tags_id_list
        new_tags_id_list.clear()
        new_tags_id_list = update_tags_facet(and_my_cast_movie_id)
        global new_movies_id_list
        new_movies_id_list.clear()
        new_movies_id_list = update_movie_results(and_my_cast_movie_id)

    if or_flag == 1:
        cast_condition_flag = 0
        print(len(or_my_cast_movie_id))
        new_director_id_list.clear()
        new_director_id_list = update_director_facet(or_my_cast_movie_id)
        new_tags_id_list.clear()
        new_tags_id_list = update_tags_facet(or_my_cast_movie_id)
        new_movies_id_list.clear()
        new_movies_id_list = update_movie_results(or_my_cast_movie_id)


def selectDirector(event):                              # When Director is selected from a list of resultant Directors
    global or_my_director_movie_id
    global seleccion_director
    seleccion_director = director_list.curselection()

    my_director_list.clear()
    for i in seleccion_director:
        entrada = director_list.get(i)
        my_director_list.append(entrada)
    print("\n")
    for j in my_director_list:
        print(j)
    my_director_movie_id.clear()
    if cast_condition_flag == 1:
        for m in and_my_cast_movie_id:
                for j in my_director_list:
                    for t in mydb.movie_directors.find({'$and': [{"movieID": {'$eq': m}}, {"directorName": j}]}):
                        my_director_movie_id.append(t["movieID"])
    if cast_condition_flag == 0:
        for m in or_my_cast_movie_id:
                for j in my_director_list:
                    for t in mydb.movie_directors.find({'$and': [{"movieID": {'$eq': m}}, {"directorName": j}]}):
                        my_director_movie_id.append(t["movieID"])

    print(len(my_director_movie_id))

    global or_my_director_movie_id
    or_my_director_movie_id.clear()
    or_my_director_movie_id = set(my_director_movie_id)
    or_my_director_movie_id = list(or_my_director_movie_id)

    if and_flag == 1:
        global director_condition_flag
        director_condition_flag = 1
        and_my_director_movie_id.clear()
        for i in or_my_director_movie_id:
            if my_director_movie_id.count(i) == len(my_director_list):
                and_my_director_movie_id.append(i)
        print(len(and_my_director_movie_id))

        global new_tags_id_list
        new_tags_id_list.clear()
        new_tags_id_list = update_tags_facet(and_my_director_movie_id)
        global new_movies_id_list
        new_movies_id_list.clear()
        new_movies_id_list = update_movie_results(and_my_director_movie_id)

    if or_flag == 1:
        director_condition_flag = 0
        new_tags_id_list.clear()
        new_tags_id_list = update_tags_facet(or_my_director_movie_id)
        new_movies_id_list.clear()
        new_movies_id_list = update_movie_results(or_my_director_movie_id)


def selectTag(event):                           # When Tag is selected from a list of resultant Tags
    user_results_list.delete(0, 'end')
    global seleccion_tag
    seleccion_tag = tag_list.curselection()

    my_tag_list.clear()
    for i in seleccion_tag:
        entrada = tag_list.get(i)
        my_tag_list.append(entrada)
    print("\n")
    for j in my_tag_list:
        print(j)

    global my_tags_value_tag_id
    my_tags_value_tag_id.clear()
    for j in my_tag_list:
        for t in mydb.tags.find({"value": j}):
            my_tags_value_tag_id.append(t["id"])

    if director_condition_flag == 1:
        for m in my_tags_value_tag_id:
            if m not in and_my_director_movie_id:
                my_tags_value_tag_id.remove(m)

    if director_condition_flag == 0:
        for m in my_tags_value_tag_id:
            if m not in or_my_director_movie_id:
                my_tags_value_tag_id.remove(m)

    global my_tags_movie_id
    my_tags_movie_id.clear()
    if selected_tag_op == "=":
        for m in my_tags_value_tag_id:
            for t in mydb.movie_tags.find({'$and':[{"tagID": {'$eq': m}}, {"tagWeight": {'$eq': int(sel_weight)}}]}):
                my_tags_movie_id.append(t["movieID"])
    if selected_tag_op == ">":
        for m in my_tags_value_tag_id:
            for t in mydb.movie_tags.find({'$and':[{"tagID": {'$eq': m}}, {"tagWeight": {'$gt': int(sel_weight)}}]}):
                my_tags_movie_id.append(t["movieID"])
    if selected_tag_op == "<":
        for m in my_tags_value_tag_id:
            for t in mydb.movie_tags.find({'$and':[{"tagID": {'$eq': m}}, {"tagWeight": {'$lt': int(sel_weight)}}]}):
                my_tags_movie_id.append(t["movieID"])
    if selected_tag_op == ">=":
        for m in my_tags_value_tag_id:
            for t in mydb.movie_tags.find({'$and':[{"tagID": {'$eq': m}}, {"tagWeight": {'$gte': int(sel_weight)}}]}):
                my_tags_movie_id.append(t["movieID"])
    if selected_tag_op == "<":
        for m in my_tags_value_tag_id:
            for t in mydb.movie_tags.find({'$and':[{"tagID": {'$eq': m}}, {"tagWeight": {'$lte': int(sel_weight)}}]}):
                my_tags_movie_id.append(t["movieID"])
    global my_user_id
    my_user_id.clear()
    for k in my_tags_movie_id:
        for t in mydb.user_taggedmovies.find({"movieID": {'$eq': k}}):
            my_user_id.append(t["userID"])
    print(len(my_user_id))

    my_user_id = set(my_user_id)
    my_user_id = list(my_user_id)
    my_user_id = sorted(my_user_id)

    for c in my_user_id:
        user_results_list.insert(END, c)


def selectedWeight(event):                      # When Tag Weight comparison operator is selected
    global sel_weight
    sel_weight = sel_tag_weight.get()
    print(sel_weight)


def selectedTagOperator(event):                 # When Tag value is selected
    global selected_tag_op
    selected_tag_op = selected_tag_operator.get()
    print(selected_tag_op)


############################################# GUI ###########################################
root = Tk()
root.title('MovieLens10_RottenTomato_IMDB Search')
top_section = Canvas(root)
top_section.pack(side=TOP, fill=BOTH, expand=True)
top_section.config(background="#ffffff")

movie_attributes_canvas = Canvas(top_section)
movie_attributes_canvas.pack(side=LEFT, fill=BOTH, expand=True)

movie_attributes_label_canvas = Canvas(movie_attributes_canvas)
movie_attributes_label_canvas.pack(side=TOP, fill=BOTH, expand=True)

top_frame_left_top_title_label = Label(movie_attributes_label_canvas, text="Movie Attributes", fg="black", bg="#26A69A")
top_frame_left_top_title_label.pack(side=TOP, fill=BOTH, expand=True)

movie_attributes_body_canvas = Canvas(movie_attributes_canvas)
movie_attributes_body_canvas.pack(side=BOTTOM, fill=BOTH, expand=True)

movie_attributes_body_canvas_part_1 = Canvas(movie_attributes_body_canvas)
movie_attributes_body_canvas_part_1.pack(side=TOP, fill=BOTH, expand=True)

genre_year_country_canvas = Canvas(movie_attributes_body_canvas_part_1)
genre_year_country_canvas.pack(side=LEFT, fill=BOTH, expand=True)

############################### Genre  and Year ###############################

main_genre_year_canvas = Canvas(genre_year_country_canvas)
main_genre_year_canvas.pack(side=LEFT, fill=BOTH, expand=True)

main_genre_canvas = Canvas(main_genre_year_canvas)
main_genre_canvas.pack(side=TOP, fill=BOTH, expand=True)

genre_label = Label(main_genre_canvas, text="Genre *", fg="black", bg="#26A69A")
genre_label.pack(side=TOP, fill=X)

genre_list_canvas = Canvas(main_genre_canvas)
genre_list_canvas.pack(side=BOTTOM, fill=BOTH, expand=True)

main_year_canvas = Canvas(main_genre_year_canvas)
main_year_canvas.pack(side=BOTTOM, fill=BOTH, expand=True)

year_label = Label(main_year_canvas, text="Movie Year *", fg="black", bg="#26A69A")
year_label.pack(side=TOP, fill=X)

year_selection_canvas = Canvas(main_year_canvas)
year_selection_canvas.pack(side=BOTTOM, fill=BOTH, expand=True)

col_name = "movies"
try:
    if col_name in mydb.collection_names():
        mycol = mydb[col_name]
except IOError:
    print(col_name + " table does not exist")
    sys.exit()

sel_year_1 = StringVar(year_selection_canvas)
sel_year_1.set("1903")  # default value

year_1 = Combobox(year_selection_canvas, textvariable=sel_year_1)
all_years = []
for testy in mycol.find().distinct('year'):
    all_years.append(testy)

year_1['values'] = sorted(all_years, key=lambda x: int(x))
year_1.bind("<<ComboboxSelected>>", selectedYear1)
year_1.pack(side=TOP, fill=X)

sel_year_2 = StringVar(year_selection_canvas)
sel_year_2.set("1903")  # default value

year_2 = Combobox(year_selection_canvas, textvariable=sel_year_2)
year_2['values'] = sorted(all_years, key=lambda x: int(x))
year_2.bind("<<ComboboxSelected>>", selectedYear2)
year_2.pack(side=BOTTOM, fill=X)

############################### Country ###############################

country_canvas = Canvas(genre_year_country_canvas)
country_canvas.pack(side=RIGHT, fill=BOTH, expand=True)

countries_label = Label(country_canvas, text="Countries", fg="black", bg="#26A69A")
countries_label.pack(side=TOP, fill=X)

countries_list_canvas = Canvas(country_canvas)
countries_list_canvas.pack(side=BOTTOM, fill=BOTH, expand=True)

############################### Cast and Director ###############################

cast_director_tag_canvas = Canvas(movie_attributes_body_canvas_part_1)
cast_director_tag_canvas.pack(side=RIGHT, fill=BOTH, expand=True)

main_cast_director_canvas = Canvas(cast_director_tag_canvas)
main_cast_director_canvas.pack(side=LEFT, fill=BOTH, expand=True)

############################### Cast ###############################
main_cast_canvas = Canvas(main_cast_director_canvas)
main_cast_canvas.pack(side=TOP, fill=BOTH, expand=True)

cast_label = Label(main_cast_canvas, text="Cast", fg="black", bg="#26A69A")
cast_label.pack(side=TOP, fill=X)

cast_list_canvas = Canvas(main_cast_canvas)
cast_list_canvas.pack(side=BOTTOM, fill=BOTH, expand=True)

############################### Director ###############################
main_director_canvas = Canvas(main_cast_director_canvas)
main_director_canvas.pack(side=BOTTOM, fill=BOTH, expand=True)

director_label = Label(main_director_canvas, text="Directors", fg="black", bg="#26A69A")
director_label.pack(side=TOP, fill=X)

director_list_canvas = Canvas(main_director_canvas)
director_list_canvas.pack(side=BOTTOM, fill=BOTH, expand=True)

############################### Tags ###############################
tags_canvas = Canvas(cast_director_tag_canvas)
tags_canvas.pack(side=RIGHT, fill=BOTH, expand=True)

tag_label = Label(tags_canvas, text="Tags", fg="black", bg="#26A69A")
tag_label.pack(side=TOP, fill=X)

tag_list_canvas = Canvas(tags_canvas)
tag_list_canvas.pack(side=BOTTOM, fill=BOTH, expand=True)

######################  AND OR Selection ########################
movie_attributes_body_canvas_part_2 = Canvas(movie_attributes_body_canvas)
movie_attributes_body_canvas_part_2.pack(side=BOTTOM, fill=BOTH, expand=True)

selectedOperator = StringVar(movie_attributes_body_canvas_part_2)
selectedOperator.set('And')  # default value

Operator_label = Label(movie_attributes_body_canvas_part_2,
                       text="Search Between Attributes' Values With AND/OR Operator : ", fg="black", bg="#26A69A")
Operator_label.pack(side=LEFT, fill=X, padx=(100, 2))

w = Combobox(movie_attributes_body_canvas_part_2, values=['AND', 'OR'], textvariable=selectedOperator)
w.bind("<<ComboboxSelected>>", selectedOperatorIs)
w.pack(side=RIGHT, fill=X, padx=(2, 100))

######################  Returning Movie Results ########################
movie_results_canvas = Canvas(top_section)
movie_results_canvas.pack(side=RIGHT, fill=BOTH, expand=True)

movie_results_canvas_title_label = Label(movie_results_canvas, text="Movie Results", fg="black", bg="#26A69A")
movie_results_canvas_title_label.pack(side=TOP, fill=X)

movie_results_body_canvas = Canvas(movie_results_canvas)
movie_results_body_canvas.pack(side=BOTTOM, fill=BOTH, expand=True)

######################  Actual Query Plus Query Exec Buttons ########################

bottom_section = Canvas(root)
bottom_section.pack(side=BOTTOM, fill=BOTH, expand=True)

bottom_section_left = Canvas(bottom_section)
bottom_section_left.pack(side=LEFT, fill=BOTH, expand=True)

bottom_section_left_top = Canvas(bottom_section_left)
bottom_section_left_top.pack(side=TOP, fill=BOTH, expand=True)

text = Text(bottom_section_left_top, height=10)
text.pack(side=LEFT, fill=BOTH, expand=True)
scroll_query = Scrollbar(bottom_section_left_top)
scroll_query.pack(side=RIGHT, fill=Y)
scroll_query.config(command=text.yview)

bottom_section_left_bottom = Canvas(bottom_section_left)
bottom_section_left_bottom.pack(side=BOTTOM, fill=BOTH, expand=True)

bottom_section_left_bottom_left = Canvas(bottom_section_left_bottom)
bottom_section_left_bottom_left.pack(side=LEFT, fill=BOTH, expand=True)

Tag_weight_label = Label(bottom_section_left_bottom_left, text="Enter Weight Value : ", fg="black",
                         bg="#26A69A")
Tag_weight_label.pack(side=LEFT, fill=X, padx=(100, 0))


bottom_section_left_bottom_right = Canvas(bottom_section_left_bottom)
bottom_section_left_bottom_right.pack(side=RIGHT, fill=BOTH, expand=True)

bottom_section_left_bottom_right_top = Canvas(bottom_section_left_bottom_right)
bottom_section_left_bottom_right_top.pack(side=RIGHT, fill=BOTH, expand=True)

selected_tag_operator = StringVar(bottom_section_left_bottom_right_top)
selected_tag_operator.set('=')  # default value

Tag_operator_label = Label(bottom_section_left_bottom_right_top, text="Tag Weight Operator : ", fg="black",
                           bg="#26A69A")
Tag_operator_label.pack(side=LEFT, fill=X)

Tag_operator = Combobox(bottom_section_left_bottom_right_top, values=['=', '>', '<', '>=', '<='],
                        textvariable=selected_tag_operator)
Tag_operator.bind("<<ComboboxSelected>>", selectedTagOperator)
Tag_operator.pack(side=RIGHT, fill=X, padx=(5, 100))

bottom_section_left_bottom_right_bottom = Canvas(bottom_section_left_bottom_right)
bottom_section_left_bottom_right_bottom.pack(side=BOTTOM, fill=BOTH, expand=True)

tag_weight = StringVar(bottom_section_left_bottom_right_bottom)
tag_weight.set('1')  # default value

bottom_section_right = Canvas(bottom_section)
bottom_section_right.pack(side=RIGHT, fill=BOTH, expand=True)

bottom_section_right_label = Label(bottom_section_right, text="User Results", fg="black", bg="#26A69A")
bottom_section_right_label.pack(side=TOP, fill=X)

bottom_section_right_user_results = Canvas(bottom_section_right)
bottom_section_right_user_results.pack(side=BOTTOM, fill=BOTH, expand=True)

#############################  Scrollbars ############################

scrollbar_movie_results = Scrollbar(movie_results_body_canvas)
scrollbar_movie_results.pack(side=RIGHT, fill=Y)

scrollbar_user_results = Scrollbar(bottom_section_right_user_results)
scrollbar_user_results.pack(side=RIGHT, fill=Y)

scrollbar_genre = Scrollbar(genre_list_canvas)
scrollbar_genre.pack(side=RIGHT, fill=Y)

scrollbar_countries = Scrollbar(countries_list_canvas)
scrollbar_countries.pack(side=RIGHT, fill=Y)

scrollbar_cast = Scrollbar(cast_list_canvas)
scrollbar_cast.pack(side=RIGHT, fill=Y)

scrollbar_director = Scrollbar(director_list_canvas)
scrollbar_director.pack(side=RIGHT, fill=Y)

scrollbar_tags = Scrollbar(tag_list_canvas)
scrollbar_tags.pack(side=RIGHT, fill=Y)

###################### Facets Movie & Users Lists #################################
movie_results_list = Listbox(movie_results_body_canvas, yscrollcommand=scrollbar_movie_results.set,
                             selectmode=MULTIPLE)
for line in range(100):
    movie_results_list.insert(END, "Movie Result number " + str(line))

movie_results_list.bind('<<ListboxSelect>>', selectMovie)
movie_results_list.configure(exportselection=False)

user_results_list = Listbox(bottom_section_right_user_results, yscrollcommand=scrollbar_user_results.set, name='mylist',
                            selectmode=MULTIPLE)
for line in range(100):
    user_results_list.insert(END, "User Result number " + str(line))

################   Unique Genre Facet List ##############
col_name = "movie_genres"
try:
    if col_name in mydb.collection_names():
        mycol = mydb[col_name]
except IOError:
    print(col_name + " table does not exist")
    sys.exit()

distinct_genres = []
for testy in mycol.find({"genre": {'$nin': ["", None]}}).distinct('genre'):
    distinct_genres.append(testy)
    # print(testy)

distinct_genres = sorted(distinct_genres)

genre_list = Listbox(genre_list_canvas, yscrollcommand=scrollbar_genre.set, name='genre_list_name', selectmode=MULTIPLE)
for g in distinct_genres:
    genre_list.insert(END, g)

genre_list.bind('<<ListboxSelect>>', selectGenre)
genre_list.configure(exportselection=False)
# genre_list.bind('<FocusOut>', lambda e: genre_list.selection_clear(0, END))

################   Unique Countries Facet List ##############
col_name = "movie_countries"
try:
    if col_name in mydb.collection_names():
        mycol = mydb[col_name]
except IOError:
    print(col_name + " table does not exist")
    sys.exit()
distinct_countries.clear()
for testy in mycol.find({"country": {'$nin': ["", None]}}).distinct('country'):
    distinct_countries.append(testy)
    # print(testy)

distinct_countries = sorted(distinct_countries)

countries_list = Listbox(countries_list_canvas, yscrollcommand=scrollbar_countries.set, name='countries_list_name',
                         selectmode=SINGLE)
for c in distinct_countries:
    countries_list.insert(END, c)

countries_list.bind('<<ListboxSelect>>', selectCountry)
countries_list.configure(exportselection=False)

################   Unique Cast Facet List ##############
col_name = "movie_actors"
try:
    if col_name in mydb.collection_names():
        mycol = mydb[col_name]
except IOError:
    print(col_name + " table does not exist")
    sys.exit()

distinct_cast = []
for testy in mycol.find({"actorName": {'$nin': ["", None]}}).distinct('actorName'):
    distinct_cast.append(testy)
    # print(testy)

distinct_cast = sorted(distinct_cast)

cast_list = Listbox(cast_list_canvas, yscrollcommand=scrollbar_cast.set, name='cast_list_name', selectmode=MULTIPLE)
for c in distinct_cast:
    cast_list.insert(END, c)

cast_list.bind('<<ListboxSelect>>', selectCast)
cast_list.configure(exportselection=False)

################   Unique Director Facet List ##############

col_name = "movie_directors"
try:
    if col_name in mydb.collection_names():
        mycol = mydb[col_name]
except IOError:
    print(col_name + " table does not exist")
    sys.exit()

distinct_directors = []
for testy in mycol.find({"directorName": {'$nin': ["", None]}}).distinct('directorName'):
    distinct_directors.append(testy)

distinct_directors = sorted(distinct_directors)
director_list = Listbox(director_list_canvas, yscrollcommand=scrollbar_director.set, name='director_list_name',
                        selectmode=MULTIPLE)
for d in distinct_directors:
    director_list.insert(END, d)

director_list.bind('<<ListboxSelect>>', selectDirector)
director_list.configure(exportselection=False)

################   Unique Tags Facet List ##############
col_name = "tags"
try:
    if col_name in mydb.collection_names():
        mycol = mydb[col_name]
except IOError:
    print(col_name + " table does not exist")
    sys.exit()

distinct_tags = []
for testy in mycol.find({"value": {'$nin': ["", None]}}).distinct('value'):
    distinct_tags.append(testy)

# distinct_tags = sorted(distinct_tags)
tag_list = Listbox(tag_list_canvas, yscrollcommand=scrollbar_tags.set, name='tag_list_name', selectmode=MULTIPLE)
for t in distinct_tags:
    tag_list.insert(END, t)

tag_list.bind('<<ListboxSelect>>', selectTag)
tag_list.configure(exportselection=False)

################   Unique Tag Weights Facet List ##############
col_name = "movie_tags"
try:
    if col_name in mydb.collection_names():
        mycol = mydb[col_name]
except IOError:
    print(col_name + " table does not exist")
    sys.exit()

distinct_tagWeights = []
for testy in mycol.find().distinct('tagWeight'):
    distinct_tagWeights.append(testy)

distinct_tagWeights = sorted(distinct_tagWeights)

sel_tag_weight = StringVar(year_selection_canvas)
sel_tag_weight.set("1")  # default value

tag_weight_list = Combobox(bottom_section_left_bottom_left, textvariable=sel_tag_weight,
                           name='tagWeight_list_name')
tag_weight_list['values'] = sorted(distinct_tagWeights, key=lambda x: int(x))
tag_weight_list.bind("<<ComboboxSelected>>", selectedWeight)
tag_weight_list.pack(side=RIGHT, fill=X, padx=(5, 100))

########################################################
movie_results_list.pack(side=LEFT, fill=BOTH, expand=True)
scrollbar_movie_results.config(command=movie_results_list.yview)

user_results_list.pack(side=TOP, fill=BOTH, expand=True)
scrollbar_user_results.config(command=user_results_list.yview)

genre_list.pack(side=TOP, fill=BOTH, expand=True)
scrollbar_genre.config(command=genre_list.yview)

countries_list.pack(side=TOP, fill=BOTH, expand=True)
scrollbar_countries.config(command=countries_list.yview)

cast_list.pack(side=TOP, fill=BOTH, expand=True)
scrollbar_cast.config(command=cast_list.yview)

director_list.pack(side=TOP, fill=BOTH, expand=True)
scrollbar_director.config(command=director_list.yview)

tag_list.pack(side=TOP, fill=BOTH, expand=True)
scrollbar_tags.config(command=tag_list.yview)

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)  # not needed, this is the default behavior
root.rowconfigure(1, weight=1)
root.mainloop()
