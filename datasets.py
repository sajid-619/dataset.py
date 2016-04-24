import json
import codecs
from collections import defaultdict 
from operator import itemgetter

##process the artist file
fp = codecs.open("artists.dat", encoding="utf-8")
fp.readline()
id2name = {}
name2id = {}
name_list = [] 
for line in fp: 
    l = line.strip() 
    fields = l.split("\t")
    id = int(fields[0])
    name = fields[1]
    tmp = {} 
    tmp['id'] = id
    tmp['name'] = name
    name_list.append(tmp)
    id2name[id] = name
    name2id[name] = id

##process the user to artists file
fpp = codecs.open("user_artists.dat", encoding="utf-8")
fpp.readline()
play_list = []
name_play_list = []
for line in fpp: 
    l = line.strip() 
    fields = l.split("\t") 
    uid = int(fields[0]) 
    aid = int(fields[1]) 
    weight = int(fields[2]) 
    tmpp = {}
    ttmpp = {}
    tmpp['userID'] = uid 
    tmpp['artistID'] = aid
    tmpp['weight'] = weight
    ttmpp['userID'] = uid 
    ttmpp['artistID'] = id2name[aid]
    ttmpp['weight'] = weight
    if aid in id2name:
        play_list.append(tmpp)          #aids are names
        name_play_list.append(ttmpp)    #aids are numbers   
        

##process the tags file
fppp = codecs.open("user_taggedartists.dat", encoding="utf-8")
fppp.readline()
tag_list = []
for line in fppp: 
    l = line.strip() 
    fields = l.split("\t")
    uid = int(fields[0])
    aid = int(fields[1]) 
    tid = int(fields[2]) 
    day = int(fields[3]) 
    mon = int(fields[4]) 
    yyr = int(fields[5]) 
    tmp = {}
    tmpp = {}
    tmp['userID'] = uid 
    tmp['artistID'] = aid
    tmp['tagID'] = tid
    tmp['day'] = day
    tmp['month'] = mon
    tmp['year'] = yyr
    if yyr >= 2000:
        if aid in id2name:
            tag_list.append(tmp)
            
##process the user friends
fpppp = codecs.open("user_friends.dat", encoding="utf-8")
fpppp.readline()
friend_list = []
for line in fpppp: 
    l = line.strip() 
    fields = l.split("\t") 
    userid = int(fields[0]) 
    friendid = int(fields[1]) 
    tmp = {}
    tmp['userID'] = userid 
    tmp['friendID'] = friendid
    friend_list.append(tmp)

fp.close()
fpp.close()
fppp.close()
fpppp.close()

##default dicts for queries
id2playcount = defaultdict(int)
for d in play_list:
    id2playcount[d['artistID']] += d['weight']
        
name2playcount = defaultdict(int)
for d in name_play_list:
    name2playcount[d['artistID']] += d['weight'] 
     
top_users = defaultdict(int)
for d in play_list:
    top_users[d['userID']] += d['weight']
    
most_listeners = defaultdict(int)
for d in play_list:
    most_listeners[d['artistID']] += 1
    
most_tags = defaultdict(int)
for d in tag_list:
    most_tags[d['artistID']] += 1
    
top_averages = defaultdict(int)             #one listener
for d in play_list:
    if most_listeners[d['artistID']] != 0:
        top_averages[d['artistID']] = id2playcount[d['artistID']] / most_listeners[d['artistID']]

top_averages_over50 = defaultdict(int)      #at least 50 different listeners
for d in play_list:
    if (most_listeners[d['artistID']] != 0) and (most_listeners[d['artistID']] >= 50):
        top_averages_over50[d['artistID']] = \
			id2playcount[d['artistID']] / most_listeners[d['artistID']]

friend_count = defaultdict(int)
for d in friend_list:
    friend_count[d['userID']] += 1
	
user_plays_over5friends = defaultdict(int)
for d in play_list:
	if friend_count[d['userID']] >= 5:
		user_plays_over5friends['pop_user_plays'] += d['weight']
		
user_plays_under5friends = defaultdict(int)
for d in play_list:
	if friend_count[d['userID']] < 5:
		user_plays_under5friends['unpop_user_plays'] += d['weight']
		
popular_users = defaultdict(int)        #users with over 5 friends
for d in play_list:
	if friend_count[d['userID']] >= 5:
		popular_users['pop_count'] += 1
		
unpopular_users = defaultdict(int)      #users with less than 5 friends
for d in play_list:
	if friend_count[d['userID']] < 5:
		unpopular_users['unpop_count'] += 1

id2users = defaultdict(list)
for d in play_list:
    id2users[d['artistID']].append(d['userID'])
    

def artist_sim(aid1, aid2):
    artid1 = set(tuple(id2users[aid1]))
    artid2 = set(tuple(id2users[aid2]))
    art_union = artid1 | artid2         # union
    art_intersection = artid1 & artid2  # intersection
    return float(len(art_intersection)) / float(len(art_union))

bd = {}
for rec in tag_list:
	group = bd.setdefault((rec['year'], rec['month']), {}).setdefault(rec['artistID'], 0)
	bd[(rec['year'], rec['month'])][rec['artistID']] += 1



#queries
######################################################
print
print 40 * '!'
print
print "1. Who are the top artists? "
sorted_ta = sorted(id2playcount.items(), key=itemgetter(1), reverse=True)
for name, t in sorted_ta[:10]: 
    print "   ", id2name[name], "("+str(name)+")", t
#######################################################
print
print 40 * '!'
print
print "2. Who are the top users? "
sorted_tu = sorted(top_users.items(), key=itemgetter(1), reverse=True)
for user, t in sorted_tu[:10]: 
    print "   ", user, t
######################################################
print
print 40 * '!'
print
print "3. What artists have the most listeners? "
sorted_ml = sorted(most_listeners.items(), key=itemgetter(1), reverse=True)
for name, c in sorted_ml[:10]: 
    print "   ", id2name[name], "("+str(name)+")", c
######################################################
print
print 40 * '!'
print
print "4. What artists have the highest average number of plays per listener? "
sorted_tavg = sorted(top_averages.items(), key=itemgetter(1), reverse=True)
for name, a in sorted_tavg[:10]:
    print "   ", id2name[name], "("+str(name)+")", id2playcount[name], most_listeners[name], a
######################################################
print
print 40 * '!'
print
print "5. What artists with at least 50 listeners have the"\
      " highest average number of plays per listener?  "
sorted_tavg50 = sorted(top_averages_over50.items(), key=itemgetter(1), reverse=True)
for name, a in sorted_tavg50[:10]:
    print "   ", id2name[name], "("+str(name)+")", id2playcount[name], most_listeners[name], a
######################################################
print
print 40 * '!'
print
print "6. Do users with five or more friends listen to more songs?  "
print "   ", "average number of song plays for users with 5 or more friends: "\
      , user_plays_over5friends['pop_user_plays'] / popular_users['pop_count']
print "   ", "average number of song plays for users with less than 5 friends: "\
      , user_plays_under5friends['unpop_user_plays'] / unpopular_users['unpop_count']
######################################################
print
print 40 * '!'
print
print "7. How similar are two artists?  "
print "   ",  id2name[735], "and", id2name[562], ": Jaccard index:", artist_sim(735,562) 
print "   ",  id2name[735], "and", id2name[89], ": Jaccard index:", artist_sim(735,89) 
print "   ",  id2name[735], "and", id2name[289], ": Jaccard index:", artist_sim(735,289) 
print "   ",  id2name[89], "and", id2name[289], ": Jaccard index:", artist_sim(89,289) 
print "   ",  id2name[89], "and", id2name[67], ": Jaccard index:", artist_sim(89,67) 
print "   ",  id2name[67], "and", id2name[735], ": Jaccard index:", artist_sim(67,735) 
######################################################
print
print 40 * '!'
print
print "8. For each month in 2005, what artists were tagged the most?  "
sorted_aug = sorted(bd[(2005,8)].items(), key=itemgetter(1), reverse=True)
print "Aug 2005"
for name, t in sorted_aug[:10]: 
    print "   ", id2name[name], "("+str(name)+"):", "num tags =", t
print

sorted_sep = sorted(bd[(2005,9)].items(), key=itemgetter(1), reverse=True)
print "Sep 2005"
for name, t in sorted_sep[:10]: 
    print "   ", id2name[name], "("+str(name)+"):", "num tags =", t
print

sorted_oct = sorted(bd[(2005,10)].items(), key=itemgetter(1), reverse=True)
print "Oct 2005"
for name, t in sorted_oct[:10]: 
    print "   ", id2name[name], "("+str(name)+"):", "num tags =", t
print

sorted_nov = sorted(bd[(2005,11)].items(), key=itemgetter(1), reverse=True)
print "Nov 2005"
for name, t in sorted_nov[:10]: 
    print "   ", id2name[name], "("+str(name)+"):", "num tags =", t
print

sorted_dec = sorted(bd[(2005,12)].items(), key=itemgetter(1), reverse=True)
print "Dec 2005"
for name, t in sorted_dec[:10]: 
    print "   ", id2name[name], "("+str(name)+"):", "num tags =", t
######################################################
print
print 40 * '!'
print
print '''9. For the 10 artists with the highest overall number of tags, list:
  a) the first month they entered the top 10 in terms of number of tags, and
  b) the number of months they were in the top 10 in terms of number of tags:  '''
top10 = {}                                                                  #dict of each month's top 10  
for k in bd.keys(): 
    sorted_bds = sorted(bd[k].iteritems(), key=itemgetter(1), reverse=True) #each month's top 10 
    for rec in sorted_bds[:10]:
        id, c = rec
        group = top10.setdefault(k, []).append(id)  
  
sorted_mt = sorted(most_tags.items(), key=itemgetter(1), reverse=True)
top_tags = {}                                                               #dict of top10 artists by tags
for id, c in sorted_mt[:10]: 
    top_tags[id] = c
    print "   ", id2name[id], "("+str(id)+"):", "num tags =", c
    print "      first month in top10 ="
    print "      months in top10 ="
print
print "top 10 artists dictionary: "
for k in top_tags:          #top 10 artists
    print k, id2name[k]     #top 10 artists  
print
print "top 10 for each year & month: "
for k in top10.items():
    print k

######################################################
