import streamlit as st
import mysql.connector
import pandas as pd

page_bg_img = """
<style>
[data-testid="stAppViewContainer"]{
background-image: url("https://img.freepik.com/premium-photo/gradient-blur-red-abstract-background_667461-807.jpg");
background-size: cover;
}
</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)
st.title(":rainbow[Youtube data harvesting]")

sql_connection = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "gayathri@123",
    database = "youtube"
)

sqlcursor = sql_connection.cursor()

try:
    display = """UPDATE videos SET duration = CASE
        WHEN duration REGEXP '^PT[0-9]+M[0-9]+S$' THEN SEC_TO_TIME(TIME_TO_SEC(CONCAT('00:', SUBSTRING_INDEX(SUBSTRING_INDEX(duration, 'M', 1), 'T', -1), ':', SUBSTRING_INDEX(SUBSTRING_INDEX(duration, 'S', 1), 'M', -1))))
        ELSE '00:00:00' -- Set default duration for invalid values
    END;"""
    sqlcursor.execute(display)
    print("duration done successfully")

except mysql.connector.Error as e:
    print(f"Error fetching data: {e}")


option = st.selectbox(
    'Select an option:',
    ('Select any option',
     '1.What are the names of all videos and their corresponding channels?',
     '2.Which channels have more number of videos and how many videos do they have?',
     '3.What are the top 10 most viewed videos and their respective channels?',
     '4.How many comments were made on each video, What are their corresponding video names?',
     '5.Which videos have the highest number likes and what are their corresponding channel names?',
     '6.What is the total number of likes and dislikes for each video and what are their corresponding video names?',
     '7.What is the total number of views for each channel and what are their corresponding channel names?',
     '8.What are the names of all the channels that have published videos in the year 2022?',
     '9.What is the average duration of all videos in each channel and what are their corresponding channel names?',
     '10.Which videos have the highest number of comments and what are their corresponding channel names?'
    )
)

if option == 'Select any option' :
    st.write("Select Something")

elif option.startswith('1.'):
    try:
        display = "SELECT video_name,channel_name FROM videos"
        sqlcursor.execute(display)
        rows = sqlcursor.fetchall()
        displaydf = pd.DataFrame(rows, columns=["VIDEO NAME", "CHANNEL"])
        styled_df = displaydf.style.set_properties(**{'color': 'green'})

        st.markdown("#### :green[The names of all videos and their corresponding channels]")
        st.table(styled_df)

    except mysql.connector.Error as e:
        print(f"Error fetching data: {e}")

elif option.startswith('2.'):
    try:
        display = "select channel_name , total_videos from channels order by total_videos desc limit 5;"
        sqlcursor.execute(display)
        rows = sqlcursor.fetchall()
        displaydf = pd.DataFrame(rows, columns=["CHANNEL", "VIDEO COUNT"])
        styled_df = displaydf.style.set_properties(**{'color': 'green'})

        st.markdown("#### :green[Channels having more number of videos]")
        st.table(styled_df)

    except mysql.connector.Error as e:
        print(f"Error fetching data: {e}")

elif option.startswith('3.'):
    try:
        display = "select channel_name , video_name , view_count from videos order by view_count desc limit 10;"
        sqlcursor.execute(display)
        rows = sqlcursor.fetchall()
        displaydf = pd.DataFrame(rows, columns=["CHANNEL", "VIDEO NAME", "VIEW COUNT"])
        styled_df = displaydf.style.set_properties(**{'color': 'green'})

        st.markdown("#### :green[The top 10 most viewed videos and their respective channels]")
        st.table(styled_df)

    except mysql.connector.Error as e:
        print(f"Error fetching data: {e}")

elif option.startswith('4.'):
    try:
        display = "select comment_count , video_name , channel_name from videos;"
        sqlcursor.execute(display)
        rows = sqlcursor.fetchall()
        displaydf = pd.DataFrame(rows, columns=["COMMENT COUNT", "VIDEO NAME", "CHANNEL NAME"])
        styled_df = displaydf.style.set_properties(**{'color': 'green'})

        st.markdown("#### :green[Comments count made on each video and their names]")
        st.table(styled_df)

    except mysql.connector.Error as e:
        print(f"Error fetching data: {e}")

elif option.startswith('5.'):
    try:
        display = "select video_name, channel_name , like_count from videos order by like_count desc limit 5;"
        sqlcursor.execute(display)
        rows = sqlcursor.fetchall()
        displaydf = pd.DataFrame(rows, columns=["VIDEO", "CHANNEL NAME", "LIKE COUNT"])
        styled_df = displaydf.style.set_properties(**{'color': 'green'})

        st.markdown("#### :green[Videos having the highest number of likes and their corresponding channel names]")
        st.table(styled_df)

    except mysql.connector.Error as e:
        print(f"Error fetching data: {e}")

elif option.startswith('6.'):
    try:
        display = "select video_name, like_count, dislike_count from videos;"
        sqlcursor.execute(display)
        rows = sqlcursor.fetchall()
        displaydf = pd.DataFrame(rows, columns=["VIDEO", "TOTAL LIKES", "TOTAL DISLIKES"])
        styled_df = displaydf.style.set_properties(**{'color': 'green'})

        st.markdown("#### :green[The total number of likes and dislikes for each video and their corresponding video names]")
        st.table(styled_df)

    except mysql.connector.Error as e:
        print(f"Error fetching data: {e}")

elif option.startswith('7.'):
    try:
        display = "select channel_name , channel_views from channels order by channel_views desc;"
        sqlcursor.execute(display)
        rows = sqlcursor.fetchall()
        displaydf = pd.DataFrame(rows, columns=["CHANNEL NAME", "CHANNEL VIEWS"])
        styled_df = displaydf.style.set_properties(**{'color': 'green'})

        st.markdown("#### :green[the total number of views for each channel and their corresponding channel names]")
        st.table(styled_df)

    except mysql.connector.Error as e:
        print(f"Error fetching data: {e}")

elif option.startswith('8.'):
    try:
        display = "select distinct channel_name, video_name, published_date from videos where year(published_date) = 2022;"
        sqlcursor.execute(display)
        rows = sqlcursor.fetchall()
        displaydf = pd.DataFrame(rows, columns=["CHANNEL", "VIDEO NAME", "PUBLISHED DATE"])
        styled_df = displaydf.style.set_properties(**{'color': 'green'})

        st.markdown("#### :green[The names of all the channels that have published videos in the year 2022]")
        st.table(styled_df)

    except mysql.connector.Error as e:
        print(f"Error fetching data: {e}")

elif option.startswith('9.'):
    try:
        display = "SELECT channel_name , SEC_TO_TIME(AVG(TIME_TO_SEC(duration))) FROM videos GROUP BY channel_name;"
        sqlcursor.execute(display)
        rows = sqlcursor.fetchall()
        displaydf = pd.DataFrame(rows, columns=["CHANNEL", "AVERAGE DURATION"])
        styled_df = displaydf.style.set_properties(**{'color': 'green'})

        st.markdown("#### :green[The average duration of all videos in each channel and their corresponding channel names]")
        st.table(styled_df)

    except mysql.connector.Error as e:
        print(f"Error fetching data: {e}")

elif option.startswith('10.'):
    try:
        display = "select video_name,channel_name,comment_count from videos order by comment_count desc limit 5;"
        sqlcursor.execute(display)
        rows = sqlcursor.fetchall()
        displaydf = pd.DataFrame(rows, columns=["VIDEO", "CHANNEL", "COMMENT COUNT"])
        styled_df = displaydf.style.set_properties(**{'color': 'green'})

        st.markdown("#### :green[Videos having the highest number of comments and their corresponding channel names]")
        st.table(styled_df)

    except mysql.connector.Error as e:
        print(f"Error fetching data: {e}")


sqlcursor.close()
sql_connection.close()
