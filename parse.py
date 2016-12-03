from collections import defaultdict

# triplets (User MD5, Song MD5, Play counts)
file_triplets = open('triplets.txt', 'r')
file_users = open('users.txt','w')
file_songs = open('songs.txt','w')
file_valid = open('validation.txt','w')

song_count = defaultdict(int)
users = set()
songs = set()

for triplet in file_triplets:
   (u_md5, s_md5, count) = triplet.split()
   users.add(u_md5)
   songs.add(s_md5)
   song_count[u_md5] += 1

for user in users:
    file_users.write(user+"\n")

for song in songs:
    file_songs.write(song+"\n")

file_triplets.close()
file_triplets = open('triplets.txt', 'r')
i_song = 0
for triplet in file_triplets:
   (u_md5, s_md5, count) = triplet.split()
   s_cnt = song_count[u_md5]
   if(i_song < s_cnt/2):
        file_valid.write(triplet)
        i_song = i_song + 1
   if(i_song == s_cnt - 1):
       i_song=0

file_triplets.close()
file_songs.close()
file_valid.close()
file_users.close()