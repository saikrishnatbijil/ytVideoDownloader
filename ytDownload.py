from pytube import YouTube

link = input("Enter Link : ")
yt = YouTube(link)

print("Title : ", yt.title)
print("Views : ",yt.views)

ok = input("Is it this one Type YES if it is the one yo are looking for : ")
if ok == "YES":
    yd = yt.streams.get_highest_resolution()
    yd.download('/Users/macintoshhd/Documents/Dowloaded files')