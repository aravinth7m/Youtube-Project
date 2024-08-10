#Importing Needed Packages:
import googleapiclient.discovery
import sqlalchemy
from sqlalchemy import create_engine
import mysql.connector
import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
import matplotlib.pyplot as plt
import datetime

#API key Connection:
api_service_name = "youtube"
api_version = "v3"
api_key = "AIzaSyD8Uiza6rXyNqGd4U4XcpI_V9hMa-ogsQs"
youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey=api_key)

# Getting Channel Details:
def channel_data(channel_id):
    request = youtube.channels().list(part="snippet,contentDetails,statistics", id=channel_id)
    response = request.execute()
    for i in response.get('items', []):
        data = {
            "channel_Id": channel_id,
            "channel_name": i['snippet']['title'],
            "channel_dec": i['snippet']['description'],
            "Playlist_Id": i['contentDetails']['relatedPlaylists']['uploads'],
            "Video_count": i['statistics']['videoCount'],
            "sub_count": i['statistics']['subscriberCount'],
            "view_count": i['statistics']['viewCount'],
        }
        return data

# Getting Video Details:
def Get_Video_Ids(channel_id):
    video_ids = []
    response = youtube.channels().list(id=channel_id, part="contentDetails").execute()
    playlist_id = response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    NextPageToken = None

    while True:
        response_A = youtube.playlistItems().list(part='snippet', maxResults=50, playlistId=playlist_id, pageToken=NextPageToken).execute()
        for i in range(len(response_A['items'])):
            video_ids.append(response_A['items'][i]['snippet']['resourceId']['videoId'])
        NextPageToken = response_A.get('nextPageToken')
        if NextPageToken is None:
            break
    return video_ids, playlist_id

# Getting video information function:
def get_video_info(video_ids, playlistId, channel_name):
    video_data = []
    for video_info in video_ids:
        request = youtube.videos().list(part="snippet,contentDetails,statistics", id=video_info)
        response = request.execute()

        # To change duration time from ISO to Seconds
        def time_duration(t):    
            a = pd.Timedelta(t)
            b = str(a).split()[-1]
            return b

        for video in response["items"]:
            data = {
                "video_Id": video['id'],
                "Playlist_Id": playlistId,
                "video_name": video['snippet']['title'],
                "channel_name": channel_name,
                "video_Description": video['snippet'].get('description'),
                "Published_Date": video['snippet']['publishedAt'],
                "View_count": int(video['statistics'].get('viewCount', 0)),
                "Like_count": int(video['statistics'].get('likeCount', 0)),
                "Comments_count": int(video['statistics'].get('commentCount', 0)),
                "Favorite_Count": int(video['statistics'].get('favoriteCount', 0)),
                "Duration": time_duration(video['contentDetails']['duration']),
                "Thumbnail": video['snippet']['thumbnails']['default']['url'],
                "Caption_Status": video['contentDetails']['caption']
                
            }
            video_data.append(data)
    return video_data

# Get comment information function
def get_comment_info(video_ids):
    Comment_data = []
    try:
        for video_id in video_ids:
            request = youtube.commentThreads().list(part="snippet", videoId=video_id, maxResults=50)
            response = request.execute()
            for i in response['items']:
                data = {
                    "Comment_Id": i['snippet']['topLevelComment']['id'],
                    "video_Id": i['snippet']['topLevelComment']['snippet']['videoId'],
                    "Comment_text": i['snippet']['topLevelComment']['snippet']['textDisplay'],
                    "comment_author": i['snippet']['topLevelComment']['snippet']['authorDisplayName'],
                    "Comment_Published_at": i['snippet']['topLevelComment']['snippet']['publishedAt']
                }
                Comment_data.append(data)
    except Exception as e:
        print(f"Error fetching comments: {e}")
    return Comment_data

# Final data function
def finaldata(channel_id):
    Channel_Details = channel_data(channel_id)
    Video_Ids, playlist_id = Get_Video_Ids(channel_id)
    Video_Details = get_video_info(Video_Ids, playlist_id, Channel_Details['channel_name'])  # Pass channel_name here
    Comment_information = get_comment_info(Video_Ids)

    youtube_data = {
        "channel": Channel_Details,
        "videoid": Video_Ids,
        "video": Video_Details,
        "comment": Comment_information
    }
    return youtube_data

# Database connection
mydb = mysql.connector.connect(host="localhost", user="root", password="")
mycursor = mydb.cursor(buffered=True)
engine = create_engine("mysql+pymysql://{user}:{pw}@localhost/{db}".format(user="root", pw="", db="ytdatas"))

mycursor.execute('CREATE DATABASE IF NOT EXISTS ytdatas')
mycursor.execute('USE ytdatas')

# Create tables
mycursor.execute("""CREATE TABLE IF NOT EXISTS channel (
            channel_Id VARCHAR(255) PRIMARY KEY,
            channel_name VARCHAR(255),
            channel_dec TEXT,
            Playlist_Id  VARCHAR(255),
            Video_count  INT,
            sub_count  INT,  
            view_count INT)""")

mycursor.execute("""CREATE TABLE IF NOT EXISTS video(
                video_Id VARCHAR(255) PRIMARY KEY,
                Playlist_Id  VARCHAR(255),
                video_name VARCHAR(255),
                channel_name VARCHAR(255),
                video_Description TEXT, 
                Published_Date DATETIME,
                View_count INT,
                Like_count INT,
                Comments_count INT,
                Favorite_Count INT,
                Duration TIME,
                Thumbnail VARCHAR(255),
                Caption_Status VARCHAR(255)  
                )""")

mycursor.execute("""CREATE TABLE IF NOT EXISTS comment(
        Comment_Id VARCHAR(255),
        Video_Id VARCHAR(255),
        FOREIGN KEY(Video_Id) REFERENCES video(Video_Id),
        Comment_text TEXT,
        comment_author VARCHAR(255),
        Comment_Published_at DATETIME
                )""")

# Streamlit app
st.set_page_config(page_title='YouTube Data Harvesting and Warehousing',
                   layout='wide',
                   initial_sidebar_state='expanded',
                   menu_items={'About': '''This streamlit application was developed by M.Aravinth.
                                Contact_e_mail: aravinth7m@gmail.com'''})

with st.sidebar:
    selected = option_menu("Main Menu",
                           ["Home", "Data collection", "MYSQL Database", "Analysis using SQL", "Data Visualization"],
                           icons=["house", "cloud-upload", "database", "filetype-sql", "bar-chart-line"],
                           menu_icon="menu-up",
                           orientation="vertical")

if selected == "Home":
    st.title(':red[You]Tube :black[Data Harvesting & Warehousing]')
    st.subheader(':blue[Domain :] Social Media')
    st.subheader(':blue[Summary:]')
    st.markdown('''Develop a basic application using Streamlit for 
                the purpose of retrieving YouTube channel data by utilizing the YouTube API. 
                The acquired data should be stored in an SQL database managed by the XAMPP control panel, 
                allowing for querying using SQL. Additionally, visualize the data within the Streamlit application
                to reveal insights and trends associated with the YouTube channel's data''')
    st.subheader(':red[Skills Take Away :]')
    st.markdown(''':red[Python scripting,Data Collection,API integration,Data Management using SQL,Streamlit]''')
    st.subheader(':green[About :]')
    st.markdown('''Hello Everyone! I'm Aravinth, I’m a passionate life science graduate with a hunger for knowledge and 
                a drive to make a meaningful impact. My journey began in the world of biology, 
                where I explored intricate cellular processes and marveled at the wonders of life.
                 But now, I’m embarking on an exciting transition into the realm of data science. 
                My life science background has honed my analytical thinking.
                 Now, I’m translating that skill to dissect complex datasets.''')
    st.subheader(':blue[Contact:]')
    st.markdown('#### linkedin: https://www.linkedin.com/in/aravinth7m')
    st.markdown('#### Email : aravinth7m@gmail.com')

if selected == "Data collection":
    st.header('Youtube data Harvesting and Warehousing')
    st.subheader('Welcome !')
    channel_id = st.text_input('**Enter the Channel ID**')
    st.write('(**Collects data** by using :orange[channel id])')
    Get_data = st.button('**Collect Data**')

    if Get_data:
        finaloutput = finaldata(channel_id)
        st.success("Data collected and inserted into the database successfully!")

        channel_df = pd.DataFrame([finaloutput['channel']])
        video_df = pd.DataFrame(finaloutput['video'])
        comment_df = pd.DataFrame(finaloutput['comment'])

        try:
            channel_df.to_sql('channel', con=engine, if_exists='append', index=False)
        except Exception as e:
            st.error(f"Error inserting into Channel table: {e}")

        try:
            video_df.columns = [col.lower() for col in video_df.columns]
            video_df.to_sql('video', con=engine, if_exists='append', index=False)
        except Exception as e:
            st.error(f"Error inserting into Video table: {e}")

        try:
            comment_df.to_sql('comment', con=engine, if_exists='append', index=False)
        except Exception as e:
            st.error(f"Error inserting into Comment table: {e}")


#MYSQL Database Section
if selected == "MYSQL Database":

    question_tosql = st.selectbox('Select Question',
                            ['1. What are the names of all the videos and their corresponding channels?',
                                '2. Which channels have the most number of videos, and how many videos do they have?',
                                '3. What are the top 10 most viewed videos and their respective channels?',
                                '4. How many comments were made on each video, and what are their corresponding video names?',
                                '5. Which videos have the highest number of likes, and what are their corresponding channel names?',
                                '6. What is the total number of likes for each video, and what are their corresponding video names?',
                                '7. What is the total number of views for each channel, and what are their corresponding channel names?',
                                '8. What are the names of all the channels that have published videos in the year 2022?',
                                '9. What is the average duration of all videos in each channel, and what are their corresponding channel names?',
                                '10. Which videos have the highest number of comments, and what are their corresponding channel names?'],
                                key='collection_question')
    
    query = ""

    if question_tosql == '1. What are the names of all the videos and their corresponding channels?':
        query = """SELECT video.Video_name, channel.channel_name
                   FROM video
                   INNER JOIN channel ON video.Playlist_id = channel.Playlist_id"""
    
    if question_tosql == '2. Which channels have the most number of videos, and how many videos do they have?':
        query = """SELECT channel.channel_name, COUNT(video.video_Id) AS Video_Count
                   FROM channel
                   INNER JOIN video ON channel.Playlist_Id = video.Playlist_Id
                   GROUP BY channel.channel_Name
                   ORDER BY Video_Count DESC"""
    
    if question_tosql == '3. What are the top 10 most viewed videos and their respective channels?':
        query = """SELECT channel.channel_name, video.video_name, video.View_Count
                   FROM video
                   INNER JOIN channel ON video.Playlist_Id = channel.Playlist_Id
                   ORDER BY video.View_Count DESC
                   LIMIT 10"""
    
    if question_tosql == '4. How many comments were made on each video, and what are their corresponding video names?':
        query = """SELECT video.video_Name, COUNT(*) AS CommentCount
                   FROM video
                   INNER JOIN comment ON video.video_Id = comment.video_Id
                   GROUP BY video.video_Name"""
    
    if question_tosql == '5. Which videos have the highest number of likes, and what are their corresponding channel names?':
        query = """SELECT channel.channel_name, video.video_name, video.Like_Count
                   FROM video
                   INNER JOIN channel ON video.Playlist_Id = channel.Playlist_Id
                   ORDER BY video.Like_Count DESC"""
    
    if question_tosql == '6. What is the total number of likes for each video, and what are their corresponding video names?':
        query = """SELECT video.video_Name, MAX(video.Like_Count) AS Total_Likes
                   FROM video
                   GROUP BY video.video_name"""
    
    if question_tosql == '7. What is the total number of views for each channel, and what are their corresponding channel names?':
        query = """SELECT channel.channel_Name, SUM(video.view_Count) AS Total_Views
                   FROM channel
                   INNER JOIN video ON channel.Playlist_Id = video.Playlist_Id
                   GROUP BY channel.channel_name"""
    
    if question_tosql == '8. What are the names of all the channels that have published videos in the year 2022?':
        query = """SELECT channel.channel_name, video.video_name
                   FROM channel
                   INNER JOIN video ON channel.Playlist_Id = video.Playlist_Id
                   WHERE YEAR(video.Published_Date) = 2022"""
    
    if question_tosql == '9. What is the average duration of all videos in each channel, and what are their corresponding channel names?':
        query = """SELECT channel.channel_name, AVG(TIME_TO_SEC(video.Duration)) AS AvgDuration_sec
                   FROM channel
                   INNER JOIN video ON channel.Playlist_Id = video.Playlist_Id
                   GROUP BY channel.channel_name"""
    
    if question_tosql == '10. Which videos have the highest number of comments, and what are their corresponding channel names?':
        query = """SELECT channel.channel_name, video.video_name, video.comments_count 
                   FROM video
                   INNER JOIN channel ON video.Playlist_Id = channel.Playlist_Id
                   ORDER BY video.comments_count DESC"""
    
    if query:
        try:
            result = pd.read_sql(query, con=engine)
            st.dataframe(result)
        except Exception as e:
            st.error(f"Error executing query: {e}")



#Analysis using SQL Section:
if selected == "Analysis using SQL":
    st.header('SQL Analysis')
    st.subheader('Run custom SQL queries')

    # SQL Query input
    sql_query = st.text_area('Enter your SQL query here')

    if st.button('Execute SQL query'):
        try:
            result = pd.read_sql(sql_query, con=engine)
            st.dataframe(result)
        except Exception as e:
            st.error(f"Error executing query: {e}")

# Data Visualization Section:
import matplotlib.pyplot as plt

if selected == "Data Visualization":
    st.header('Data Visualization')
    st.subheader('Visualize the YouTube data')

    # Example Visualization: Number of videos per channel
    query = "SELECT channel_name, view_count FROM Channel"
    result = pd.read_sql(query, con=engine)
    
    fig, ax = plt.subplots()
    ax.bar(result['channel_name'], result['view_count'])
    ax.set_xlabel('Channel Name')
    ax.set_ylabel('view_count')
    ax.set_title('Number of view_count per Channel')

    # Rotate x-axis labels
    ax.set_xticklabels(result['channel_name'], rotation=45, ha="right")

    st.pyplot(fig)

#Sellected Channels For This Projects:

            #1.{SuGaR._.CuBe}==UCSs-CH4DMgpTxwX2IxuVItw
            #2.Indian jobs tamil==UCGTVPl2EP8lTwzjWb-YQHmA
            #3.Weeb Tamil==UCq3WUhQt9V8PrRBt49zNgEg
            #4.Mrs Merchant Navy Tamil==UCRvVNo5ZXbZLDChU-zZ9vEg
            #5.Dining with Dhoot==UC97oerjWs4Wmq3PL7SRN1tw
            #6.Deenul Aakhira==UC2mXwVqIk0JjIu91iTiiRNw
            #7.Christian Songs==UCM533r-_vS3lwsk1snNVUfA
            #8.Movie List==UCmjJffxnaCukc5oA8W-HwgQ
            #9.Famjam Vibes==UCNVHrxC96x_8JlYwAHKJ15Q
            #10.KAYAL VISION==UCFMBD8xDi-eQte9WsbinLYg
