import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

LOG_DATA = config.get("S3","LOG_DATA")
SONG_DATA = config.get("S3","SONG_DATA")
ARN = config.get("IAM_ROLE","ARN")
LOG_JSONPATH = config.get("S3","LOG_JSONPATH")

print(LOG_DATA)
print(SONG_DATA)
print(ARN)
print(LOG_JSONPATH)

# DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS staging_events"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs"
songplay_table_drop = "DROP TABLE IF EXISTS songplays"
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS songs"
artist_table_drop = "DROP TABLE IF EXISTS artists"
time_table_drop = "DROP TABLE IF EXISTS time"

# CREATE TABLES

staging_events_table_create= ("""
CREATE TABLE IF NOT EXISTS staging_events(
artist varchar DISTKEY,
auth varchar,
firstName varchar ,
gender varchar ,
iteminSession integer,
lastName varchar,
length float,
level varchar,
location varchar,
method varchar,
page varchar,
registration BIGINT,
sessionId integer,
song varchar,
status integer,
ts bigint,
userAgent varchar,
userId integer
)
""")

staging_songs_table_create = ("""
CREATE TABLE IF NOT EXISTS staging_songs(
num_songs integer,
artist_id varchar,
artist_latitude numeric,
artist_longitude numeric,
artist_location varchar,
artist_name varchar DISTKEY,
song_id varchar,
title varchar,
duration float,
year integer
)
""")

songplay_table_create = ("""
CREATE TABLE IF NOT EXISTS songplays(
songplay_ID integer IDENTITY(0,1) PRIMARY KEY, 
start_time timestamp NOT NULL SORTKEY, 
user_ID integer NOT NULL, 
level varchar, 
song_ID varchar NOT NULL, 
artist_ID varchar NOT NULL, 
session_ID integer, 
location varchar, 
user_agent varchar
)
""")

user_table_create = ("""
CREATE TABLE IF NOT EXISTS users(
user_ID integer PRIMARY KEY, 
first_name varchar, 
last_name varchar, 
gender varchar, 
level varchar
)
""")

song_table_create = ("""
CREATE TABLE IF NOT EXISTS songs(
song_ID varchar PRIMARY KEY, 
title varchar, 
artist_ID varchar, 
year integer, 
duration numeric
)
""")

artist_table_create = ("""
CREATE TABLE IF NOT EXISTS artists(
artist_ID varchar PRIMARY KEY, 
name varchar, 
location varchar, 
latitude numeric, 
longitude numeric
)
""")

time_table_create = ("""
CREATE TABLE IF NOT EXISTS time(
start_time timestamp PRIMARY KEY SORTKEY, 
hour integer, 
day integer, 
week integer, 
month integer, 
year integer, 
weekday integer
)
""")

# STAGING TABLES

staging_events_copy = ("""
copy staging_events from {}
    credentials 'aws_iam_role={}'
    compupdate off region 'us-west-2'
    format as json {};
""").format(LOG_DATA,ARN,LOG_JSONPATH)

staging_songs_copy = ("""
copy staging_songs from {}
    credentials 'aws_iam_role={}'
    compupdate off region 'us-west-2'
    format as json 'auto';
""").format(SONG_DATA,ARN)

# FINAL TABLES

songplay_table_insert = ("""
INSERT INTO songplays
(
start_time, user_ID, level, song_ID, artist_ID, session_ID, location, user_agent
) 
SELECT
(TIMESTAMP 'epoch' + se.ts/1000*INTERVAL '1 second') AS start_time, 
se.userId,
se.level,
ss.song_id,
ss.artist_id,
se.sessionId,
se.location,
se.userAgent
FROM staging_events se
JOIN staging_songs ss
ON se.artist = ss.artist_name
WHERE (se.page='NextSong') AND (se.ts IS NOT NULL) AND (ss.song_id IS NOT NULL) 
AND (ss.artist_id IS NOT NULL) AND (se.userId IS NOT NULL)
""")

user_table_insert = ("""
INSERT INTO users
(
user_ID, first_name, last_name, gender, level
) 
SELECT DISTINCT se.userId,
se.firstName,
se.lastName,
se.gender,
se.level
FROM staging_events se
WHERE se.userId IS NOT NULL
""")

song_table_insert = ("""
INSERT INTO songs
(
song_ID, title, artist_ID, year, duration
) 
SELECT DISTINCT ss.song_id,
ss.title,
ss.artist_id,
ss.year,
ss.duration
FROM staging_songs ss
WHERE ss.song_id IS NOT NULL
""")

artist_table_insert = ("""
INSERT INTO artists(
artist_ID, name,location , latitude, longitude
) 
SELECT DISTINCT ss.artist_id,
ss.artist_name,
ss.artist_location,
ss.artist_latitude,
ss.artist_longitude
FROM staging_songs ss
WHERE ss.artist_id IS NOT NULL
""")

time_table_insert = ("""
INSERT INTO time(
start_time, hour, day, week, month, year, weekday
) 
SELECT
(TIMESTAMP 'epoch' + se.ts/1000*INTERVAL '1 second') AS start_time, 
EXTRACT(hour from (TIMESTAMP 'epoch' 
+ se.ts/1000*INTERVAL '1 second')) as hour,
EXTRACT(day from (TIMESTAMP 'epoch' 
+ se.ts/1000*INTERVAL '1 second')) as day,
EXTRACT(week from (TIMESTAMP 'epoch' 
+ se.ts/1000*INTERVAL '1 second')) as week,
EXTRACT(month from (TIMESTAMP 'epoch' 
+ se.ts/1000*INTERVAL '1 second')) as month,
EXTRACT(year from (TIMESTAMP 'epoch' 
+ se.ts/1000*INTERVAL '1 second')) as year,
EXTRACT(DOW from (TIMESTAMP 'epoch' 
+ se.ts/1000*INTERVAL '1 second')) as DOW
FROM staging_events se
WHERE (se.page='NextSong') AND (se.ts IS NOT NULL)
""")

# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]
