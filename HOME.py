
import streamlit as st
import pandas as pd
import googleapiclient.discovery
import googleapiclient.errors

api_key = "AIzaSyDjSSfpid_d5VMiZRn-2V481lky5vjsn5o"
api_service_name = "youtube"
api_version = "v3"

youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey = api_key)

st.set_page_config(
    page_title = "Multipage App",
    page_icon = "👈"
)

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
st.write("Home")
channel_id = st.text_input("Enter a channel id")
request = youtube.channels().list(
        part = "snippet,contentDetails,statistics",
        id=channel_id
        )
response = request.execute()
if "items" in response:
        name = response["items"][0]["snippet"]["title"]
        playlist_id = response["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
        subscribers = response['items'][0]['statistics']['subscriberCount']
        totalvideocount = response['items'][0]['statistics']['videoCount']


        channel_info = {'CHANNEL NAME': name, 'SUBSCRIBERS': subscribers, 'TOTAL VIDEOS': totalvideocount, 'PLAYLIST ID': playlist_id}

        df = pd.DataFrame(channel_info, index=[1], columns=['CHANNEL NAME', 'SUBSCRIBERS', 'TOTAL VIDEOS', 'PLAYLIST ID'])
        styled_df = df.style.set_properties(**{'color': 'green'})
        st.table(styled_df)

        response1 = youtube.playlistItems().list(
                playlistId=playlist_id,
                part='snippet',
                maxResults=50).execute()
        videoids = []
        videotitles = []
        for item in response1['items']:
            videoids.append(item['snippet']['resourceId']['videoId'])
            videotitles.append(item['snippet']['title'])

            totalcomments = []
            for i in videoids:
                comments = []
                try:
                    request2 = youtube.commentThreads().list(
                            part="snippet",
                            videoId=i,
                            maxResults=100
                        )
                    response2 = request2.execute()
                    for item in response2['items']:
                        comments.append(item['snippet']['topLevelComment']['snippet']['textDisplay'])
                except googleapiclient.errors.HttpError as e:
                    comments.append("Comments for this video are disabled")
                totalcomments.append(comments)
        video_comments_dict = dict(zip(videotitles, totalcomments))

        video_comment_df = pd.DataFrame.from_dict(video_comments_dict, orient='index')
        st.write("VIDEO - COMMENTS")
        st.table(video_comment_df)
else:
    st.write("")

