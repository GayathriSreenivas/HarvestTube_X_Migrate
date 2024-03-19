import streamlit as st
import googleapiclient.discovery
import googleapiclient.errors
from pymongo import MongoClient
import mysql.connector
import pandas as pd
from datetime import datetime

mongo_uri = "mongodb://localhost:27017/"
client = MongoClient(mongo_uri)

database_name = "youtube"
db = client[database_name]

collection = db["channels"]

data_list = []
videodata_list = []
cmntsdata_list =[]

for data in collection.find({},{"_id":0,"channel_information":1}):
    data_list.append(data["channel_information"])
df = pd.DataFrame(data_list)

for videos in collection.find({},{"_id":0,"video_information":1}):
   for video_info in videos["video_information"]:
       date = video_info["video"]["PublishedAt"]
       original_datetime = datetime.fromisoformat(date.replace('Z', '+00:00'))
       formatted = original_datetime.strftime('%Y-%m-%d %H:%M:%S')
       video_data = {
           "Video id": video_info["video"]["Video id"],
           "Video name": video_info["video"]["Video name"],
           "Channel Id": video_info["video"]["Channel Id"],
           "Channel Name": video_info["video"]["Channel Name"],
           "Video description": video_info["video"]["Video description"],
           "PublishedAt": formatted,
           "View count": video_info["video"]["View count"],
           "Like count": video_info["video"]["Like count"],
           "Dislike count": video_info["video"]["Dislike count"],
           "Favorite count": video_info["video"]["Favorite count"],
           "Comment count": video_info["video"]["Comment count"],
           "Duration": video_info["video"]["Duration"],
           "Thumbnail": video_info["video"]["Thumbnail"],
           "Caption status": video_info["video"]["Caption status"]
       }
       videodata_list.append(video_data)
df1 = pd.DataFrame(videodata_list)

for comments in collection.find({},{"_id":0,"video_information":1}):
   for cmnt_info in comments["video_information"]:
       for cmnts in cmnt_info["video"]["Comments"]:
           if cmnts["comments"]=="Comments not available for this video":
               print("No availability")
           else:
               date = cmnts["comments"]["Comment Publish"]
               original_datetime = datetime.fromisoformat(date.replace('Z', '+00:00'))
               formatted = original_datetime.strftime('%Y-%m-%d %H:%M:%S')
               cmnt_data ={
                "Comment Id":cmnts["comments"]["Comment Id"],
                "Comment Text":cmnts["comments"]["Comment Text"],
                "Channel Id":cmnts["comments"]["Channel Id"],
                "Channel name":cmnts["comments"]["Channel Name"],
                "Video Id":cmnts["comments"]["Video Id"],
                "Comment Author":cmnts["comments"]["Comment Author"],
                "Comment Publish":formatted
                }
               cmntsdata_list.append(cmnt_data)

df2 = pd.DataFrame(cmntsdata_list)

api_key = "AIzaSyDjSSfpid_d5VMiZRn-2V481lky5vjsn5o"
api_service_name = "youtube"
api_version = "v3"

youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey = api_key)

page_bg_img = """
<style>
[data-testid="stAppViewContainer"]{
background-image: url("https://img.freepik.com/premium-photo/gradient-blur-red-abstract-background_667461-807.jpg");
background-size: cover;
}
</style>
"""

sql_connection = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "gayathri@123",
    database = "youtube"
)

sqlcursor = sql_connection.cursor()

try:
    sqlcursor.execute("""
        create table if not exists channels(
            channel_id varchar(100) primary key,
            channel_name varchar(255),
            channel_views bigint,
            total_videos int,
            channel_description text,
            subscription_count bigint,
            playlist_id varchar(100)
            )""")
    sqlcursor.execute("""
        create table if not exists videos(
            video_id varchar(100) primary key,
            video_name varchar(255),
            channel_id varchar(100),
            channel_name varchar(255),
            video_description text,
            published_date datetime,
            view_count int,
            like_count int,
            dislike_count int,
            favorite_count int,
            comment_count int,
            duration varchar(50),
            thumbnail varchar(255),
            caption_status varchar(255),
            FOREIGN KEY (channel_id) REFERENCES channels(channel_id))"""
            )
    sqlcursor.execute("""
        create table if not exists comments(
            comment_id varchar(100) primary key,
            comment_text varchar(255),
            video_id varchar(100),
            channel_id varchar(100),
            channel_name varchar(255),
            comment_author varchar(255),
            comment_published_date datetime,
            FOREIGN KEY (video_id) REFERENCES videos(video_id))"""
            )
    sql_connection.commit()
except:
    print("tables already exists")


st.markdown(page_bg_img, unsafe_allow_html=True)

col1,col2 = st.columns([6,2])

url = "https://w7.pngwing.com/pngs/747/798/png-transparent-mysql-logo-mysql-database-web-development-computer-software-dolphin-marine-mammal-animals-text-thumbnail.png"
col2.image(url,width=50)

with col1:
    st.title(":rainbow[Youtube data harvesting]")

st.write("Migrating data from MongoDB to SQL")


option = collection.find({},{"_id":0,"channel_information":1})
dropdown_options = [item["channel_information"]["CHANNEL NAME"] for item in option]
default = None
selected_option = st.selectbox("Harvested data only will be shown here", dropdown_options, index=dropdown_options.index(default) if default else None)

for index,row in df.iterrows():
    if row["CHANNEL NAME"] == selected_option :
            print("channel id matched")
            insertion_query = """insert into channels(channel_id,
                                                      channel_name ,
                                                      channel_views,
                                                      total_videos ,
                                                      channel_description,
                                                      subscription_count,
                                                      playlist_id 
                                                      )values(%s,%s,%s,%s,%s,%s,%s)"""
            values=(row['CHANNEL ID'],
                    row['CHANNEL NAME'],
                    row['CHANNEL VIEWS'],
                    row['TOTAL VIDEOS'],
                    row['CHANNEL DESCRIPTION'],
                    row['SUBSCRIPTION COUNT'],
                    row['PLAYLIST ID'])

            try:
                sqlcursor.execute(insertion_query,values)
                sql_connection.commit()

            except mysql.connector.Error as e:
                print(f"Error:{e}")


for index,row in df1.iterrows():
    if row["Channel Name"] == selected_option :
            print("channel id matched")
            videoinsertion_query = """insert into videos(
                                                        video_id,
                                                        video_name,
                                                        channel_id,
                                                        channel_name,
                                                        video_description,
                                                        published_date,
                                                        view_count,
                                                        like_count,
                                                        dislike_count,
                                                        favorite_count,
                                                        comment_count,
                                                        duration,
                                                        thumbnail,
                                                        caption_status
                                                      )values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
            values=(row['Video id'],
                    row['Video name'],
                    row['Channel Id'],
                    row['Channel Name'],
                    row['Video description'],
                    row['PublishedAt'],
                    row['View count'],
                    row['Like count'],
                    row['Dislike count'],
                    row['Favorite count'],
                    row['Comment count'],
                    row['Duration'],
                    row['Thumbnail'],
                    row['Caption status'])

            try:
                sqlcursor.execute(videoinsertion_query,values)
                sql_connection.commit()
                print("values inserting")

            except mysql.connector.Error as e:
                print(f"Error:{e}")

for index,row in df2.iterrows():
    if row["Channel name"] == selected_option :
            print("channel id matched")
            cmntinsertion_query = """insert into comments(  comment_id,
                                                        comment_text,
                                                        video_id,
                                                        channel_id,
                                                        channel_name,
                                                        comment_author,
                                                        comment_published_date
                                                      )values(%s,%s,%s,%s,%s,%s,%s)"""
            values=(row['Comment Id'],
                    row['Comment Text'],
                    row['Video Id'],
                    row['Channel Id'],
                    row['Channel name'],
                    row['Comment Author'],
                    row['Comment Publish'])

            try:
                sqlcursor.execute(cmntinsertion_query,values)
                sql_connection.commit()

            except mysql.connector.Error as e:
                print(f"Error:{e}")

try:
    display = "SELECT channel_name FROM channels"
    sqlcursor.execute(display)
    rows = sqlcursor.fetchall()
    displaydf = pd.DataFrame(rows,columns=["CHANNEL NAME"])
    styled_df = displaydf.style.set_properties(**{'color': 'green'})

    st.markdown("### :green[Already Migrated Data]")
    st.write("Channels")
    st.table(styled_df)

except mysql.connector.Error as e:
    print(f"Error fetching data: {e}")

try:
    display = "SELECT channel_name,video_name FROM videos"
    sqlcursor.execute(display)
    rows = sqlcursor.fetchall()
    displaydf = pd.DataFrame(rows,columns=["channel", "video_name"])
    styled_df = displaydf.style.set_properties(**{'color': 'green'})

    st.write("Videos")
    st.table(styled_df)

except mysql.connector.Error as e:
    print(f"Error fetching data: {e}")

try:
    display = "SELECT channel_name,comment_text FROM comments"
    sqlcursor.execute(display)
    rows = sqlcursor.fetchall()
    displaydf = pd.DataFrame(rows,columns=["channel", "comment"])
    styled_df = displaydf.style.set_properties(**{'color': 'green'})

    st.write("Comments")
    st.table(styled_df)

except mysql.connector.Error as e:
    print(f"Error fetching data: {e}")


sqlcursor.close()
sql_connection.close()



