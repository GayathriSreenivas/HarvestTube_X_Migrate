import streamlit as st
import googleapiclient.discovery
import googleapiclient.errors
from pymongo import MongoClient
import pandas as pd
mongo_uri = "mongodb://localhost:27017/"
client = MongoClient(mongo_uri)

database_name = "youtube"
collect = client[database_name]

collection_names = collect.list_collection_names()
channel_collection = collect[collection_names[0]]
documents = channel_collection.find()

data_list=[]

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

st.markdown(page_bg_img, unsafe_allow_html=True)
col1, col2 = st.columns([6, 2])

url = "https://w7.pngwing.com/pngs/956/695/png-transparent-mongodb-original-wordmark-logo-icon-thumbnail.png"
col2.image(url,width=50)


with col1:
    st.title(":rainbow[Youtube data harvesting]")

st.write("Harvesting data to MongoDB")



option = st.selectbox(
    'Select an option:',
    ('Select any option',
     '1.Mashmool [UC0JKrFn8FJKawvIc3GBoiAg]',
     '2.Rajeswari Pachabotla Vlogs [UC2MvPcseboRfVVSnqxN3HTw]',
     '3.Hari Krishna [UCGyQcxW-5jmqTLHlijO4EgQ]',
     '4.Alex Miller [UCzOWDDAKrijRpAW4hX_-u1g]',
     '5.Framed Recipes [UCbX-QVVAOKKhFGISuSOUweA]',
     '6.Love n Food [UCryn96bWC1TRHIv1VgmPlQw]',
     '7.MSRelax [UCC_SP26qIYfMuQRNV2L6HsA]',
     '8.Worldering Around [UCpYYdG3SrFWlaREgU1cCNSw]',
     '9.Pathapadu Sreeharsha [UCCSnyEegYLT59gaA5M9LlGA]',
     '10.Sravani World [UCqYPp4Gnxehu1B06PnKb9jA]'
    )
)
if option == 'Select any option' :
    st.write("Select Something")
else :
    start = option.find("[") + 1
    end = option.find("]")
    option = option[start:end]

    allvideos = {}
    channel_id = option
    request = youtube.channels().list(
        part="snippet,contentDetails,statistics",
        id=channel_id
    )
    response = request.execute()

    if "items" in response:
        name = response["items"][0]["snippet"]["title"]
        playlist_id = response["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
        subscribers = response['items'][0]['statistics']['subscriberCount']
        totalvideocount = response['items'][0]['statistics']['videoCount']
        channel_id = response['items'][0]['id']
        channel_views = response['items'][0]['statistics']['viewCount']
        description = response['items'][0]['snippet']['description']

        channel_info = {'CHANNEL NAME': name, 'CHANNEL ID': channel_id, 'SUBSCRIPTION COUNT': subscribers, 'CHANNEL VIEWS': channel_views, 'CHANNEL DESCRIPTION': description , 'TOTAL VIDEOS': totalvideocount,'PLAYLIST ID': playlist_id}
        channel_info1 = {"channel_information" : channel_info}

        allvideos.update(channel_info1)

        totalcomments = []
        videos1 = []
        response1 = youtube.playlistItems().list(
            playlistId=playlist_id,
            part='snippet,contentDetails',
            maxResults=50).execute()

        for it in response1['items']:
            video_request = youtube.videos().list(
                part = 'snippet,statistics,contentDetails',
                id = it['contentDetails']['videoId']
            )
            video_response = video_request.execute()
            video_id = video_response['items'][0]['id']
            video_name = video_response['items'][0]['snippet']['localized']['title']
            video_description = video_response['items'][0]['snippet']['localized']['description']
            video_tags = video_response['items'][0]['snippet'].get('tags', [])
            video_publish = video_response['items'][0]['snippet']['publishedAt']
            view_count = video_response['items'][0]['statistics']['viewCount']
            like_count = video_response['items'][0]['statistics']['likeCount']
            dislike_count = video_response['items'][0]['statistics'].get('dislikeCount', 0)
            favorite_count = video_response['items'][0]['statistics']['favoriteCount']
            comment_count = video_response['items'][0]['statistics'].get('commentCount', 0)
            duration = video_response['items'][0]['contentDetails']['duration']
            thumbnail = video_response['items'][0]['snippet']['thumbnails']['default']['url']
            caption_status = video_response['items'][0]['contentDetails']['caption']

            cmnts = []
            try:
                request2 = youtube.commentThreads().list(
                    part="snippet",
                    videoId=video_id,
                    maxResults=100
                )
                response2 = request2.execute()

                for item in response2['items']:
                    cmt = 1
                    comment_id = item['id']
                    comment_text = item['snippet']['topLevelComment']['snippet']['textDisplay']
                    comment_author = item['snippet']['topLevelComment']['snippet']['authorDisplayName']
                    comment_publish = item['snippet']['topLevelComment']['snippet']['publishedAt']
                    comments = {
                        'Comment Id': comment_id,
                        'Comment Text': comment_text,
                        'Channel Id': channel_id,
                        'Channel Name': name,
                        'Video Id': video_id,
                        'Comment Author': comment_author,
                        'Comment Publish': comment_publish
                    }
                    cmntdata = {"comments": comments}
                    cmnts.append(cmntdata)

            except googleapiclient.errors.HttpError as e:
                cmntdata = {"comments": 'Comments not available for this video'}
                cmnts.append(cmntdata)

            video_data = {
                'Video id': video_id,
                'Video name': video_name,
                'Channel Id':channel_id,
                'Channel Name':name,
                'Video description': video_description,
                'Tags': video_tags,
                'PublishedAt': video_publish,
                'View count': view_count,
                'Like count': like_count,
                'Dislike count': dislike_count,
                'Favorite count': favorite_count,
                'Comment count': comment_count,
                'Duration': duration,
                'Thumbnail': thumbnail,
                'Caption status': caption_status,
                'Comments': cmnts
            }
            videos = {"video": video_data}
            videos1.append(videos)
        vid = {"video_information" : videos1}
        allvideos.update(vid)

        if channel_collection.find_one(allvideos):
            st.write("Channel already exists")
        else:
            result = channel_collection.insert_one(allvideos)
            st.write("Data of the channel was harvested into the data lake")

st.markdown("### :green[Already Harvested Data]")

for data in channel_collection.find({},{"_id":0,"channel_information":1}):
    data_list.append(data["channel_information"])
df = pd.DataFrame(data_list)

styled_df = df.style.set_properties(**{'color': 'green'})
st.table(styled_df)

client.close()
