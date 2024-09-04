from sqlite3 import *

db = connect('DataBase.db')

c = db.cursor()


#Data for Artist 
datas = [('tuyu@gmail.com','tuyu','Rei','TUYU','False',0),\
('yoasobi@gmail.com','yoasobi','Ikura','YOASOBI','False',0),\
('maroon5@gmail.com','maroon','Adam','Maroon 5', 'False',0),\
('yorushika@gmail.com','yorushika', 'Suis', 'Yorushika', 'False',0),\
('lisa@gmail.com', 'lisa', 'Risa', 'LiSA', 'False',0),\
('radwimps@gmail.com', 'radwimps', 'Noda', 'Radwimps', 'False',0),\
('eve@gmail.com', 'eve', 'Keitora', 'Eve', 'False',0),\
('mafumafu@gmail.com', 'mafumafu', 'Mafumafu', 'Mafumafu', 'False',0),\
('yonezu@gmail.com', 'yonezu' , 'Yonezu', 'Kenshi Yonezu', 'False',0),\
('miku@gmail.com', 'miku', 'Fujita', 'Hatsune Miku', 'False',0)\
]


#Insert Data into Artist Table
for data in datas:
    c.execute('''INSERT INTO Artist (\
    email, password, name, username, login, balance)\
    VALUES(?,?,?,?,?,?)''', data)



#Data for Songs
songs = [(1, "TUYU - If there was an endpoint", "tuyu1.jpg", "https://www.youtube.com/watch?v=B-1Yw9PebRg", 'IfThereWasAnEndpoint.mp3'),\
(1, "TUYU - Loser Girl", "tuyu2.jpg", "https://www.youtube.com/watch?v=6rg4cYlAKOc&ab_channel=%E3%83%84%E3%83%A6", 'LoserGirl.mp3'),\
(2, "YOASOBI - Racing Into The Night", "yoasobi1.jpg", "https://www.youtube.com/watch?v=x8VYWazR5mE&ab_channel=Ayase%2FYOASOBI", 'RacingIntoTheNight.mp3'),\
(2, "YOASOBI - Kaibustu", "yoasobi2.jpg", "https://www.youtube.com/watch?v=dy90tA3TT1c&ab_channel=Ayase%2FYOASOBI", 'kaibutsu.mp3'),\
(3, "Maroon 5 - Sugar", "maroon1.jpg", "https://www.youtube.com/watch?v=09R8_2nJtjg&ab_channel=Maroon5VEVO", 'Sugar.mp3'),\
(3, "Maroon 5 - Maps", "maroon2.jpg", "https://www.youtube.com/watch?v=Y7ix6RITXM0&ab_channel=Maroon5VEVO", 'Maps.mp3'),\
(4, "Yorushika - Say It", "yorushika1.jpg", "https://www.youtube.com/watch?v=F64yFFnZfkI&ab_channel=%E3%83%A8%E3%83%AB%E3%82%B7%E3%82%AB%2Fn-bunaOfficial", 'SayIt.mp3'),\
(4, "Yorushika - Raining With Cappuccino", "yorushika2.jpg", "https://www.youtube.com/watch?v=PWbRleMGagU&ab_channel=%E3%83%A8%E3%83%AB%E3%82%B7%E3%82%AB%2Fn-bunaOfficial", 'RainigWithCap.mp3'),\
(5, "LiSA - Gurenge", "lisa1.jpg", "https://www.youtube.com/watch?v=XjvaJH8aRc0&ab_channel=AnimeOST", 'Gurenge.mp3'),\
(5, "LiSA - Homura", "lisa2.jpg", "https://www.youtube.com/watch?v=4DxL6IKmXx4&ab_channel=LiSAOfficialYouTube", 'Homura.mp3'),\
(6, "Radwimps - Zen Zen Zense", "radwimps1.jpg", "https://www.youtube.com/watch?v=PDSkFeMVNFs&ab_channel=RADWIMPS",'Zen.mp3'),\
(6, "Radwimps - Is There Anything That Love Can Do?", "radwimps2.jpg", "https://www.youtube.com/watch?v=EQ94zflNqn4&ab_channel=RADWIMPS", 'IsThereAnythingLoveCanDo.mp3'),\
(7, "Eve - Kaikai Kitan", "eve1.jpg", "https://www.youtube.com/watch?v=1tk1pqwrOys&ab_channel=Eve", 'KaiKaiKitan.mp3'),\
(7, "Eve - Dramaturgy", "eve2.jpg", "https://www.youtube.com/watch?v=jJzw1h5CR-I&ab_channel=Eve", 'Dramaturgy.mp3'),\
(8, "Mafumafu - Life Hates Us Now", "mafu1.jpg", "https://www.youtube.com/watch?v=eq8r1ZTma08&ab_channel=%E3%81%BE%E3%81%B5%E3%81%BE%E3%81%B5%E3%81%A1%E3%82%83%E3%82%93%E3%81%AD%E3%82%8B", 'LifeHatesUsNow.mp3'),\
(8, "Mafumafu - I want to be a girl", "mafu2.jpg", "https://www.youtube.com/watch?v=ucbx9we6EHk&ab_channel=%E3%81%BE%E3%81%B5%E3%81%BE%E3%81%B5%E3%81%A1%E3%82%83%E3%82%93%E3%81%AD%E3%82%8B", 'IWantToBeAGirl.mp3'),\
(9, "Kenshi Yonezu - Peace Sign", "kenshi1.jpg", "https://www.youtube.com/watch?v=9aJVr5tTTWk&ab_channel=%E7%B1%B3%E6%B4%A5%E7%8E%84%E5%B8%AB", 'PeaceSign.mp3'),\
(9, "Kenshi Yonezu - Lemon", "kenshi2.jpg", "https://www.youtube.com/watch?v=SX_ViT4Ra7k&ab_channel=%E7%B1%B3%E6%B4%A5%E7%8E%84%E5%B8%AB", 'Lemon.mp3'),\
(10, "Hatsune Miku - Senbonzakura", "miku1.jpg", "https://www.youtube.com/watch?v=Mqps4anhz0Q&ab_channel=googoo888", 'Senbonzakura.mp3'),\
(10, "Hatsune Miku - First Storm", "miku2.jpg", "https://www.youtube.com/watch?v=L7BxD7HHWl4&ab_channel=DECO%2a27", 'FirstStorm.mp3')\
]


for song in songs:
    c.execute('''INSERT INTO Songs(\
artist_id, name_of_song, picture, youtube_link, audio)\
VALUES(?,?,?,?,?)''', song)


#Dummy data for Consumer
c.execute('''INSERT INTO Consumer(\
email, password, name, username, login, balance)\
VALUES(?,?,?,?,?,?)''', ('justin@gmail.com', 'justin', 'Justin', 'DraSlayer', 'False', 100))


db.commit()
db.close()
