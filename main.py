import random
# from typing import Any
import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.video import Video
from kivy.core.audio import SoundLoader
from kivy.uix.button import Button
# from kivy.uix.button import ButtonBehavior
# from kivy.uix.behaviors import DragBehavior
# from kivy.uix.videoplayer import VideoPlayer
from kivy.uix.scrollview import ScrollView
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.image import AsyncImage
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
# from kivy.uix.stacklayout import StackLayout
# from kivy.uix.widget import Widget
from kivy.animation import Animation
from kivy.uix.progressbar import ProgressBar
from kivy.core.window import Window
from kivy.clock import Clock
from functools import partial
# from kivy.graphics import Rectangle, Color
from pytube import YouTube, Channel, Playlist, Search
import pandas as pd
import os
import requests
import pickle
import threading
# import dill
# from class_def import foo



Window.size = 360,640
# thubnail = ["wallpaper\\code ston.jpg","wallpaper\\dadicpsu85pdw66r.jpg","wallpaper\\hunt.jpg","wallpaper\\mirored.jpg","wallpaper\\nth wallpaper.jpeg","wallpaper\\quiet-sunset-wallpaper.jpg","wallpaper\\spiderman.jpg","wallpaper\\wall p.png","wallpaper\\WjY21KO.jpg","wallpaper\\spiderman.jpg"]
# img_placeholder = "wallpaper\\mirored.jpg"
img_placeholder = "mirored.jpg"
count = 0
active = False
listings = [['How Does Fusion Produce Energy?', 'But Why?']]
urls = []
loading_pct = 0

all_videos = []
# for audio player
objectslist = []  #this contain all the audio objects
current_index = 0  #when user clicks an audio form the list it will update the variable with it index number this will allow us to go to the next audio

audio_playlist = []
video_playlist = []
lastplaylist = []
lastvid = None
vid_refresh = False
error_downloading = False

loading_dic = {"length":1, "downloaded":0, "current_title": None}

# making a directory
dir = 'TubeApp_storage'

if not os.path.exists(dir):
    os.mkdir(dir)

data_loc = f'{dir}\\catch_bin.dat'

# class joki(pickle.Unpickler):
#     def find_class(self, module, name):
#         if module == "__main__":
#             module = "kivyproject"
#         return super().find_class(module, name)
    
def load_data():
    global all_videos, objectslist, audio_playlist, video_playlist, lastplaylist, lastvid
    try:
        if __name__ == '__main__':
            with open(data_loc, "rb") as f:
                all_videos, objectslist, audio_playlist, video_playlist, lastplaylist, lastvid = pickle.load(f)
                print('this is the all_video part',all_videos)
                print('video_ playlist part',video_playlist)
                tube.run()
    except:
        all_videos, objectslist, audio_playlist, video_playlist, lastplaylist, lastvid = [],[],[],[],[],None
        tube.run()
        print('got to where empty array is set as and exception')
    return all_videos, objectslist, audio_playlist, video_playlist

def save_data():
    clear_junks()
    data = [all_videos, objectslist, audio_playlist, video_playlist, lastplaylist, lastvid]
    with open(data_loc, "wb") as f:
        pickle.dump(data,f)

def delete(target):
    global objectslist
    global all_videos
    if target in all_videos:
        if not target.address:
            all_videos.remove(target)
            if os.path.exists(target.thumbnail_address):
                os.remove(target.thumbnail_address)

        elif os.path.exists(target.address):
            os.remove(target.address)
            if os.path.exists(target.thumbnail_address):
                os.remove(target.thumbnail_address)
            all_videos.remove(target)

        else:
            all_videos.remove(target)
            if os.path.exists(target.thumbnail_address):
                os.remove(target.thumbnail_address)

    elif target in objectslist:
        if not target.address:
            objectslist.remove(target)
            if os.path.exists(target.thumbnail_address):
                os.remove(target.thumbnail_address)

        elif os.path.exists(target.address):
            os.remove(target.address)
            if os.path.exists(target.thumbnail_address):
                os.remove(target.thumbnail_address)
            objectslist.remove(target)

        else:
            objectslist.remove(target)
            if os.path.exists(target.thumbnail_address):
                os.remove(target.thumbnail_address)
    save_data()

def clear_junks():
    global all_videos, objectslist, audio_playlist, video_playlist

    for i in objectslist,all_videos:
        i = remove_duobles(i)
        for j in i:
            if not j.address:
                i.remove(j)
    for i in audio_playlist,video_playlist:
        i = remove_duobles(i)
        for j in i:
            j.child = remove_duobles(j.child)
            for k in j.child:
                if not k.address:
                    j.child.remove(k)

def remove_duobles(jk):
    q = []
    new_jk = None
    for i in jk:
        if i not in q:
            q.append(i)
    new_jk = q.copy()
    if new_jk:
        return new_jk
    else:
        return jk

    


def load_list(location):
    csv_file = pd.read_csv(location)
    cols = csv_file.columns

    if len(csv_file.columns) == 2:
        if 'title' in cols and 'author' in cols:
            if len(csv_file['title']) and len(csv_file['author']):
                for i in range(0,len(csv_file.index)):
                    listings.append([csv_file.iloc[i,0], csv_file.iloc[i,1]])
                return 'title and author'
    elif len(csv_file.columns) == 1:
        if 'title' in cols:
            if len(csv_file['title']):
                for i in range(0,len(csv_file.index)):
                    listings.append([csv_file.iloc[i,0]])
                return 'title'  
        elif 'url' in cols:
            if len(csv_file['url']):
                for i in range(0,len(csv_file.index)):
                    urls.append([csv_file.iloc[i,0]])
                return 'url'
    else:
        print('wrong file format')
        return 'wrong file format'
        
def fetch_video(title,author=None):
    if author == None:
        find = Search(title)
        for i in find.results:
            if i.title == title:
                len(find.results)
                return i
        return 'error video not found'
    else:
        find = Search(title)
        dd = find.results
        count = 0
        while count != 3:
            for i in dd:
                if i.title == title and i.author == author:
                    len(find.results)
                    return i
                dd = find.get_next_results
                count += 1
        return 'error video not found'

def download_video(vid, quality, title = None, playlist = False):
    if playlist == False:
        new_video = Viideo(vid.title, vid.description, vid.views, vid.author, vid.length)
        all_videos.append(new_video)
        new_video.download(vid,quality)
    elif playlist:
        new_video = Viideo(vid.title, vid.description, vid.views, vid.author, vid.length)
        new_video.download(vid,quality,title)
        return new_video

def download_audio(vid, quality, title = None, playlist = False):
    if playlist == False:
        new_audio = audiio(vid.title, vid.description, vid.views, vid.author, vid.length)
        objectslist.append(new_audio)
        new_audio.download(vid,quality)
    elif playlist:
        new_audio = audiio(vid.title, vid.description, vid.views, vid.author, vid.length)
        new_audio.download(vid,quality,title)
        return new_audio



def on_progress(stream,chunk,bytes_remaining):
    global loading_pct
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    pct_completed = round(bytes_downloaded / total_size * 100)
    print(pct_completed)
    loading_pct = pct_completed
    # threading.Thread(target=hol.on_it, args= (pct_completed,)).start()

def download_all_from_list(resolution, author = False, audio = False):
    if audio == False:
        if author == True:
            for i in listings:
                download_video(fetch_video(i[0], i[1]), resolution)
            return 'done'
        else:
            for i in listings:
                download_video(fetch_video(i[0]), resolution)
            return 'done'
        
    elif audio == True:
        if author == True:
            for i in listings:
                download_audio(fetch_video(i[0], i[1]), resolution)
            return 'done'
        else:
            for i in listings:
                download_audio(fetch_video(i[0]), resolution)
            return 'done'

def download_all_from_url_list(resolution,audio = False):
    for i in urls:
        use_link(i[0], resolution, audio)
    return 'done'

# download_all_from_list(resolution, author = True)

def download_playlist(playlist_url, resolution, title, amount = "ALL", audio = False):
    newP = n_playlist()
    newP.download_playlist(playlist_url, resolution, title, amount, audio)

def add_playlist(title,type,children): #note that the children are video or audio in array
    newP = n_playlist()
    newP.title = title
    newP.type = type
    newP.child = children
    newP.linked = True
    newP.thumbnail_address = newP.child[0].thumbnail_address
    # newP.address = f'{dir}\\{newP.title}' canceled because i do not need it
    if newP.type == 'audio':
        audio_playlist.append(newP)
    elif newP.type == 'video':
        video_playlist.append(newP)
    save_data()

def delete_playlist(target, focus = None): # focus has to be an array
    if target.linked:
        if focus:
            for h in focus:
                if h in target.child:
                    target.child.remove(h)
                    if not target.child:
                        if target in audio_playlist:
                            audio_playlist.remove(target)
                        elif target in video_playlist:
                            video_playlist.remove(target)
        else:
            if target in audio_playlist:
                audio_playlist.remove(target)
            elif target in video_playlist:
                video_playlist.remove(target)

    else:
        if focus:
            for h in focus:
                if h in target.child:
                    if os.path.exists(h.address):
                        os.remove(h.address)
                        if os.path.exists(h.thumbnail_address):
                            os.remove(h.thumbnail_address)
                    target.child.remove(h)

            if not target.child:
                if target in audio_playlist:
                    audio_playlist.remove(target)
                elif target in video_playlist:
                    video_playlist.remove(target)

                if os.path.exists(f"{dir}\\{target.title}\\thumbnails"):
                    os.rmdir(f"{dir}\\{target.title}\\thumbnails")
                if os.path.exists(f"{dir}\\{target.title}"):
                    os.rmdir(f"{dir}\\{target.title}")

        else:
            for i in target.child:
                if os.path.exists(i.address):
                    os.remove(i.address)
                    if os.path.exists(i.thumbnail_address):
                        os.remove(i.thumbnail_address)
                target.child.remove(i)

            if target in audio_playlist:
                audio_playlist.remove(target)
            elif target in video_playlist:
                video_playlist.remove(target)

            if os.path.exists(f"{dir}\\{target.title}\\thumbnails"):
                os.rmdir(f"{dir}\\{target.title}\\thumbnails")
            if os.path.exists(f"{dir}\\{target.title}"):
                os.rmdir(f"{dir}\\{target.title}")
    save_data()

def download_channel(channel_url, resolution, amount = "ALL", audio = False):
    c = Channel(channel_url)
    if amount == "ALL":
        if audio == True:
            for i in c.videos:
                download_audio(i, resolution)
        else:
            for i in c.videos:
                download_video(i, resolution)
    else:
        if audio == True:
            for j,i in enumerate(c.videos):
                if j <= amount:
                    download_audio(i, resolution)
        else:  
            for j,i in enumerate(c.videos):
                if j <= amount:
                    download_video(i, resolution)

def use_link(url, resolution, audio = False):
    video = YouTube(url)
    if audio == True:
        download_audio(video, resolution)
    else:
        download_video(video, resolution)

def search(title,next = False):
    find = Search(title)
    if next == False:
        return find.results
    elif next == True:
        find.get_next_results
        return find.results

def update_view_counts():
    global all_videos
    for i in all_videos:
        kk = fetch_video(i.title, i.author)
        i.views = kk.view
        i.discription = kk.discription

class Viideo():
    def __init__(self, title, description, views, author,duration):
        self.title = title
        self.description = description
        self.author = author
        self.views = views
        self.thumbnail_address = None
        self.address = None
        self.categorie = []
        self.duration = duration
        self.last_pos = None
        self.type = 'video'

    def download(self, vid, quality, playlist = 'video'):
        global error_downloading, loading_dic, loading_pct
        loading_dic['current_title'] = vid.title
        try:
            folder_path = f"{dir}\\{playlist}"
            if not os.path.exists(folder_path):
                os.mkdir(folder_path)
            folder_for_thumb = f"{folder_path}\\thumbnails"
            if not os.path.exists(folder_for_thumb):
                os.mkdir(folder_for_thumb)

            num = 0
            clean_title = vid.title.replace("|","")
            clean_title = clean_title.replace("\\","")
            clean_title = clean_title.replace("\"","")

            responds = requests.get(vid.thumbnail_url)
            k = f"""{folder_for_thumb}\\{clean_title}.jpg"""
            while os.path.exists(k):
                num += 1
                k = f"""{folder_for_thumb}\\{clean_title}({num}).jpg"""

            with open(k, "wb") as f:
                f.write(responds.content)
            self.thumbnail_address = k


            vid.register_on_progress_callback(on_progress)
            if quality == 'high':
                vid.streams.get_highest_resolution().download(folder_path, f'{clean_title}.mp4')
            elif quality == 'medium':
                vid.streams.get_by_resolution("360p").download(folder_path, f'{clean_title}.mp4')
            elif quality == 'low':
                vid.streams.get_lowest_resolution().download(folder_path, f'{clean_title}.mp4')
            else:
                vid.streams.get_highest_resolution().download(folder_path, f'{clean_title}.mp4')
            self.address = f"{folder_path}\\{clean_title}.mp4"
            loading_dic['downloaded'] += 1
            loading_pct = 0
            save_data()
        
        except:
            print("something is wrong with video.download()")
            loading_pct = 0
            error_downloading = True
            return 'error'

class audiio():
    def __init__(self, title, description, views, author, duration):
        self.title = title
        self.description = description
        self.author = author
        self.views = views
        self.thumbnail_address = None
        self.address = None
        self.categorie = []
        self.duration = duration
        self.last_pos = None
        self.type = 'audio'

    def download(self,vid, quality, playlist = 'audio'):
        global error_downloading, loading_dic, loading_pct
        loading_dic['current_title'] = vid.title
        try:
            folder_path = f"{dir}\\{playlist}"
            if not os.path.exists(folder_path):
                os.mkdir(folder_path)
            folder_for_thumb = f"{folder_path}\\thumbnails"
            if not os.path.exists(folder_for_thumb):
                os.mkdir(folder_for_thumb)

            num = 0
            clean_title = vid.title.replace("|","")
            clean_title = clean_title.replace("\\","")
            clean_title = clean_title.replace("\"","")

            responds = requests.get(vid.thumbnail_url)
            k = f"{folder_for_thumb}\\{clean_title}.jpg"
            while os.path.exists(k):
                num += 1
                k = f"{folder_for_thumb}\\{clean_title}({num}).jpg"

            with open(k, 'wb') as f:
                f.write(responds.content)
            self.thumbnail_address = k

            vid.register_on_progress_callback(on_progress)
            if quality == 'high':
                iki = vid.streams.filter(only_audio = True).first()
                iki.download(folder_path, f'{clean_title}.mp3')
            elif quality == 'medium':
                kj = vid.streams.filter(only_audio = True).all()
                kj[1].download(folder_path, f'{clean_title}.mp3')
            elif quality == 'low':
                ji = vid.streams.filter(only_audio = True).all()
                ji[2].download(folder_path, f'{clean_title}.mp3')
            else:
                iki = vid.streams.filter(only_audio = True).first()
                iki.download(folder_path, f'{clean_title}.mp3')
            self.address = f"{folder_path}\\{clean_title}.mp3"
            loading_dic['downloaded'] += 1
            loading_pct = 0
            save_data()
        
        except:
            print('something is wrong with Audiio.download()')
            loading_pct = 0
            error_downloading = True
            return 'error'

class n_playlist():
    def __init__(self):
        self.title = None
        self.type = None
        self.address = None
        self.child = []
        self.linked = False
        self.thubmnail_address = None

    def download_playlist(self,playlist_url, resolution, title, amount = "ALL", audio = False):
        global loading_dic
        try:
            p = Playlist(playlist_url)
        except:
            print('error in playlist.download_playlist()')
        if amount == "ALL":
            loading_dic['length'] = len(p.videos)
        else:
            loading_dic['length'] = amount
        if title:
            self.title = title
        else:
            self.title = p.title

        if amount == "ALL":
            if audio == True:
                for i in p.videos:
                    self.child.append(download_audio(i, resolution, self.title, True))
                    self.type = 'audio'
                    self.thumbnail_address = self.child[0].thumbnail_address
                audio_playlist.append(self)
                save_data()
                return p.title
            else:
                for i in p.videos:
                    self.child.append(download_video(i, resolution, self.title, True))
                    self.type = 'video'
                    self.thumbnail_address = self.child[0].thumbnail_address
                video_playlist.append(self)
                save_data()
                return p.title
        else:
            if audio == True:
                for j,i in enumerate(p.videos):
                    if j < amount:
                        self.child.append(download_audio(i, resolution, self.title, True))
                        self.type = 'audio'
                        self.thumbnail_address = self.child[0].thumbnail_address
                    else:
                        break
                audio_playlist.append(self)
                save_data()
                return p.title
            else:
                j = 0
                for j,i in enumerate(p.videos):
                    if j < amount:
                        self.child.append(download_video(i, resolution, self.title, True))
                        self.type = 'video'
                        self.thumbnail_address = self.child[0].thumbnail_address
                    else:
                        break
                video_playlist.append(self)
                save_data()
                return p.title




# this is just a play class to test things
holki = Viideo('What happens when youTube brakes',
                "The way the world as we know it is evolving is terifiying and i cant want to make things better for all of us that is why i made this bad video about the lagendary youtube that has been poisoning the young people of today in a way that we might not expect. Thanks for watching my noncenses",
                2903,
               'Teliej',
               3899)
holki.address = "learning-python-c\\projects\\TubeApp\\Tour.mp4"

holki_audi = audiio('What happens when youTube brakes',
                "The way the world as we know it is evolving is terifiying and i cant want to make things better for all of us that is why i made this bad video about the lagendary youtube that has been poisoning the young people of today in a way that we might not expect. Thanks for watching my noncenses",
                2903,
               'Teliej',
               3899)
holki_audi.address = "learning-python-c\\projects\\TubeApp\\ui.mp3"
holki_audi.thumbnail_address = "learning-python-c\\projects\\TubeApp\\yababuluku.jpg"





def string_cut(string, max_length):
    k = None
    if len(string) > max_length:
        k = string[:max_length]
        while k[max_length-1] == ' ':
            k = string[:max_length-1]
            max_length -= 1
        k = f'{k}...'
        return k
    return string





class WindowManager(ScreenManager):
    def __init__(self, **kwargs):
        super(WindowManager, self).__init__(**kwargs)
    
    def refreshv(self):
        self.clear_widgets(screens = [self.get_screen('Watch Videos')])
        hi = WatchVideos()
        self.add_widget(hi)

    def refresha(self):
        self.clear_widgets(screens = [self.get_screen('PlayAudiio')])
        hi = PlayAudiio()
        self.add_widget(hi)

class FirstWindow(Screen):
    pass



class downloading(Popup):
    def __init__(self, **kwargs):
        super(downloading, self).__init__(**kwargs)
        self.size_hint = (.78,.28)
        self.pos_hint = {'center_x': .5, 'center_y': .5}
        self.title = 'Downloading'
        self.auto_dismiss = False
        self.updater = None
        self.done_self = None

    def rem(self):
        self.dismiss()

    def looper(self, j = None):
        if j:
            self.done_self = j
        self.open()
        self.updater = Clock.schedule_interval(self.on_it, 0)

    def on_it(self, n):
        global loading_pct
        global error_downloading
        if loading_dic['downloaded'] == loading_dic['length']:
            self.dismiss()
            self.updater.cancel()
            loading_dic['current_title'] = None
            loading_dic['length'] = 1
            loading_dic['downloaded'] = 0
            # if self.done_self:
            #     try:
            #         self.done_self.manager.refresha()
            #         self.done_self.manager.refreshv()
            #     except:
            #         pass
        else:
            if loading_dic['length'] > 1:
                pct = ((( loading_dic['downloaded'] * 100 ) + loading_pct ) / ( loading_dic['length'] * 100) ) * 100
                self.ids.nofn.text = f'Status: {loading_dic["downloaded"]} of {loading_dic["length"]} downloaded...'
                if loading_dic['downloaded'] == (loading_dic['downloaded'] + 1):
                    if self.done_self:
                        try:
                            self.done_self.manager.refresha()
                            self.done_self.manager.refreshv()
                        except:
                            pass
            else:
                pct = loading_pct
                if error_downloading:
                    self.dismiss()
                    self.updater.cancel()
            if loading_dic['current_title']:
                self.ids.title.text = string_cut(loading_dic['current_title'],40)
            self.ids.loading.value = pct
            self.ids.pct.text = f'{pct}%/100%'


        # self.ids.loading.value = loading_pct
        # self.ids.pct.text = f'{loading_pct}%/100%'
        # if loading_pct == 100:
        #     self.dismiss()
        #     self.updater.cancel()
        # if error_downloading == True:
        #     error_downloading = False
        #     self.dismiss()
        #     self.updater.cancel()

class download(Popup):
    def __init__(self, **kwargs):
        super(download, self).__init__(**kwargs)
        self.size_hint = (.98,.5)
        self.pos_hint = {'center_x': .5, 'center_y': .5}
        self.title = 'Download'
        self.auto_dismiss = False
        self.target = None
        self.resolution = 'high'
        self.audionly = False
        self.loading = downloading()
        self.search_self = None
        self.ki = None

    def rem(self):
        self.dismiss()

    def pop(self,j, sel, u):
        self.open()
        self.target = j
        self.search_self = sel

    def downl(self):
        if self.target:
            self.dismiss()
            if self.audionly == True:
                self.dismiss()
                self.loading.looper(self.search_self)
                # self.ki = Clock.schedule_interval(self.loading.on_it, 0)  
                threading.Thread(target= download_audio, args= (self.target,self.resolution)).start()
            else:
                self.dismiss()
                self.loading.looper(self.search_self)
                # self.ki = Clock.schedule_interval(self.loading.on_it, 0)
                threading.Thread(target= download_video, args= (self.target,self.resolution)).start()
        else:
            self.dismiss()

    def details(self):
        jj = details()
        jj.on_it_search(self.target)

    def quality(self, vi,value):
        self.resolution = value

    def audi(self,i):
        self.audionly = i.active

class settings(Popup):
    def __init__(self, **kwargs):
        super(settings, self).__init__(**kwargs)
        self.size_hint = (.6,.4)
        self.pos_hint = {'center_x': .5, 'center_y': .5}
        self.title = 'Settings'
        self.dd = details()
    
    def seli(self):
        self.dismiss()
        self.jkl = selections()
        self.parent.add_widget(self.jkl)

    def details(self, dt, t=None):
        self.dd.on_it(dt)

class details(Popup):
    def __init__(self, **kwargs):
        super(details, self).__init__(**kwargs)
        self.size_hint = (.85,.5)
        self.pos_hint = {'center_x': .5, 'center_y': .5}
        self.title = 'details'
        # self.showall.bind(minimum_height = self.showall.setter('height'))
        self.ids.hold.bind(minimum_height = self.ids.hold.setter('height'))
        # self.ids.description.bind(minimum_height = self.ids.description.setter('height'))
    
    def on_it(self, target):
        if target.title:
            self.ids.title.text = f'Title: {target.title}'
        if target.author:
            self.ids.author.text = f'Author: {target.author}'
        if target.views:
            self.ids.views.text = "Views: {:,}".format(target.views)
        if target.duration:
            self.ids.duration.text = f'Duration: {self.timer(target.duration)}'
        if target.description:
            self.ids.description.text = target.description
        self.open()

    def on_it_search(self, target):
        if target.title:
            self.ids.title.text = f'Title: {target.title}'

        if target.author:
            self.ids.author.text = f'Author: {target.author}'

        if target.views:
            self.ids.views.text = "Views: {:,}".format(target.views)

        if target.length:
            self.ids.duration.text = f'Duration: {self.timer(target.length)}'

        if target.description:
            self.ids.description.text = target.description
        self.open()

    def timer(self, duration):
        hour = int((duration // 60) // 60)
        minute = int((duration // 60) % 60)
        seconds = int(duration % 60)
        if minute < 10:
            minute = f'0{minute}'
        if seconds < 10:
            seconds = f'0{seconds}'
        if hour:
            return f'{hour}:{minute}:{seconds}'
        else:
            return f'{minute}:{seconds}'

class newplaylist(Popup):
    def __init__(self, **kwargs):
        super(newplaylist, self).__init__(**kwargs)
        self.size_hint = (.98,.2)
        self.pos_hint = {'center_x': .5, 'center_y': .5}
        self.title = 'new playlist'

    def rem(self):
        self.dismiss()

class selections(FloatLayout):
    def __init__(self, **kwargs):
        super(selections, self).__init__(**kwargs)



class videoid(Button, BoxLayout):
    def __init__(self, **kwargs):
        super(videoid, self).__init__(**kwargs)
        self.background_normal = ''
        self.background_color = (0,0,0,1)


    def jki(self):
        print('yes it worked')

class audioid(Button, BoxLayout):
    def __init__(self, **kwargs):
        super(audioid, self).__init__(**kwargs)

    def jki(self):
        print('yes it worked')

class btndrag(Button):
    def __init__(self, **kwargs):
        super(btndrag, self).__init__(**kwargs)
        self.pos_percent = None
    
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            touch.grab(self)
            return True
        return super().on_touch_down(touch)
    
    def on_touch_move(self, touch):
        if touch.grab_current == self:
            # self.pos_hint = {"x": touch.dx, "center_y":.1}
            self.pos_percent = touch.pos[0]/Window.width
            self.pos_hint = {"center_x": self.pos_percent, "center_y":.1}

    def on_touch_up(self, touch):
        if touch.grab_current == self:
            touch.ungrab(self)
            self.pos_percent = None
            return True
        return super().on_touch_up(touch)

class WatchVideos(Screen): 
    
    def __init__(self, **kwargs):
        super(WatchVideos, self).__init__(**kwargs)
        self.selections = []
        self.select = False
        self.target = None
        self.ctarget = lastvid
        self.B_state = 'playlist'
        self.selection_frame = []
        # load_data()
        self.list1 = all_videos.copy()
        self.list2 = lastplaylist.copy()
        self.list1.reverse()
        self.list2.reverse()
        self.is_playlist = False
        self.target_playlist = None
        # self.sim = WindowManager()

        self.vid_placeholder = None
        self.contents = BoxLayout(orientation = 'vertical',spacing = 20)

        self.vidcontain = AnchorLayout(size_hint = (1,.6))

        self.vidclick = videoid(orientation = 'vertical',spacing = 10)
        # self.vidclick.bind(on_press = self.change_animate)
        self.immg = Image(source = img_placeholder)
        self.immg.size_hint = (.8,.8)
        self.immg.pos_hint = {"center_x":0.5, "center_y":0.5}
        self.vidclick.add_widget(self.immg)

        self.txtings = Label(text = 'Welcome. At your service here.')
        self.txtings.size_hint = (1,.05)
        self.txtings.valign = 'center'
        self.txtings.halign = 'left'
        # self.txt.text_size = self.txt.size
        self.vidclick.add_widget(self.txtings)


        self.vidcontain.add_widget(self.vidclick)
        self.contents.add_widget(self.vidcontain)

        self.bottompart = ScrollView()
        self.bottompart.size = self.bottompart.size

        # if vid_refresh:
        if lastvid:
            self.vidclick.bind(on_press = self.previous)
            self.immg.source = lastvid.thumbnail_address
            
        self.listings(self.list1)

        self.nav = GridLayout()
        self.nav.cols = 2
        self.nav.size_hint = (1,.1)
        self.nav.spacing = 3
        
        self.buttton1 = Button()
        self.buttton1.text = '<- Go Back'
        self.buttton1.bind(on_press = self.gobackback)
        self.buttton1.background_color = (.1,.1,.1,1)
        self.buttton1.background_normal = ''
        # self.manager.current.transition.direction = 'left'
        self.nav.add_widget(self.buttton1)


        self.buttton2 = Button()
        self.buttton2.text = 'Playlists Here'
        self.buttton2.on_press = self.playlist_details
        self.buttton2.background_color = (.1,.1,.1,1)
        self.buttton2.background_normal = ''
        self.nav.add_widget(self.buttton2)

        self.contents.add_widget(self.nav)
        self.contents.add_widget(self.bottompart)
        self.add_widget(self.contents)


        self.uno = settings()
        self.jj = selections()

        jk = self.uno.ids.jkk
        jk.bind(on_press = self.seli_mode)
        jso = self.uno.ids.back
        jso.bind(on_press = self.rem)

        dman = self.jj.ids.done
        dman.bind(on_press = self.opp)

        self.uno.ids.play.bind(on_press = self.play_op)
        self.uno.ids.details.bind(on_press = self.detail)
        self.uno.ids.delete.bind(on_press = self.delete)
        self.uno.ids.newplay.bind(on_press = self.newp)

    def listings(self, list):
        if not list:
            self.vid_placeholder = BoxLayout()
            self.vid_placeholder.size_hint = (1,1)
            txt = Label()
            txt.text = 'Nothing here!'
            self.vid_placeholder.add_widget(txt)
            try:
                self.bottompart.add_widget(self.vid_placeholder)
            except:
                pass
            return 0
        if self.vid_placeholder:
            self.bottompart.remove_widget(self.vid_placeholder)
            self.vid_placeholder = None

        
        self.txtings.text = 'Welcome back continue from where you left'

        columns = 3
        heights = 100
        self.stack_0 = GridLayout()
        

        self.stack_0.cols = columns
        self.stack_0.size_hint_y = None
        self.stack_0.bind(minimum_height = self.stack_0.setter('height'))
        self.stack_0.spacing = (15,15)
        self.stack_0.padding = (10,0)

        for i in list:
            self.item = videoid()
            self.item.bind(on_press = partial(self.pop, i))
            self.item.orientation = 'vertical'
            self.item.size_hint = (1,None)
            self.item.height = heights

            # self.img = Image(source = holki_audi.thumbnail_address)

            self.img = Image()
            self.img.source = i.thumbnail_address
            self.img.size_hint = (1,1)

            self.item.add_widget(self.img)
            self.lab = Label(text = f'{string_cut(i.title,20)}')
            self.lab.size_hint = (1,.4)
            self.lab.valign = 'center'
            self.lab.halign = 'left'

            self.item.spacing = 5
            self.lab.text_size = self.lab.size
            self.item.add_widget(self.lab)
            self.stack_0.add_widget(self.item)
        try:
            self.bottompart.add_widget(self.stack_0)
        except:
            pass
 
    def listing_rec(self, list):
        global lastplaylist
        lastplaylist = list.copy()
        columns = 1
        heights = 275
        self.stack_1 = GridLayout()
        

        self.stack_1.cols = columns
        self.stack_1.size_hint_y = None
        self.stack_1.bind(minimum_height = self.stack_1.setter('height'))
        self.stack_1.spacing = 20

        for i in list:
            if i == self.ctarget:
                continue
            self.item = videoid()
            self.item.bind(on_press = partial(self.pop, i))
            self.item.orientation = 'vertical'
            self.item.size_hint = (1,None)
            self.item.height = heights
            self.item.background_color = (.1,.1,.1,.5)

            self.img = Image(source = i.thumbnail_address)
            # self.img = Image(source = holki_audi.thumbnail_address)
            self.img.size_hint = (1,1)

            self.item.add_widget(self.img)
            self.titles = Label(text = f'{string_cut(i.title, 87)}')
            self.titles.size_hint = (1,.2)
            self.titles.valign = 'center'
            self.titles.halign = 'left'
            self.titles.text_size = self.size
            self.titles.font_size = 15
            self.titles.pos_hint = {"x":.02}
            
            self.author = Label(text = f'Author: {i.author}')
            self.author.size_hint = (1,.1)
            self.author.valign = 'center'
            self.author.halign = 'left'
            self.author.font_size = 12
            self.author.pos_hint = {"x":.02}
            self.author.text_size = self.size

            self.duration = Label(text = f'Duration: {self.timer(i.duration)}')
            self.duration.size_hint = (1,.1)
            self.duration.valign = 'center'
            self.duration.halign = 'left'
            self.duration.font_size = 12
            self.duration.pos_hint = {"x":.02}
            self.duration.text_size = self.size

            self.item.add_widget(self.titles)
            self.item.add_widget(self.author)
            self.item.add_widget(self.duration)
            self.stack_1.add_widget(self.item)

        self.uno.ids.play.unbind(on_press = self.play_op)
        self.uno.ids.play.bind(on_press = self.switch_vid)

        self.buttton2.text = 'Details Here |^|'
        self.B_state = 'details'

    def previous(self,i):
        # self.ctarget = self.target
        self.ctarget = lastvid
        self.target = lastvid
        self.list1 = self.list2
        self.change_animate("run")
        self.vidclick.unbind(on_press = self.previous)

    def newp(self,p):
        self.uno.dismiss()
        kk = newplaylist()
        kk.ids.create.bind(on_press = partial(self.create,kk))
        kk.open()

    def create(self,cre,l):
        if self.selections:
            add_playlist(cre.ids.playlist.text, self.selections[0].type ,self.selections)
            self.rem("k")
            cre.dismiss()
        else:
            cre.dismiss()

    def delete(self,k):
        if self.select:
            if self.is_playlist:
                if self.target_playlist:
                    self.uno.dismiss()
                    try:
                        delete_playlist(self.target_playlist, self.selections)
                        self.refresh_child()
                    except:
                        pass
                    self.rem(k)
                else:
                    self.uno.dismiss()
                    for i in self.selections:
                        try:
                            delete_playlist(i)
                            self.refresh_p()
                        except:
                            pass
                    self.rem(k)
            else:
                self.uno.dismiss()
                for i in self.selections:
                    try:
                        delete(i)
                        self.manager.refreshv()
                    except:
                        pass
                self.rem(k)
        else:
            if self.is_playlist:
                if self.target_playlist:
                    self.uno.dismiss()
                    try:
                        delete_playlist(self.target_playlist,[self.target])
                        self.refresh_child()
                    except:
                        pass
                else:
                    self.uno.dismiss()
                    try:
                        delete_playlist(self.target)
                        self.refresh_p()
                    except:
                        pass
            else:
                self.uno.dismiss()
                try:
                    delete(self.target)
                    self.manager.refreshv()
                except:
                    pass

    def refresh_child(self):
        self.bottompart.remove_widget(self.stack_1)
        self.listing_rec(self.target_playlist.child)
        self.bottompart.add_widget(self.stack_1)     

    def refresh_p(self):
        self.B_state = 'playlist'
        self.playlist_details()
    
    def pop(self,i,j):
        # kk = download()
        if self.select == True:
            if i in self.selections:
                j.background_color = (0,0,0,1)
                self.selections.remove(i)
                self.selection_frame.remove(j)
            else:
                j.background_color = (.1,.1,.2,.6)
                self.selections.append(i)
                self.selection_frame.append(j)
            self.jj.ids.count.text = f'{len(self.selections)} selected'
        else:
            self.target = i
            self.uno.open()
   
    def detail(self,k):
        if self.target_playlist:
            self.uno.details(self.target)
        elif not self.is_playlist:
            self.uno.details(self.target)

    def seli_mode(self,k):
        self.uno.dismiss()
        self.select = True
        try:
            self.add_widget(self.jj)
        except:
            pass

    def play_op(self,t):
        if self.is_playlist:
            if self.select:
                self.rem("k")

            if not self.target_playlist:
                if self.target.type == 'audio':
                    self.uno.dismiss()
                    jk = self.manager
                    olo = jk.get_screen('PlayAudiio')
                    olo.open_with(self.target, self.target.child)
                    jk.current = 'PlayAudiio'
                elif self.target.type == 'video':
                    self.uno.dismiss()
                    self.target_playlist = self.target
                    self.list1 = self.target_playlist.child
                    self.target = self.target_playlist.child[0]
                    self.ctarget = self.target
                    self.change_animate()

        elif self.target:
            if self.select:
                self.list1 = self.selections
                self.rem("k")
            self.uno.dismiss()
            self.ctarget = self.target
            self.change_animate()

    def switch_vid(self,i):
        global lastvid
        self.bottompart.remove_widget(self.stack_1)
        self.vidclick.remove_widget(self.floating)
        self.uno.dismiss()
        self.video.state = 'stop'
        self.updater.cancel()
        self.video.source = self.target.address
        self.video.bind(position = self.last_position)
        self.ctarget = self.target
        lastvid = self.ctarget
        self.play_pause("k")
        self.listing_rec(self.list1)
        self.bottompart.add_widget(self.stack_1)
        self.vidclick.add_widget(self.floating)

        lastvid = self.target
        self.immg.source = lastvid.thumbnail_address

    def rem(self, k):
        if self.select == True:
            self.select = False
            self.remove_widget(self.jj)
            for i in self.selection_frame:
                i.background_color = (0,0,0,1)
            self.selections = []
            self.uno.dismiss()
            self.jj.ids.count.text = '0 selected'
        else:
            self.uno.dismiss()

    def opp(self,i):
        self.uno.open()

    def change_animate(self, bindarg = None):
        global lastvid
        # if bindarg != 'run':
        lastvid = self.target
        self.immg.source = lastvid.thumbnail_address


        self.buttton1.unbind(on_press = self.gobackback)
        self.buttton1.bind(on_press = self.goback)

        self.vidclick.remove_widget(self.immg)
        self.vidclick.remove_widget(self.txtings)

        self.floating = FloatLayout()
        self.floating.size_hint = (1,1)
        self.video = Video(options = {'fit_mode': 'contain'})
        self.video.size_hint = (.8,.8)
        self.video.pos_hint = {"center_x":0.5, "center_y":0.5}
        self.video.source = self.target.address
        self.video.bind(position = self.last_position)
        self.video.state = 'play'

        self.floating.add_widget(self.video)
        self.vidclick.add_widget(self.floating)

        animation = Animation(size_hint = (1,1),
                            duration= .3)
        animation.start(self.video)
        self.vidclick.unbind(on_press = self.previous)

        # self.vidclick.bind(on_press = self.vidcontrol) #was commented
        self.vidcontrol("p")

        animation = Animation(opacity = 0, duration = 0)
        animation += Animation(opacity = 1,duration= 2)
        animation.start(self.bottompart)

        self.bottompart.remove_widget(self.stack_0)
        self.listing_rec(self.list1)
        self.bottompart.add_widget(self.stack_1)

    def last_position(self,k,l):
        if self.target.last_pos:
            self.video.seek(percent= self.target.last_pos / self.target.duration, precise= True)
            self.video.unbind(position = self.last_position)
        else:
            self.video.unbind(position = self.last_position)

    def vidcontrol(self, kl):
        global active

        self.sec_jumper = BoxLayout()
        # self.sec_jumper.size_hint = (1,.9) 
        self.sec_jumper.size_hint = (1,1) 
        self.sec_jumper.spacing = 0
        self.sec_jumper.pos_hint = {"x": 0, "top":1}

        self.left_side = Button()
        self.left_side.size_hint = (1,1)
        self.left_side.background_color = (0,0,0,1)
        self.left_side.background_normal = ''
        self.left_side.opacity = .7
        self.left_side.bind(on_press = partial(self.movebysec, 'toleft'))

        self.right_side = Button()
        self.right_side.size_hint = (1,1)
        self.right_side.background_color = (0,0,0,1)
        self.right_side.background_normal = ''
        self.right_side.opacity = .7
        self.right_side.bind(on_press = partial(self.movebysec, 'toright'))

        self.sec_jumper.add_widget(self.left_side)
        self.sec_jumper.add_widget(self.right_side)



        self.top_container = BoxLayout()
        self.top_container.size_hint = (1,1)
        self.top_container.pos_hint = {"x":0, "center_y":.95}

        self.txt = Label(text = string_cut(self.target.title, 37))
        self.txt.size_hint = (1,1)
        self.txt.valign = 'center'
        self.txt.halign = 'left'
        self.txt.font_size = 13
        # self.txt.text_size = self.txt.size

        self.txt2 = Label(text = ' ')
        self.txt2.size_hint = (.4,1)

        self.top_container.add_widget(self.txt)
        self.top_container.add_widget(self.txt2)



        self.lower_container = FloatLayout()
        self.lower_container.size_hint = (1,.1)
        self.lower_container.pos_hint = {"x":0, "y":0}

        self.time_txt = Label()
        self.time_txt.text = "00:00/00:00"
        self.time_txt.font_size = 10
        self.time_txt.halign = 'left'
        self.time_txt.size_hint = (.25,.5)
        self.time_txt.pos_hint = {"x":0, "y":.6}

        self.progress = ProgressBar()
        self.progress.size_hint = (1,.1)
        self.progress.max = 1
        self.progress.value = 0
        self.progress.pos_hint = {"x":0, "y":0}


        self.round_btn = btndrag()
        self.round_btn.size_hint = (None,None)
        self.round_btn.height = 15
        self.round_btn.width = 15
        self.round_btn.pos_hint = {"x":0, "center_y":.1}

        self.lower_container.add_widget(self.time_txt)
        self.lower_container.add_widget(self.progress)
        self.lower_container.add_widget(self.round_btn)



        self.nav_container = BoxLayout()
        self.nav_container.size_hint = (1,.2) 
        self.nav_container.pos_hint = {"center_x":0.5, "center_y":0.5}

        self.btn_nav1 = Button()
        self.btn_nav1.text = '<<'
        self.btn_nav1.background_color = (0,0,0,0)
        self.btn_nav1.background_normal = ''
        self.btn_nav1.bind(on_press = self.backward)
        self.btn_nav1.size_hint = (.5,1)

        self.btn_nav2 = Button()
        self.btn_nav2.text = '|>'
        self.btn_nav2.background_color = (0,0,0,0)
        self.btn_nav2.background_normal = ''
        self.btn_nav2.bind(on_press = self.play_pause)
        self.btn_nav2.size_hint = (.5,1)

        self.btn_nav3 = Button()
        self.btn_nav3.text = '>>'
        self.btn_nav3.background_color = (0,0,0,0)
        self.btn_nav3.background_normal = ''
        self.btn_nav3.bind(on_press = self.forward)
        self.btn_nav3.size_hint = (.5,1)

        self.nav_container.add_widget(self.btn_nav1)
        self.nav_container.add_widget(self.btn_nav2)
        self.nav_container.add_widget(self.btn_nav3)



        self.floating.add_widget(self.sec_jumper)
        self.floating.add_widget(self.top_container)
        self.floating.add_widget(self.lower_container)
        self.floating.add_widget(self.nav_container)
        active = True

        
        self.updater = Clock.schedule_interval(self.udatebar,.1)

        Clock.schedule_once(partial(self.removeall,'removeControl'),5)
        self.vidclick.unbind(on_press = self.vidcontrol)

    def forward(self,k):
        if (self.list1.index(self.ctarget) + 1) >= len(self.list1):
            return 0
        else:
            self.target = self.list1[self.list1.index(self.ctarget) + 1]
            self.switch_vid(k)

    def backward(self,k):
        if (self.list1.index(self.ctarget) - 1) < 0:
            return 0
        else:
            self.target = self.list1[self.list1.index(self.ctarget) - 1]
            self.switch_vid(k)

    def removeall(self, command, ll=None):
        global active
        if command == 'removeControl' and active == True:
            self.left_side.opacity = 0
            self.right_side.opacity = 0
            self.floating.remove_widget(self.top_container)
            self.floating.remove_widget(self.nav_container)
            self.lower_container.remove_widget(self.time_txt)
            self.lower_container.remove_widget(self.round_btn)
            active = False
        elif active == False:
            if ll:
                pass
            else:
                self.left_side.opacity = .5
                self.right_side.opacity = .5
                self.floating.add_widget(self.top_container)
                self.floating.add_widget(self.nav_container)
                self.lower_container.add_widget(self.time_txt)
                self.lower_container.add_widget(self.round_btn)
                active = True
                Clock.schedule_once(partial(self.removeall,'removeControl'),5)
        elif active == None:
            active = True
            Clock.schedule_once(partial(self.removeall,'removeControl'),5)

    def play_pause(self,ss):
            if self.video.state == 'play':
                self.video.state = 'pause'
                self.btn_nav2.text = '||'
                self.updater.cancel()
            else:
                self.video.state = 'play'
                self.btn_nav2.text = '|>'
                self.updater = Clock.schedule_interval(self.udatebar,.1)
                
    def udatebar(self, kk):
            global active
            if self.round_btn.pos_percent == None:
                self.video.state = 'play'
                self.ctarget.last_pos = self.video.position
                self.progress.value = (self.video.position + 3)/self.video.duration
                self.round_btn.pos_hint = {"center_x":self.progress.value, "center_y":.1}
                self.time_txt.text = f'{self.timer(self.video.position)}/{self.timer(self.video.duration)}'


                if self.progress.value >= .95:
                    self.round_btn.pos_hint = {"right":1, "center_y":.1}

                if self.video.duration == self.video.position:
                    self.video.state = 'pause'
                    self.updater.cancel()
            else:
                self.video.state = 'pause'
                self.progress.value = self.round_btn.pos_percent
                self.video.seek(percent= self.round_btn.pos_percent, precise= True)
                self.time_txt.text = f'{self.timer(self.video.position)},{self.timer(self.video.duration)}'
                active = None
 
    def timer(self, duration):
        hour = int((duration // 60) // 60)
        minute = int((duration // 60) % 60)
        seconds = int(duration % 60)
        if minute < 10:
            minute = f'0{minute}'
        if seconds < 10:
            seconds = f'0{seconds}'
        if hour:
            return f'{hour}:{minute}:{seconds}'
        else:
            return f'{minute}:{seconds}'

    def movebysec(self, to, sel):
        global count
        global active
        count += 1
        if count == 2:
            if to == 'toleft':
                animi = Animation(opacity = .5,duration = .1) 
                # self.left_side.text = '<<'
                animi += Animation(opacity = .7,duration = .2) 
                # self.left_side.text = '-10 <<'

                pos_percent = (self.video.position - 10)/self.video.duration
                self.video.seek(percent = pos_percent, precise = True)

                animi += Animation(opacity = 0,duration = .1) 
                # self.left_side.text = ''
                animi.start(self.left_side)
                return

            else:
                animi = Animation(opacity = .5,duration = .1) 
                # self.right_side.text = '>>'
                animi += Animation(opacity = .7,duration = .2) 
                # self.right_side.text = '>> +10'

                pos_percent = (self.video.position + 10)/self.video.duration
                self.video.seek(percent = pos_percent, precise = True)

                animi += Animation(opacity = 0,duration = .1) 
                # self.right_side.text = ''
                animi.start(self.right_side)
                return
        def small(kk):
            global count
            global active
            if count <= 1:
                if active == False:
                    Clock.schedule_once(self.removeall,0)
                else:
                    Clock.schedule_once(partial(self.removeall,'removeControl'),0)
            count = 0

        Clock.schedule_once(small,0.5)
        
    def playlist_details(self):
        global lastvid
        if self.B_state == 'playlist':

            self.B_state = 'videos'
            self.buttton2.text = 'Videos Here'
            self.is_playlist = True
            self.list1 = video_playlist.copy()
            self.list1.extend(audio_playlist)
            print(self.list1)
            try:
                self.bottompart.remove_widget(self.stack_0)
            except:
                pass
            self.listings(self.list1)

        elif self.B_state == 'videos':
            self.B_state = 'playlist'
            self.buttton2.text = 'Playlists Here'
            self.is_playlist = False
            self.list1 = all_videos.copy()
            self.list1.reverse()
            try:
                self.bottompart.remove_widget(self.stack_0)
                self.listings(self.list1)
                self.bottompart.add_widget(self.stack_0)
            except:
                pass

        elif self.B_state == 'details':
            self.video.state = 'pause'
            # self.ctarget = self.target
            self.uno.details(self.ctarget)

    def goback(self,dd):
        
        self.list1 = all_videos.copy()
        self.list1.reverse()
        self.vidclick.remove_widget(self.floating)
        
        self.vidclick.unbind(on_press = self.vidcontrol)
        self.vidclick.add_widget(self.immg)
        self.vidclick.add_widget(self.txtings)
        self.bottompart.remove_widget(self.stack_1)
        self.bottompart.add_widget(self.stack_0)
        self.vidclick.unbind(on_press = self.previous)
        self.vidclick.bind(on_press = self.returner)

        self.buttton1.unbind(on_press = self.goback)
        self.buttton1.bind(on_press = self.gobackback)
        self.updater.cancel()
        if self.video.state == 'play':
            self.video.state = 'pause'
            self.btn_nav2.text = '||'

        self.uno.ids.play.unbind(on_press = self.switch_vid)
        self.uno.ids.play.bind(on_press = self.play_op)
        if self.is_playlist:
            self.buttton2.text = 'Videos Here'
            self.B_state = 'videos'

        elif not self.is_playlist:
            self.buttton2.text = 'Playlists Here'
            self.B_state = 'playlist'
        self.target_playlist = None

        # elif not self.target_playlist:

    def gobackback(self,dd):
        # if self.video.state == 'play':
        #     self.video.state = 'pause'
     
        self.manager.current = 'first'

    def returner(self,ll):
        self.vidclick.remove_widget(self.immg)
        self.vidclick.remove_widget(self.txtings)
        

        self.vidclick.add_widget(self.floating)
        self.vidclick.unbind(on_press = self.returner)
        # self.vidclick.bind(on_press = self.previous)
        # self.vidclick.bind(on_press = self.vidcontrol)

        self.bottompart.remove_widget(self.stack_0)
        self.bottompart.add_widget(self.stack_1)

        self.buttton1.unbind(on_press = self.gobackback)
        self.buttton1.bind(on_press = self.goback)

        self.uno.ids.play.unbind(on_press = self.play_op)
        self.uno.ids.play.bind(on_press = self.switch_vid)

        self.buttton2.text = 'Details Here |^|'
        self.B_state = 'details'


"""
"""


class chooser(Screen):
    def floaded(self,selection):
        print(selection[0].split('\\')[-1])
        self.manager.current = 'Download Videos'
        jk = self.manager
        olo = jk.get_screen('Download Videos')
        olo.update(selection)

class PlayAudiio(Screen):
    def __init__(self, **kwargs):
        super(PlayAudiio, self).__init__(**kwargs)
        self.selections = []
        self.select = False
        self.target = None
        self.ctarget = None
        self.selection_frame = []
        self.list1 = objectslist.copy()
        self.list1.reverse()
        self.is_playlist = False
        self.target_playlist = None
        self.aud_placeholder = None
        self.is_opened_with = False
        self.play_state = 'N'
        

 
        self.uno = settings()
        self.jj = selections()
        jk = self.uno.ids.jkk
        jk.bind(on_press = self.seli_mode)
        jso = self.uno.ids.back
        jso.bind(on_press = self.rem)

        dman = self.jj.ids.done
        dman.bind(on_press = self.opp)

        self.uno.ids.play.bind(on_press = self.play_op)
        self.uno.ids.details.bind(on_press = self.detail)
        self.uno.ids.delete.bind(on_press = self.delete)
        self.uno.ids.newplay.bind(on_press = self.newp)

        # Clock.schedule_once(partial(self.listinggs,10), 2)


        self.bind(size = self.upin)

    def upin(self, *args):
        self.canvas.clear()
        self.listinggs(self.list1)

    def listinggs(self,k):
        self.holderr = BoxLayout()
        self.holderr.size_hint = (1,1)
        self.holderr.orientation = 'vertical'
        self.holderr.padding = (20,20,5,0)


        self.backe = audioid()
        self.backe.background_color = (.01,.01,.01,1)
        self.backe.background_normal = ''
        self.backe.size_hint = (.1,.05)

        if self.is_opened_with:
            self.backe.bind(on_press = self.sudo_back)
        else:
            self.backe.bind(on_press = self.backef)


        self.letter = Label()
        self.letter.text = '<-'
        self.letter.font_size = 30
        self.letter.size_hint = (.1,.5)
        self.letter.pos_hint = {"x":0,"top":1}
        self.letter.valign = 'center'
        self.letter.halign = 'left'

        self.backe.add_widget(self.letter)
        self.holderr.add_widget(self.backe)
        self.add_widget(self.holderr)

        if not k:
            self.aud_placeholder = BoxLayout()
            self.aud_placeholder.size_hint = (1,1)
            txt = Label()
            txt.text = 'Nothing here!'
            self.aud_placeholder.add_widget(txt)
            self.holderr.add_widget(self.aud_placeholder)
            return 0
        if self.aud_placeholder:
            self.holderr.remove_widget(self.aud_placeholder)
            self.aud_placeholder = None


        self.view = ScrollView()
        self.view.size_hint = (1,1)

        self.showall = GridLayout()
        self.showall.cols = 1
        self.showall.spacing = 15
        self.showall.size_hint = (1,None)
        self.showall.bind(minimum_height = self.showall.setter('height'))
        for i in k:
            self.items = audioid()
            self.items.background_color = (0,0,0,1)
            self.items.background_normal = ''
            self.items.bind(on_press = partial(self.pop,i))

            self.items.size_hint = (1,None)
            self.items.height = 50
            self.items.spacing = 0

            self.img_box = BoxLayout()
            self.img_box.size_hint = (.35,1)

            self.imgs = Image()
            self.imgs.source = i.thumbnail_address
            # self.imgs.source = holki_audi.thumbnail_address
            self.imgs.size_hint = (1,1)
            self.imgs.pos_hint = {"x":0,"y":0}
            self.imgs.fit_mode = 'fill'

            self.img_box.add_widget(self.imgs)
            self.items.add_widget(self.img_box)

            self.box_cont = BoxLayout()
            self.box_cont.orientation = 'vertical'
            self.box_cont.size_hint = (1,1)
            self.box_cont.padding = 0
            self.box_cont.spacing = 0
            # self.box_cont.width = 240

            self.titles = Label()
            self.titles.text = f'{string_cut(i.title,27)}'
            self.titles.size_hint = (1,.1)
            self.titles.valign = 'center'
            self.titles.halign = 'left'
            self.titles.font_size = 17
            self.titles.pos_hint = {"x":.3}
            self.titles.text_size = self.size



            self.box_cont.add_widget(self.titles)

            self.author = Label()
            self.author.text = f'Author: {string_cut(i.author,27)}'
            self.author.valign = 'center'
            self.author.halign = 'left'
            self.author.font_size = 13
            self.author.size_hint = (1,.1)
            self.author.pos_hint = {"x":.3}
            self.author.text_size = self.size
            self.box_cont.add_widget(self.author)

            self.items.add_widget(self.box_cont)
            self.showall.add_widget(self.items)

        self.view.add_widget(self.showall)
        self.holderr.add_widget(self.view)

    def detail(self,k):
        self.uno.details(self.target)

    def open_with(self,playlist,k):
        try:
            self.remove_widget(self.holderr)
        except:
            pass
        self.is_opened_with = True
        self.list1 = k
        self.target_playlist = playlist
        self.listinggs(k)

    def sudo_back(self,l):
        self.manager.current = 'Watch Videos'
        self.sudo_restore()

    def sudo_restore(self):
        self.is_opened_with = False
        self.list1 = objectslist.copy()
        self.remove_widget(self.holderr)
        self.listinggs(self.list1)
        self.backe.unbind(on_press = self.sudo_back)
        self.backe.bind(on_press = self.backef)

    def newp(self,p):
        self.uno.dismiss()
        kk = newplaylist()
        kk.ids.create.bind(on_press = partial(self.create,kk))
        kk.open()

    def create(self,cre,l):
        if self.selections:
            add_playlist(cre.ids.playlist.text, self.selections[0].type ,self.selections)
            self.rem("k")
            cre.dismiss()
        else:
            cre.dismiss()

    def pop(self,i,j):
        # kk = download()
        if self.select == True:
            if j in self.selections:
                j.background_color = (0,0,0,1)
                self.selection_frame.remove(j)
                self.selections.remove(i)
            else:
                j.background_color = (.1,.1,.2,.6)
                self.selection_frame.append(j)
                self.selections.append(i)
            self.jj.ids.count.text = f'{len(self.selections)} selected'
        else:
            self.target = i
            self.uno.open()

    def seli_mode(self,k):
        self.uno.dismiss()
        self.select = True
        try:
            self.add_widget(self.jj)
        except:
            pass

    def rem(self, k):
        if self.select == True:
            self.select = False
            self.remove_widget(self.jj)
            for i in self.selection_frame:
                i.background_color = (0,0,0,1)
            self.selections = []
            self.selection_frame = []
            self.uno.dismiss()
            self.jj.ids.count.text = '0 selected'
        else:
            self.uno.dismiss()

    def opp(self,i):
        self.uno.open()

    def switcher(self):
        self.remove_widget(self.holderr)
        self.play()

    def play_op(self,j):
        if self.target:
            self.ctarget = self.target
            self.uno.dismiss()
            self.switcher()

    def delete(self,k):
        if self.select:
            if self.is_opened_with:
                self.uno.dismiss()
                delete_playlist(self.target_playlist, self.selections)
                self.rem("k")
            else:
                self.uno.dismiss()
                for i in self.selections:
                    delete(i)
                self.rem("k")
        else:
            if self.is_opened_with:
                self.uno.dismiss()
                delete_playlist(self.target_playlist,[self.target])
            else:
                self.uno.dismiss()
                delete(self.target)

        self.manager.refresha()

    def play(self):
        self.sound = SoundLoader.load(self.ctarget.address)
        self.sound.play()

        self.container = BoxLayout(orientation = 'vertical')
        self.container.size_hint = (1,1)
        
        self.topsection = FloatLayout()
        self.topsection.size_hint = (1,.1)
        self.backi = Button()
        self.backi.background_color = (0,0,0,0)
        self.backi.background_normal = ''
        self.backi.text = "<-"
        self.backi.bind(on_press = self.goback)
        self.backi.font_size = 30
        self.backi.size_hint = (.2,1)
        self.backi.pos_hint = {"x":0, "top":1}

        self.topsection.add_widget(self.backi)



        self.midsection = AnchorLayout()
        self.midsection.size_hint = (1,1)
        self.midsection.anchor_x = "center"
        self.midsection.anchor_y = "center"
        self.packerr = BoxLayout(orientation = 'vertical')
        self.packerr.size_hint = (1,.7)

        self.audimg = Image()
        self.audimg.source = self.ctarget.thumbnail_address
        self.audimg.pos_hint = {"center_x":.5, "y":0}
        self.audimg.size_hint = (1,1)

        self.titlee = Label()
        self.titlee.text = string_cut(self.ctarget.title,47)
        self.titlee.valign = 'center'
        self.titlee.halign = 'left'
        self.titlee.pos_hint = {"x":0, "top":1}
        self.titlee.size_hint = (1,.1)
        
        self.author = Label()
        self.author.text = f'Author: {string_cut(self.ctarget.author,39)}'
        self.author.valign = 'top'
        self.author.halign = 'left'
        self.author.pos_hint = {"x":0, "top":1}
        self.author.size_hint = (1,.1)
        self.author.font_size = 12

        self.packerr.add_widget(self.audimg)
        self.packerr.add_widget(self.titlee)
        self.packerr.add_widget(self.author)
        self.midsection.add_widget(self.packerr)
        
        



        self.lastsection = BoxLayout(orientation = 'vertical')
        self.lastsection.size_hint = (1,.3)

        self.proggress = FloatLayout()
        self.proggress.size_hint = (1,.1)

        self.loopshuffle = Button()
        self.loopshuffle.size_hint = (None,None)
        self.loopshuffle.height = 12
        self.loopshuffle.width = 10
        self.loopshuffle.text = self.play_state
        self.loopshuffle.bind(on_press = self.chplaytype)
        self.loopshuffle.background_color = (.15,.15,.15,15)
        self.loopshuffle.background_normal = ''
        self.loopshuffle.pos_hint = {"x":.1,"center_y":1}
        self.proggress.add_widget(self.loopshuffle)

        self.timmer = Label()
        self.timmer.text = '00:00/00:00'
        self.timmer.font_size = 10
        self.timmer.pos_hint = {"right":1,"center_y":1}
        self.timmer.size_hint = (.2,.2)
        self.timmer.valign = "center"
        self.timmer.halign = "right"
        self.proggress.add_widget(self.timmer)

        self.barr = ProgressBar()
        self.barr.max = 1
        self.barr.value = .5
        self.barr.size_hint = (1,.1)
        self.barr.pos_hint = {"x":0,"y":0}
        self.proggress.add_widget(self.barr)
        
        self.tdial = btndrag()
        self.tdial.size_hint = (None,None)
        self.tdial.height = 12
        self.tdial.width = 10
        self.tdial.background_color = (.15,.15,.15,15)
        self.tdial.background_normal = ''
        self.tdial.pos_hint = {"x":.5,"center_y":.05}
        self.proggress.add_widget(self.tdial)
        self.updater = Clock.schedule_interval(self.udatebar,0)




        self.controler = BoxLayout()
        self.controler.size_hint = (1,.25) 
        self.controler.pos_hint = {"center_x":0.5, "center_y":0.5}

        self.btn_nav1 = Button()
        self.btn_nav1.text = '<<'
        self.btn_nav1.bind(on_press = self.backward)
        self.btn_nav1.background_color = (0,0,0,0)
        self.btn_nav1.background_normal = ''
        self.btn_nav1.size_hint = (.5,1)

        self.btn_nav2 = Button()
        self.btn_nav2.text = '|>'
        self.btn_nav2.background_color = (0,0,0,0)
        self.btn_nav2.background_normal = ''
        self.btn_nav2.bind(on_press = self.playcontrol)
        self.btn_nav2.size_hint = (.5,1)

        self.btn_nav3 = Button()
        self.btn_nav3.text = '>>'
        self.btn_nav3.bind(on_press = self.forward)
        self.btn_nav3.background_color = (0,0,0,0)
        self.btn_nav3.background_normal = ''
        self.btn_nav3.size_hint = (.5,1)

        self.controler.add_widget(self.btn_nav1)
        self.controler.add_widget(self.btn_nav2)
        self.controler.add_widget(self.btn_nav3)


        self.lastsection.add_widget(self.proggress)
        self.lastsection.add_widget(self.controler)

        self.container.add_widget(self.topsection)
        self.container.add_widget(self.midsection)
        self.container.add_widget(self.lastsection)
        self.add_widget(self.container)

    def udatebar(self, kk):
        if self.tdial.pos_percent == None:
            self.sound.play()
            self.barr.value = (self.sound.get_pos() + 3)/self.sound.length
            self.tdial.pos_hint = {"center_x":self.barr.value, "center_y":.1}
            self.timmer.text = f'{self.timer(self.sound.get_pos())}/{self.timer(self.sound.length)}'
        
            if self.barr.value >= .95:
                self.tdial.pos_hint = {"right":1, "center_y":.1}

            if  self.sound.get_pos() >= (self.sound.length - 2):
                print('here got here')
                self.updater.cancel()
                self.sound.stop()
                self.playtype("p")

        else:
            self.barr.value = self.tdial.pos_percent
            print(round(self.tdial.pos_percent * self.sound.length))
            self.sound.seek(round(self.tdial.pos_percent * self.sound.length))
            self.timmer.text = f'{self.timer(self.sound.get_pos())}/{self.timer(self.sound.length)}'

    def timer(self, duration):
        hour = int((duration // 60) // 60)
        minute = int((duration // 60) % 60)
        seconds = int(duration % 60)
        if minute < 10:
            minute = f'0{minute}'
        if seconds < 10:
            seconds = f'0{seconds}'
        if hour:
            return f'{hour}:{minute}:{seconds}'
        else:
            return f'{minute}:{seconds}'

    def goback(self,d):
        try:
            self.sound.stop()
            self.updater.cancel()
        except:
            pass
        self.remove_widget(self.container)
        self.add_widget(self.holderr)
        
        self.uno.ids.play.unbind(on_press = self.play_op)
        self.uno.ids.play.bind(on_press = self.player)
        # self.uno.ids.play.bind(on_press = partial(self.player, self.target.address))

    def backef(self,d):
        self.manager.current = 'first'

    def player(self,jkl = None):
        self.remove_widget(self.container)
        self.play_op("k")

    def playcontrol(self,f):
        if self.sound.state == 'play':
            print("got here to the pause part")
            self.updater.cancel()
            self.sound.stop()
            self.btn_nav2.text = '||'

        elif self.sound.state == 'stop':
            self.btn_nav2.text = '|>'
            # k = round((self.sound.get_pos()/self.sound.length) * 100)
            k = round(self.sound.get_pos())
            self.sound.seek(k)
            self.sound.play()
            self.updater = Clock.schedule_interval(self.udatebar,0)

    def playtype(self,q):
        if self.loopshuffle.text == "L":
            if self.sound.loop == True:
                self.play_state = "L"
            else:
                self.play_state = "L"
                self.sound.loop = True
        elif self.loopshuffle.text == "S":
            # self.list_back = self.list1.copy()
            # random.shuffle(self.list1)
            self.play_state = "S"
            self.sound.loop = False
            self.ctarget = self.list1[random.randint(0, len(self.list1))]
            self.updater.cancel()
            self.sound.stop()
            # del self.sound
            self.remove_widget(self.container)
            self.play()
            
        elif self.loopshuffle.text == "N":
            if (self.list1.index(self.ctarget) + 1) >= len(self.list1):
                return 0
            else:
                self.play_state = "N"
                self.sound.loop = False
                self.ctarget = self.list1[self.list1.index(self.ctarget) + 1]
                self.updater.cancel()
                self.sound.stop()
                # del self.sound
                self.remove_widget(self.container)
                self.play()

    def chplaytype(self,j):
        if self.loopshuffle.text == "L":
            self.loopshuffle.text = "S"
        elif self.loopshuffle.text == "S":
            self.loopshuffle.text = "N"
        elif self.loopshuffle.text == "N":
            self.loopshuffle.text = "L"

    def forward(self,e):
        if (self.list1.index(self.ctarget) + 1) >= len(self.list1):
            return 0
        else:
            self.ctarget = self.list1[self.list1.index(self.ctarget) + 1]
            self.sound.stop()
            self.updater.cancel()
            del self.sound
            self.remove_widget(self.container)
            self.play()

    def backward(self,e):
        if (self.list1.index(self.ctarget) - 1) < 0:
            return 0
        else:
            self.ctarget = self.list1[self.list1.index(self.ctarget) - 1]
            self.updater.cancel()
            self.sound.stop()
            del self.sound
            self.remove_widget(self.container)
            self.play()

class SearchVideos(Screen):
    def __init__(self, **kwargs):
        super(SearchVideos, self).__init__(**kwargs)
        self.rcc = None
        self.holdall = BoxLayout()
        self.holdall.size_hint = (1,1)
        self.holdall.orientation = 'vertical'
        self.holdall.padding = (5,10)
        self.holdall.spacing = 20

        self.backe = BoxLayout()
        self.backe.size_hint = (1,.05)
        self.backe.spacing = 0

        self.backbtn = Button()
        self.backbtn.text = '<-'
        self.backbtn.font_size = 30
        self.backbtn.size_hint = (.1,.5)
        self.backbtn.pos_hint = {"x":0,"center_y":.5}
        self.backbtn.bind(on_press = self.backef)
        self.backbtn.background_color = (.1,.1,.1,0)
        self.backbtn.background_normal = ''
        
        self.textin = TextInput()
        self.textin.hint_text_color = (1,1,1,1)
        self.textin.foreground_color = (1,1,1,1)
        self.textin.background_color = (.1,.1,.1,1)
        self.textin.background_normal = ''
        self.textin.multiline = False
        self.textin.size_hint = (1,None)
        self.textin.height = 30
        self.textin.hint_text = 'Search'
        self.textin.pos_hint = {"x":0,"center_y":.5}
        self.textin.bind(on_text_validate = self.go)

        self.gobtn = Button()
        self.gobtn.text = 'Go'
        self.gobtn.size_hint = (.1,None)
        self.gobtn.height = 30
        self.gobtn.background_color = (.1,.1,.1,1)
        self.gobtn.background_normal = ''
        self.gobtn.bind(on_press = self.go)
        self.gobtn.pos_hint = {"right":1,"center_y":.5}

        self.backe.add_widget(self.backbtn)
        self.backe.add_widget(self.textin)
        self.backe.add_widget(self.gobtn)


        self.bottom = BoxLayout()
        self.bottom.size_hint = (1,1)

        self.labe = Label()
        self.labe.text = 'results are displayed here'
        self.labe.size_hint = (1,1)
        self.bottom.add_widget(self.labe)

        # self.listinggs(10)

        self.holdall.add_widget(self.backe)
        self.holdall.add_widget(self.bottom)
        self.add_widget(self.holdall)

        self.uno = download()

    def listinggs(self,k):
        self.view = ScrollView()
        self.view.size_hint = (1,1)

        self.showall = GridLayout()
        self.showall.cols = 1
        self.showall.spacing = 20
        self.showall.size_hint = (1,None)
        self.showall.bind(minimum_height = self.showall.setter('height'))
        self.num = 0
        def hm(j):
            if self.num == len(k):
                self.but = Button()
                self.but.text = 'get next results'
                self.but.size_hint = (1,None)
                self.but.height = 30
                self.but.background_color = (.1,.1,.1,1)
                self.but.background_normal = ''
                self.but.bind(on_press = self.kane)
                self.showall.add_widget(self.but)
                self.num = 0
                self.cman.cancel()
            i = k[self.num]
            self.items = audioid()
            self.items.bind(on_press = partial(self.uno.pop, i, self))
            self.items.orientation = 'vertical'
            self.items.background_color = (.1,.1,.1,.5)
            self.items.background_normal = ''

            self.items.size_hint = (1,None)
            self.items.height = 275

            self.imgs = AsyncImage()
            self.imgs.source = i.thumbnail_url
            self.imgs.size_hint = (1,1)
            self.imgs.pos_hint = {"x":0,"y":0}
            self.items.add_widget(self.imgs)

            self.titles = Label()
            self.titles.text = i.title
            # self.titles.size = self.titles.texture_size
            self.titles.text_size = self.size
            self.titles.valign = 'center'
            self.titles.halign = 'left'
            self.titles.font_size = 15
            self.titles.size_hint = (1,.2)
            self.titles.pos_hint = {"x":.02}
            self.items.add_widget(self.titles)

            self.authors = Label()
            self.authors.text = f'Author: {i.author}'
            self.authors.text_size = self.size
            self.authors.valign = 'center'
            self.authors.halign = 'left'
            self.authors.font_size = 12
            self.authors.size_hint = (1,.1)
            self.authors.pos_hint = {"x":.02}
            self.items.add_widget(self.authors)

            self.duration = Label()
            self.duration.text = f'Duration: {self.timer(i.length)}'
            self.duration.text_size = self.size
            self.duration.valign = 'center'
            self.duration.halign = 'left'
            self.duration.font_size = 12
            self.duration.size_hint = (1,.1)
            self.duration.pos_hint = {"x":.02}
            self.items.add_widget(self.duration)
            self.showall.add_widget(self.items)
            self.num += 1

        self.cman = Clock.schedule_interval(hm, 0)

        try:
            self.bottom.remove_widget(self.labe)
            self.view.add_widget(self.showall)
            self.bottom.add_widget(self.view)
        except:
            pass

    def timer(self, duration):
        hour = int((duration // 60) // 60)
        minute = int((duration // 60) % 60)
        seconds = int(duration % 60)
        if minute < 10:
            minute = f'0{minute}'
        if seconds < 10:
            seconds = f'0{seconds}'
        if hour:
            return f'{hour}:{minute}:{seconds}'
        else:
            return f'{minute}:{seconds}'

    def backef(self,d):
        self.manager.current = 'first'

    def go(self,sel):
        word = self.textin.text
        try:
            holder = search(word)
        except:
            self.labe.text = 'NO INTERNET CONNECTION'
            return 0
        # threading.Thread(target=self.listinggs, args= (holder,)).start()
        # self.labe.text = 'loading...'
        self.listinggs(holder)
        self.gobtn.unbind(on_press = self.go)
        self.gobtn.bind(on_press = self.kane)
        self.textin.unbind(on_text_validate = self.go)
        self.textin.bind(on_text_validate = self.kane)

    def kane(self,sel):
        try:
            self.bottom.remove_widget(self.view)
            self.bottom.remove_widget(self.labe)
        except:
            pass
        self.bottom.add_widget(self.labe)
        word = self.textin.text
        try:
            holder = search(word)
        except:
            self.labe.text = 'NO INTERNET CONNECTION'
            return 0
        self.listinggs(holder)

class DownloadVideos(Screen):
    def __init__(self, **kwargs):
        super(DownloadVideos, self).__init__(**kwargs)
        self.amount = 'ALL'
        self.resolution = 'high'
        self.d_audio = False
        self.filename = None
        self.loading = downloading()

    def update(self,selection):
        self.filename = selection[0]
        na = self.filename.split('\\')[-1]
        self.ids.filebtn.text = na
    
    def gotofilefunc(self):
        self.manager.current = 'chooser'
        
    def num(self,sel,state,res):
        self.amount = res

    def quality(self,sel,state,res):
        self.resolution = res

    def audi(self, se):
        self.d_audio = se.active

    def runni(self):
        print(self.ids.title.text)
        print(self.ids.author.text)
        print(self.ids.url.text)
        print(self.amount)
        print(self.resolution)
        title = self.ids.title.text
        author = self.ids.author.text
        url = self.ids.url.text

        if url:
            self.loading.looper(self)
            threading.Thread(target= use_link, args= (url, self.resolution, self.d_audio)).start()

        elif title and author:
            if self.d_audio == False:
                self.loading.looper(self)
                threading.Thread(target= download_video, args= (fetch_video(title, author), self.resolution)).start()
            elif self.d_audio == True:
                self.loading.looper(self)
                threading.Thread(target= download_audio, args= (fetch_video(title, author), self.resolution)).start()

        elif title:
            if self.d_audio == False:
                self.loading.looper(self)
                threading.Thread(target= download_video, args= (fetch_video(title), self.resolution)).start()
            elif self.d_audio == True:
                self.loading.looper(self)
                threading.Thread(target= download_audio, args= (fetch_video(title), self.resolution)).start()

        elif self.filename:
            valu = load_list(self.filename)
            if 'author' not in valu and 'title' in valu:
                self.loading.looper(self)
                threading.Thread(target= download_all_from_list, args= (self.resolution, False, self.d_audio)).start()
            elif 'author' in valu and 'title' in valu:
                self.loading.looper(self)
                threading.Thread(target= download_all_from_list, args= (self.resolution, True, self.d_audio)).start()
            elif 'url' in valu:
                self.loading.looper(self)
                threading.Thread(target= download_all_from_url_list, args= (self.resolution,False, self.d_audio)).start()

class DownloadPlaylist(Screen):
    def __init__(self, **kwargs):
        super(DownloadPlaylist, self).__init__(**kwargs)
        self.amount = 'ALL'
        self.resolution = 'high'
        self.d_audio = False
        self.loading = downloading()

    def num(self,sel,state,res):
        self.amount = res

    def quality(self,sel,state,res):
        self.resolution = res

    def audi(self, se):
        self.d_audio = se.active

    def runni(self):
        print(self.ids.name.text)
        print(self.ids.url.text)
        print(self.amount)
        print(self.resolution)
        url = self.ids.url.text
        title = self.ids.name.text
        if url:
            self.loading.looper(self)
            threading.Thread(target = download_playlist, args = (url, self.resolution, title, self.amount, self.d_audio)).start()
        else:
            print('please input url')

class DownloadChannel(Screen):
    def __init__(self, **kwargs):
        super(DownloadChannel, self).__init__(**kwargs)
        self.amount = 'ALL'
        self.resolution = 'high'
        self.d_audio = False
        self.loading = downloading()
        
    def num(self,sel,state,res):
        self.amount = res

    def quality(self,sel,state,res):
        self.resolution = res

    def audi(self, se):
        self.d_audio = se.active

    def runni(self):
        print(self.ids.name.text)
        print(self.ids.url.text)
        print(self.amount)
        print(self.resolution)
        stri = self.ids.name.text
        stri = stri.replace(" ", "")
        stri = f"https://youtube.com/@{stri}"
        url = self.ids.url.text
        print(stri)
        print(url)

        
        if self.ids.url.text:
            self.loading.looper(self)
            threading.Thread(target= download_channel, args= (url, self.resolution, self.amount, self.d_audio)).start()

        elif self.ids.name.text:
            self.loading.looper(self)
            threading.Thread(target = download_channel, args= (stri, self.resolution, self.amount, self.d_audio)).start()

class TubeApp(App):
    def on_start(self):
        # load_data()
        pass

tube = TubeApp()
load_data()