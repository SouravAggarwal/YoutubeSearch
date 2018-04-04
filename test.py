from YTSearch.utils import YTsearch


def runTest():
    '''
    returns list of videos by channelId and Related videos of each .
    api_key:             your api key(required)
    channelId:           Youtube channel Id (required)
    max_results:         fetch No. of videos per page by given channelID(max Value =50),
                               lesser value will have less no. pages will have more no. of get requests
    max_related_result:  fetch n no. of related videos per page by given videoId (max Value =50)
    no_related_videos:   fetch n No. of related videos by each given video ID
    '''

    yt = YTsearch(api_key="AIzaSyDMY2r2vszk1YmId9ipfOnuvqsYHcNU87A", channelId="UCWN3xxRkmTPmbKwht9FuE5A")

    yt.max_results = 10
    yt.max_related_result = 10
    yt.no_related_videos = 2

    results = yt.get_results(type_='bychannel')
    print('\n')
    inp = input("Want to look at results? press y: ")
    if (inp.lower() == 'y'):
        print(results)

    print("\n")
    print(f"Fetching {yt.no_related_videos} Related Videos for each above videos")

    for count, i in enumerate(results):
        related_results = []
        video_id = i['id']["videoId"]
        print(f'Fetching Related videos of {count+1}: {video_id}')
        yt.videoId = video_id
        related_results = yt.get_results(type_="relatedVideo")
        related_results += related_results
        print("\n")
    print(related_results)

    return (results, related_results)


if (__name__ == "__main__"):
    runTest()
