from django.shortcuts import render
import psycopg2
import datetime


def prepare_fetched_movies(fetched_data):
    """
    prepare data fetched by scrapers

    Parameters
    -------
    fetched_data: list
        list of data fetched by scrapers
    """

    movies = []
    for r in fetched_data:
        place = r[4].replace("['", "").replace("}", "").replace("{", "").replace("']", "")
        date = r[6].replace("['", "").replace("}", "").replace("{", "").replace("']", "")
        time = r[7].replace("{", "").replace("}", "")

        movies.append({
            "title": r[1],
            "place": place,
            "date": date,
            "type": r[0],
            "address": r[5],
            "image": r[2],
            "time": time,
            "url": r[3]
        })
    return movies


def index(request):
    # get request parameters
    search_query = request.GET.get('movie')
    place = request.GET.get('place')
    type_ = request.GET.get('type')
    date_time = request.GET.get('datetime')
    date = date_time[:10] if date_time else ""
    time = date_time[11:-1] if date_time else ""

    today = str(datetime.date.today())

    # connect to the database
    db = psycopg2.connect(user='illya', database='events', password='i1l0l0y%a', host='localhost')
    cursor = db.cursor()

    # get a list of movies:
    # TODO: это нужно рефакторить!
    # создание запроса можно значительно упростить и всё это можно заменить на 20-30 строчек кода
    if search_query and date and place and type_ and time:
        # if a movie was requested, try to find it in the DB
        cursor.execute("SELECT event_types.name, events.title, events.image, events.url, places.name, places.address,"
                       " event_runs.data, event_runs.times FROM events "
                       "INNER JOIN event_runs ON event_runs.id_event = events.id "
                       "INNER JOIN places ON places.id = events.id "
                       "INNER JOIN event_types ON event_types.id = events.id "
                       "WHERE title LIKE '%" + search_query + "%' AND event_runs.data LIKE'%" + date + "%' AND places.name LIKE '%" + place + "%' AND event_types.name LIKE '%" + type_ + "%' AND event_runs.times LIKE '%" + time + "%'")
    elif date and search_query and place and time:
        cursor.execute("SELECT event_types.name, events.title, events.image, events.url, places.name, places.address,"
                       " event_runs.data, event_runs.times  FROM events "
                       "INNER JOIN event_runs ON event_runs.id_event = events.id "
                       "INNER JOIN places ON places.id = events.id "
                       "INNER JOIN event_types ON event_types.id = events.id "
                       "WHERE event_runs.data LIKE '%" + date + "%' AND title LIKE'%" + search_query + "%' AND places.name LIKE '%" + place + "%' AND event_runs.times LIKE '%" + time + "%'")
    elif search_query and place and type_ and time:
        cursor.execute("SELECT event_types.name, events.title, events.image, events.url, places.name, places.address,"
                       " event_runs.data, event_runs.times  FROM events "
                       "INNER JOIN event_runs ON event_runs.id_event = events.id "
                       "INNER JOIN places ON places.id = events.id "
                       "INNER JOIN event_types ON event_types.id = events.id "
                       "WHERE title LIKE '%" + search_query + "%' AND places.name LIKE '%" + place + "%' AND event_types.name LIKE '%" + type_ + "%' AND event_runs.times LIKE '%" + time + "%' AND event_runs.data>='" + today +"'")
    elif date and place and type_ and time:
        cursor.execute("SELECT event_types.name, events.title, events.image, events.url, places.name, places.address,"
                       " event_runs.data, event_runs.times  FROM events "
                       "INNER JOIN event_runs ON event_runs.id_event = events.id "
                       "INNER JOIN places ON places.id = events.id "
                       "INNER JOIN event_types ON event_types.id = events.id "
                       "WHERE event_runs.data LIKE '%" + date + "%' AND places.name LIKE'%" + place + "%' AND event_types.name LIKE '%" + type_ + "%' AND event_runs.times LIKE '%" + time + "%'")
    elif date and search_query and type_ and time:
        cursor.execute("SELECT event_types.name, events.title, events.image, events.url, places.name, places.address,"
                       " event_runs.data, event_runs.times  FROM events "
                       "INNER JOIN event_runs ON event_runs.id_event = events.id "
                       "INNER JOIN places ON places.id = events.id "
                       "INNER JOIN event_types ON event_types.id = events.id "
                       "WHERE event_runs.data LIKE '%" + date + "%' AND title LIKE'%" + search_query + "%' AND event_types.name LIKE '%" + type_ + "%'  AND event_runs.times LIKE '%" + time + "%'")
    elif date and type_ and search_query and place:
        cursor.execute("SELECT event_types.name, events.title, events.image, events.url, places.name, places.address,"
                       " event_runs.data, event_runs.times  FROM events "
                       "INNER JOIN event_runs ON event_runs.id_event = events.id "
                       "INNER JOIN places ON places.id = events.id "
                       "INNER JOIN event_types ON event_types.id = events.id "
                       "WHERE event_runs.data LIKE '%" + date + "%' AND event_types.name LIKE '%" + type_ + "%'  AND title LIKE '%" + search_query + "%'  AND places.name LIKE '%" + place + "%'")
    elif search_query and type_ and time:
        cursor.execute("SELECT event_types.name, events.title, events.image, events.url, places.name, places.address,"
                       " event_runs.data, event_runs.times  FROM events "
                       "INNER JOIN event_runs ON event_runs.id_event = events.id "
                       "INNER JOIN places ON places.id = events.id "
                       "INNER JOIN event_types ON event_types.id = events.id "
                       "WHERE title LIKE '%" + search_query + "%' AND event_types.name LIKE '%" + type_ + "%' AND event_runs.times LIKE '%" + time + "%' AND event_runs.data>='" + today +"'")
    elif place and type_ and time:
        cursor.execute("SELECT event_types.name, events.title, events.image, events.url, places.name, places.address,"
                       " event_runs.data, event_runs.times  FROM events "
                       "INNER JOIN event_runs ON event_runs.id_event = events.id "
                       "INNER JOIN places ON places.id = events.id "
                       "INNER JOIN event_types ON event_types.id = events.id "
                       "WHERE places.name LIKE '%" + place + "%' AND event_types.name LIKE '%" + type_ + "%' AND event_runs.times LIKE '%" + time + "%' AND event_runs.data>='" + today +"'")
    elif place and search_query and time:
        cursor.execute("SELECT event_types.name, events.title, events.image, events.url, places.name, places.address,"
                       " event_runs.data, event_runs.times  FROM events "
                       "INNER JOIN event_runs ON event_runs.id_event = events.id "
                       "INNER JOIN places ON places.id = events.id "
                       "INNER JOIN event_types ON event_types.id = events.id "
                       "WHERE places.name LIKE '%" + place + "%' AND title LIKE '%" + search_query + "%' AND event_runs.times LIKE '%" + time + "%' AND event_runs.data>='" + today +"'")
    elif place and date and time:
        cursor.execute("SELECT event_types.name, events.title, events.image, events.url, places.name, places.address,"
                       " event_runs.data, event_runs.times  FROM events "
                       "INNER JOIN event_runs ON event_runs.id_event = events.id "
                       "INNER JOIN places ON places.id = events.id "
                       "INNER JOIN event_types ON event_types.id = events.id "
                       "WHERE places.name LIKE '%" + place + "%' AND event_runs.data LIKE '%" + date + "%' AND event_runs.times LIKE '%" + time + "%'")
    elif search_query and date and time:
        cursor.execute("SELECT event_types.name, events.title, events.image, events.url, places.name, places.address,"
                       " event_runs.data, event_runs.times  FROM events "
                       "INNER JOIN event_runs ON event_runs.id_event = events.id "
                       "INNER JOIN places ON places.id = events.id "
                       "INNER JOIN event_types ON event_types.id = events.id "
                       "WHERE title LIKE '%" + search_query + "%' AND event_runs.data LIKE '%" + date + "%'  AND event_runs.times LIKE '%" + time + "%'")
    elif search_query and place and date:
        cursor.execute("SELECT event_types.name, events.title, events.image, events.url, places.name, places.address,"
                       " event_runs.data, event_runs.times  FROM events "
                       "INNER JOIN event_runs ON event_runs.id_event = events.id "
                       "INNER JOIN places ON places.id = events.id "
                       "INNER JOIN event_types ON event_types.id = events.id "
                       "WHERE title LIKE '%" + search_query + "%' AND event_runs.data LIKE '%" + date + "%' AND places.name LIKE '%" + place + "%'")
    elif place and type_ and search_query:
        cursor.execute("SELECT event_types.name, events.title, events.image, events.url, places.name, places.address,"
                       " event_runs.data, event_runs.times  FROM events "
                       "INNER JOIN event_runs ON event_runs.id_event = events.id "
                       "INNER JOIN places ON places.id = events.id "
                       "INNER JOIN event_types ON event_types.id = events.id "
                       "WHERE places.name LIKE '%" + place + "%' AND event_types.name LIKE '%" + type_ + "%' AND title LIKE '%" + search_query + "%' AND event_runs.data>='" + today +"'")
    elif type_ and place and date:
        cursor.execute("SELECT event_types.name, events.title, events.image, events.url, places.name, places.address,"
                       " event_runs.data, event_runs.times  FROM events "
                       "INNER JOIN event_runs ON event_runs.id_event = events.id "
                       "INNER JOIN places ON places.id = events.id "
                       "INNER JOIN event_types ON event_types.id = events.id "
                       "WHERE event_types.name LIKE '%" + type_ + "%' AND places.name LIKE '%" + place + "%' AND event_runs.data LIKE '%" + date + "%'")
    elif date and type_ and search_query:
        cursor.execute("SELECT event_types.name, events.title, events.image, events.url, places.name, places.address,"
                       " event_runs.data, event_runs.times  FROM events "
                       "INNER JOIN event_runs ON event_runs.id_event = events.id "
                       "INNER JOIN places ON places.id = events.id "
                       "INNER JOIN event_types ON event_types.id = events.id "
                       "WHERE event_runs.data LIKE '%" + date + "%' AND event_types.name LIKE '%" + type_ + "%' AND title LIKE '%" + search_query + "%' ")
    elif date and type_ and time:
        cursor.execute("SELECT event_types.name, events.title, events.image, events.url, places.name, places.address,"
                       " event_runs.data, event_runs.times  FROM events "
                       "INNER JOIN event_runs ON event_runs.id_event = events.id "
                       "INNER JOIN places ON places.id = events.id "
                       "INNER JOIN event_types ON event_types.id = events.id "
                       "WHERE event_types.name LIKE '%" + type_ + "%' AND event_runs.times LIKE '%" + time + "%' AND event_runs.data LIKE '%" + date + "%'")
    elif date and type_:
        cursor.execute("SELECT event_types.name, events.title, events.image, events.url, places.name, places.address,"
                       " event_runs.data, event_runs.times  FROM events "
                       "INNER JOIN event_runs ON event_runs.id_event = events.id "
                       "INNER JOIN places ON places.id = events.id "
                       "INNER JOIN event_types ON event_types.id = events.id "
                       "WHERE event_types.name LIKE '%" + type_ + "%' AND event_runs.data LIKE '%" + date + "%'")
    elif place and type_:
        cursor.execute("SELECT event_types.name, events.title, events.image, events.url, places.name, places.address,"
                       " event_runs.data, event_runs.times  FROM events "
                       "INNER JOIN event_runs ON event_runs.id_event = events.id "
                       "INNER JOIN places ON places.id = events.id "
                       "INNER JOIN event_types ON event_types.id = events.id "
                       "WHERE places.name LIKE '%" + place + "%' AND event_types.name LIKE '%" + type_ + "%' AND event_runs.data>='" + today +"'")
    elif type_ and search_query:
        cursor.execute("SELECT event_types.name, events.title, events.image, events.url, places.name, places.address,"
                       " event_runs.data, event_runs.times  FROM events "
                       "INNER JOIN event_runs ON event_runs.id_event = events.id "
                       "INNER JOIN places ON places.id = events.id "
                       "INNER JOIN event_types ON event_types.id = events.id "
                       "WHERE event_types.name LIKE '%" + type_ + "%' AND title LIKE '%" + search_query + "%' AND event_runs.data>='" + today + "'")
    elif type_ and time:
        cursor.execute("SELECT event_types.name, events.title, events.image, events.url, places.name, places.address,"
                       " event_runs.data, event_runs.times  FROM events "
                       "INNER JOIN event_runs ON event_runs.id_event = events.id "
                       "INNER JOIN places ON places.id = events.id "
                       "INNER JOIN event_types ON event_types.id = events.id "
                       "WHERE event_types.name LIKE '%" + type_ + "%' AND event_runs.times LIKE '%" + time + "%' AND event_runs.data>='" + today +"'")
    elif place and date:
        cursor.execute("SELECT event_types.name, events.title, events.image, events.url, places.name, places.address,"
                       " event_runs.data, event_runs.times  FROM events "
                       "INNER JOIN event_runs ON event_runs.id_event = events.id "
                       "INNER JOIN places ON places.id = events.id "
                       "INNER JOIN event_types ON event_types.id = events.id "
                       "WHERE event_runs.data LIKE '%" + date + "%' AND places.name LIKE '%" + place + "%'")
    elif search_query and place:
        cursor.execute("SELECT event_types.name, events.title, events.image, events.url, places.name, places.address,"
                       " event_runs.data, event_runs.times  FROM events "
                       "INNER JOIN event_runs ON event_runs.id_event = events.id "
                       "INNER JOIN places ON places.id = events.id "
                       "INNER JOIN event_types ON event_types.id = events.id "
                       "WHERE title LIKE '%" + search_query + "%' AND places.name LIKE '%" + place + "%' AND event_runs.data>='" + today +"'")
    elif place and time:
        cursor.execute("SELECT event_types.name, events.title, events.image, events.url, places.name, places.address,"
                       " event_runs.data, event_runs.times  FROM events "
                       "INNER JOIN event_runs ON event_runs.id_event = events.id "
                       "INNER JOIN places ON places.id = events.id "
                       "INNER JOIN event_types ON event_types.id = events.id "
                       "WHERE places.name LIKE '%" + place + "%' AND event_runs.times LIKE '%" + time + "%' AND event_runs.data>='" + today + "'")
    elif date and search_query:
        cursor.execute("SELECT event_types.name, events.title, events.image, events.url, places.name, places.address,"
                       " event_runs.data, event_runs.times  FROM events "
                       "INNER JOIN event_runs ON event_runs.id_event = events.id "
                       "INNER JOIN places ON places.id = events.id "
                       "INNER JOIN event_types ON event_types.id = events.id "
                       "WHERE event_runs.data LIKE '%" + date + "%' AND title LIKE '%" + search_query + "%' ")
    elif date and time:
        cursor.execute("SELECT event_types.name, events.title, events.image, events.url, places.name, places.address,"
                       " event_runs.data, event_runs.times  FROM events "
                       "INNER JOIN event_runs ON event_runs.id_event = events.id "
                       "INNER JOIN places ON places.id = events.id "
                       "INNER JOIN event_types ON event_types.id = events.id "
                       "WHERE event_runs.data LIKE '%" + date + "%'  AND event_runs.times LIKE '%" + time + "%'")
    elif search_query and time:
        cursor.execute("SELECT event_types.name, events.title, events.image, events.url, places.name, places.address,"
                       " event_runs.data, event_runs.times  FROM events "
                       "INNER JOIN event_runs ON event_runs.id_event = events.id "
                       "INNER JOIN places ON places.id = events.id "
                       "INNER JOIN event_types ON event_types.id = events.id "
                       "WHERE title LIKE '%" + search_query + "%' AND event_runs.times LIKE '%" + time + "%' AND event_runs.data>='" + today +"'")
    elif search_query:
        cursor.execute("SELECT event_types.name, events.title, events.image, events.url, places.name, places.address,"
                       " event_runs.data, event_runs.times  FROM events "
                       "INNER JOIN event_runs ON event_runs.id_event = events.id "
                       "INNER JOIN places ON places.id = events.id "
                       "INNER JOIN event_types ON event_types.id = events.id "
                       "WHERE title LIKE '%" + search_query + "%' AND event_runs.data>='" + today + "'")
    elif time:
        cursor.execute("SELECT event_types.name, events.title, events.image, events.url, places.name, places.address,"
                       " event_runs.data, event_runs.times  FROM events "
                       "INNER JOIN event_runs ON event_runs.id_event = events.id "
                       "INNER JOIN places ON places.id = events.id "
                       "INNER JOIN event_types ON event_types.id = events.id "
                       "WHERE event_runs.times LIKE '%" + time + "%' AND event_runs.data>='" + today + "'")
    elif type_:
        cursor.execute("SELECT event_types.name, events.title, events.image, events.url, places.name, places.address,"
                       " event_runs.data, event_runs.times  FROM events "
                       "INNER JOIN event_runs ON event_runs.id_event = events.id "
                       "INNER JOIN places ON places.id = events.id "
                       "INNER JOIN event_types ON event_types.id = events.id "
                       "WHERE event_types.name LIKE '%" + type_ + "%' AND event_runs.data>='" + today + "'")
    elif place:
        cursor.execute("SELECT event_types.name, events.title, events.image, events.url, places.name, places.address,"
                       " event_runs.data, event_runs.times  FROM events "
                       "INNER JOIN event_runs ON event_runs.id_event = events.id "
                       "INNER JOIN places ON places.id = events.id "
                       "INNER JOIN event_types ON event_types.id = events.id "
                       "WHERE places.name LIKE '%" + place + "%' AND event_runs.data>='" + today + "'")
    elif date:
        cursor.execute("SELECT event_types.name, events.title, events.image, events.url, places.name, places.address,"
                       " event_runs.data, event_runs.times  FROM events "
                       "INNER JOIN event_runs ON event_runs.id_event = events.id "
                       "INNER JOIN places ON places.id = events.id "
                       "INNER JOIN event_types ON event_types.id = events.id "
                       "WHERE event_runs.data LIKE '%" + date + "%'")
    else:
        # otherwise, return all movies today
        cursor.execute("SELECT event_types.name, events.title, events.image, events.url, places.name, places.address,"
                       " event_runs.data, event_runs.times  FROM events "
                       "INNER JOIN event_runs ON event_runs.id_event = events.id "
                       "INNER JOIN places ON places.id = events.id "
                       "INNER JOIN event_types ON event_types.id = events.id WHERE data>='" + today +"'"
                       " LIMIT 20")

    results = cursor.fetchall()
    db.close()

    movies = prepare_fetched_movies(results)

    return render(request, 'index.html', {'movies': movies, 'date': date if date else today})
