def imp():
      try :
            import pytube
            import ffmpeg
      except Exception as e:
            a = input('some required libraries are not installed. note that without them, the program can not work\n\tdo you want to install it?[Y/N] ')
            if a=='y' or a=='Y':
                  from subprocess import call 
                  call(['pip','install','pytube'])
                  call(['pip','install','ffmpeg'])
            else:
                  print('Program closed.')
                  exit()

#progress showing 
def progress_function(stream, chunk, bytes_remaining):
      try:
            s = 26
            size = stream.filesize
            l = int((bytes_remaining/size)*s) 
            c = s-l
            rl = ' '
            rl = rl*l
            rc = '█'
            rc = rc*c
            if(bytes_remaining>1000000):
                  print('[',rc,rl,']\t',bytes_remaining/1000000,"\tmb left",end='\r')
            else:
                  print('[',rc,rl,']\t',bytes_remaining/1024,"\tkb left",end='\r')
      except Exception as e:
            raise(e)
            
"""     `````````````_____`````````````               """            
"""    /////////////  THE  \\\\\\\\\\\\\\             """
"""   /////////////  ACTUAL \\\\\\\\\\\\\\            """
"""  /////////////    CODE   \\\\\\\\\\\\\\           """
""" ///////////// STARTS HERE \\\\\\\\\\\\\\          """

# importing the needed libraries
imp()
import pytube
import ffmpeg
#     getting input and making the video ready
while True:
      url = input('insert your youtube link:\t')
      try:
            video = pytube.YouTube(url,on_progress_callback=progress_function)
            break
      except Exception as e:
            print('video not found!')

isprogressive = True
#     printing the tags of different types of the video
while True:
      x = input('Would you like to download a progrssive video?[Y/N]')
      if x=='Y' or x=='y':
      #     Downloading a progressive file 
            isprogressive = True
            for stream in video.streams.filter(progressive=True):
                  print('\titag: ',stream.itag,'\ttype: ',stream.mime_type,'\tres: ',stream.resolution,'\tfps: ',stream.fps)
            tag = input('which tag would you like to download:\t')
            print(video.streams.get_by_itag(tag))
            q = input('is it the right tag you wish to download? [Y/N]').strip()
            if(q=='Y' or q=='y'):
                  break
      else :
      #     Downloading a non progressive file \ getting AUDIO 
            isprogressive = False
            
            for stream in video.streams.filter(only_audio=True):
                  print('\titag: ',stream.itag,'\ttype: ',stream.mime_type,'\tres: ',stream.resolution,'\tfps: ',stream.fps)
            a_tag = input('which tag would you like to download (audio):\t')
            print(video.streams.get_by_itag(a_tag))
            q = input('is it the right tag you wish to download? [Y/N]').strip()
            if(q=='N' or q=='n'): continue
      #     getting VIDEO 
            for stream in video.streams.filter(only_video=True):
                  print('\titag: ',stream.itag,'\ttype: ',stream.mime_type,'\tres: ',stream.resolution,'\tfps: ',stream.fps)
            v_tag = input('which tag would you like to download (video):\t')
            print(video.streams.get_by_itag(v_tag))
            q = input('is it the right tag you wish to download? [Y/N]').strip()
            if(q=='Y' or q=='y'):
                  break
#     set destination to store the video in.
detination = input('destination:[leave empty for \'/sdcard/ADM\']\t')


#     downloading
if isprogressive:
      print('downloading...')
      try:
            stream = video.streams.get_by_itag(tag)
            try:
                  stream.download(destination)
            except :
                  stream.download('/sdcard/ADM')
            print('download sucessful!')
      except Exception as e:
            print(e)
else :
      print('downloading audio...')
      try:
            stream = video.streams.get_by_itag(a_tag)
            try:
                  afile=stream.download(destination,'a')
            except:
                  afile=stream.download('/sdcard/ADM','a')
            print('downloading audio file sucessful!')
      except Exception as e:
            print(e)
      
      print('downloading video...')
      try:
            stream = video.streams.get_by_itag(v_tag)
            try:
                  vfile=stream.download(destination)
            except:
                  vfile=stream.download('/sdcard/ADM')
            print('downloading video file sucessful!')
      except Exception as e:
            print(e)
      
      try:
            print('combining the audio file with video file...')
            import os 
            os.system('apt-get install ffmpeg')
            input_video = ffmpeg.input(vfile)
            input_audio = ffmpeg.input(afile)
            ffmpeg.concat(input_video, input_audio, v=1, a=1).output(os.path.splitext(vfile)[0]+'e.mp4').run()
            os.remove(afile)
            os.remove(vfile)
            os.rename(os.path.splitext(vfile)[0]+'e.mp4',os.path.splitext(vfile)[0]+'.mp4')
      except Exception as e:
            print(e)