from PIL import Image, ImageSequence
from luma.core.interface.serial import spi, noop
from luma.led_matrix.device import max7219
from pytube import YouTube
import time
import ffmpeg
import os
serial = spi(port=0, device=0, gpio=noop())
device = max7219(serial,width=32, height=32, block_orientation=-90, rotate=0, blocks_arranged_in_reverse_order=0 )
file = "output.gif"
size = [32,32] # change to use capabilities instead
thresh = 127
thresh = 255 - thresh
out_file = "done"
led_frames = {"info":[], "frames":[]}
device.contrast(100)


def rev_rows(matrix):
    for y in range(int(size[1]/16)):
        y += 1
        y *= 2
        #print("Y Val: " + str(y))
        box = (0,((y-1)*8),size[0],(y*8))
        #print("Box:  " + str(box))
        pog = matrix.crop(box).rotate(180)
        matrix.paste(pog, box)
    return matrix
        
        
def get_mp4(link):
    try:
        yt = YouTube(link)
        global mp4_file
        streams = yt.streams.filter(file_extension="mp4")
        print(title)
        stream = streams.get_lowest_resolution()
        mp4_file = stream.defualt_filename
        stream.download()
    except:
        print("broken link or bad connection")

def mp4togif(filename):
    (
    ffmpeg
    .input('input.mp4')
    .filter(stream, 'fps', fps=30, round='up')
    .scale(size[0], size[1])
    .output('processed.gif')
    .run()
    )
    (
    ffmpeg
    .input('input.mp4')
    .filter("vn")
    .acodec("copy")
    .output('processed.mp3')
    .run()
    )
    global file
    file = "processed.gif"
    global audio
    file = "processed.mp3"
    

def gifs(img):
    # index = 0
    led_frames["info"] = img.info
    frame_list = []
    while(img.tell() < img.n_frames):
        obj = (Image.eval(img.convert("L").resize(size), lambda x: ((x <= thresh)*255)))
        obj = rev_rows(obj)
        frame_list.append(obj)
        led_frames["frames"].append(obj.convert("1"))
        # with np.printoptions(threshold=np.inf):
        #     print(np.asarray(frame_list[index]))
        # index += 1
        
        try:
            img.seek(img.tell() + 1)
        except EOFError:
            #frame_list[0].save(out_file, save_all=True, append_images=frame_list[1:], duration=img.info["duration"])
            return


def processing(img):
    global out_file
    global led_frames
    led_frames["info"] = img.info
    print(img.info)
    if img.n_frames > 1:
        out_file += ".gif"
        gifs(img)
    else:
        out_file += ".bmp"
        img = Image.eval(img.convert("L").resize(size), lambda x: (x >= thresh)*255)
        img = rev_rows(img)
        img.save(out_file)
        led_frames["frames"] = [img.convert("1")]
        led_frames["info"]["duration"] = 10
        print(img.info)        
#         add way to pass in some arguments like how long and such
def display_final(device):
    device.show()
    device.clear()
    device.contrast(1)
    if len(led_frames["frames"]) > 1:
        #os.system("vlc processing.mp3")
        for frame in led_frames["frames"]:
            #print("hello")
            print(frame)
            device.display(frame)
            #display(frame)
            #display(led_frames["info"]["duration"])
            time.sleep((led_frames["info"]["duration"])/1000)
        print("gif is done")
        device.clear()
    else:
        print(led_frames["frames"])
        device.display(led_frames["frames"][0])
        #display(frame)
        time.sleep(led_frames["info"]["duration"])
    #device.clear()
        
def test():
    img = Image.open(file)
    processing(img)
    display_final(device)

#     processing(img)
#     print(led_frames["info"])
#     display(led_frames["frames"])
#     for frame in led_frames["frames"]:
#         print(frame)
#     global test_img    
#     test_img = led_frames["frames"][1]
#     test_img.show()
#     device.display(test_img)
#     print(np.asarray(test_img))

def vids():
    _less = input("is it a mp4/yt link?")
    if( _less == True):
        print("next")
        if(input("is it a yt link?") == True):
            link = input("Enter YouTube link to download   ")
            get_mp4(link)
        # title = title in get_mp4() or input("mp4 file")
        

# %%



