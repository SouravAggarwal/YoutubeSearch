from requests import get
from json import loads
from math import ceil, floor


class YTsearch:
    '''
    It fetches Youtube video results page by page by given config.
    if type_= "bychannel", then it fetches given n no. of videos by channelID
    if type_= "relatedVideo", then it fetches Related videos by given VideoID
    '''

    def __init__(self, api_key='', channelId='', max_results=50, max_related_result=50, no_related_videos=2):
        self.API_KEY = api_key
        self.channelID = channelId
        self.max_results = max_results  # videos per page upto 50
        self.max_related_result = max_related_result  # videos per page upto 50
        self.no_related_videos = no_related_videos

        # self.VIDEOS_REQ = VIDEOS_REQ  # fetch first n no. of videos from given channel(@ runtime)
        self.videoId = ""
        self.total_channel_videos = 0

    def get_channel_url(self, page_token=""):
        '''return url with meta info and n videos info for a channel
        ex: https://www.googleapis.com/youtube/v3/search?key=AIzaSyDMY2r2vszk1YmId9ipfOnuvqsYHcNU87A&channelId=UCWN3xxRkmTPmbKwht9FuE5A&part=snippet,id&type=video&order=date&maxResults=20
        '''
        CHANNEL_URL = f'https://www.googleapis.com/youtube/v3/search?key={self.API_KEY}&channelId={self.channelID}&part=snippet,id&type=video&order=date&maxResults={self.max_results}&pageToken={page_token}'
        return CHANNEL_URL

    def get_video_url(self, page_token=""):
        '''returns url having videos related to given video id
        ex: https://www.googleapis.com/youtube/v3/search?part=snippet&relatedToVideoId=93E_GzvpMA0&type=video&key=AIzaSyDMY2r2vszk1YmId9ipfOnuvqsYHcNU87A&order=date&maxResults=2&pageToken=
        '''
        VIDEO_URL = f'https://www.googleapis.com/youtube/v3/search?part=snippet&relatedToVideoId={self.videoId}&type=video&key={self.API_KEY}&pageToken={page_token}&order=date&maxResults={self.max_related_result}'
        return VIDEO_URL

    def get_results(self, type_='bychannel'):
        ''' return list of videos by given config'''
        self.results = []
        self.info = ""

        if type_ == 'bychannel':
            self.info = loads(get(self.get_channel_url()).text)
        elif type_ == 'relatedVideo':
            self.info = loads(get(self.get_video_url()).text)

        page_info = self.info.get('pageInfo')
        total_results = page_info.get('totalResults')

        if type_ == 'bychannel':
            self.total_channel_videos = total_results

            print(f"Total { total_results } videos found!")
            print(f"To get all videos Prss Enter else Enter no. of Vidoes less than {total_results} ")
            entered = input()
        elif type_ == 'relatedVideo':
            print(f"Total {total_results} related videos found")
            print(f"Fetching first {self.no_related_videos} related videos ")
            entered = str(self.no_related_videos)

        if entered.isdigit() and int(entered) < total_results:
            VIDEOS_REQ = int(entered)
        else:
            VIDEOS_REQ = int(total_results)

        req_vidoes = min(total_results, VIDEOS_REQ)
        full_pages = floor(req_vidoes / self.max_results)
        last_page_videos = req_vidoes % self.max_results
        if type_ == 'bychannel':
            print(f"Getting first {VIDEOS_REQ} videos")
            print(
                f"Fist {full_pages} page(s) has {full_pages}*{self.max_results} videos & last page has {last_page_videos} videos")
            # To show Progress
        progress = ceil(req_vidoes / self.max_results)

        # Getting videos from 1 to n pages
        if full_pages > 0:
            for i in range(1, full_pages + 1):

                items = self.info.get('items')
                if items is not None:
                    self.results += items

                # Update Progress
                print(f"\r Progress = {(i/progress)*100} %", end='\r')

                page_token = self.info.get("nextPageToken")
                if type_ == 'bychannel':
                    self.info = loads(get(self.get_channel_url(page_token)).text)
                elif type_ == 'relatedVideo':
                    self.info = loads(get(self.get_video_url(page_token)).text)

        if last_page_videos > 0:

            items = self.info.get('items')
            if items is not None:
                self.results += items[:last_page_videos]
            print(f"\r Progress = {(1)*100} %", end='\r')
        return (self.results)

    # ***************** OR **************************#

    def get_results_generator(self, type_='bychannel'):
        ''' return a generator of results for each video page'''
        self.results = []
        self.info = ""

        if type_ == 'bychannel':
            self.info = loads(get(self.get_channel_url()).text)
        elif type_ == 'relatedVideo':
            self.info = loads(get(self.get_video_url()).text)

        page_info = self.info.get('pageInfo')
        total_results = page_info.get('totalResults')

        if type_ == 'bychannel':
            self.total_channel_videos = total_results

            print(f"Total { total_results } videos found!")
            print(f"To get all videos Prss Enter else Enter no. of Vidoes less than {total_results} ")
            entered = input()
        elif type_ == 'relatedVideo':
            print(f"Total {total_results} related videos found")
            print(f"Fetching first {self.no_related_videos} related videos ")
            entered = str(self.no_related_videos)

        if entered.isdigit() and int(entered) < total_results:
            VIDEOS_REQ = int(entered)
        else:
            VIDEOS_REQ = int(total_results)

        req_vidoes = min(total_results, VIDEOS_REQ)
        full_pages = floor(req_vidoes / self.max_results)
        last_page_videos = req_vidoes % self.max_results
        if type_ == 'bychannel':
            print(f"Getting first {VIDEOS_REQ} videos")
            print(
                f"Fist {full_pages} page(s) has {full_pages}*{self.max_results} videos & last page has {last_page_videos} videos")
            # To show Progress
        progress = ceil(req_vidoes / self.max_results)

        # Getting videos from 1 to n pages
        if full_pages > 0:
            for i in range(1, full_pages + 1):

                items = self.info.get('items')
                if items is not None:
                    yield items

                # Update Progress
                print(f"\r Progress = {(i/progress)*100} %", end='\r')

                page_token = self.info.get("nextPageToken")
                if type_ == 'bychannel':
                    self.info = loads(get(self.get_channel_url(page_token)).text)
                elif type_ == 'relatedVideo':
                    self.info = loads(get(self.get_video_url(page_token)).text)

        if last_page_videos > 0:
            print(f"\r Progress = {(1)*100} %", end='\r')
            items = self.info.get('items')
            if items is not None:
                yield items[:last_page_videos]
