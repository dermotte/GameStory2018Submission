"""
/home/mlux/Temp/gamestory18-data/train_set/timelines/11.json
"""
import json

# setting the paths ...
import math
import os

# data_path = "/home/mlux/Temp/gamestory18-data/train_set/"
data_path = "/home/mlux/tmp/gamestory/gamestory18-data/train_set/"

# know data ... without loss of generality (w.l.o.g.)
teams2players = {
    "FaZe Clan": ["GuardiaN", "NiKo", "karrigan", "olofmeister", "rain"],
    "Fnatic": ["Golden", "JW", "KRIMZ", "Lekr0", "flusha"]
}
teamid2team = {
    '24a7a69c-4c71-4534-853d-31b6d0be1399': "FaZe Clan",
    '2d651b3b-8db9-4bb5-b3e1-c801050fc424': "Fnatic"
}
player2stream = {
    "Golden": "2018-03-04_P6.mp4",
    "GuardiaN": "2018-03-04_P1.mp4",
    "JW": "2018-03-04_P8.mp4",
    "KRIMZ": "2018-03-04_P10.mp4",
    "Lekr0": "2018-03-04_P7.mp4",
    "NiKo": "2018-03-04_P3.mp4",
    "flusha": "2018-03-04_P9.mp4",
    "karrigan": "2018-03-04_P4.mp4",
    "olofmeister": "2018-03-04_P2.mp4",
    "rain": "2018-03-04_P5.mp4"
}
stream2start = {}
offset = {
    'P1': 33,
    'P2': 34,
    'P3': 33,
    'P4': 33,
    'P5': 34,
    'P6': 32,
    'P7': 33,
    'P8': 33,
    'P9': 33,
    'P10': 32,
    'P11': 45,
    'P12': 33,
}

startdata = """P3	2018-03-04_P3.mp4	8:05:04	2018-03-04 21:48:23+00:00
P10	2018-03-04_P10.mp4	8:05:04	2018-03-04 21:48:24+00:00
P1	2018-03-04_P1.mp4	8:05:06	2018-03-04 21:48:25+00:00
P6	2018-03-04_P6.mp4	8:05:06	2018-03-04 21:48:25+00:00
P7	2018-03-04_P7.mp4	8:05:04	2018-03-04 21:48:25+00:00
P8	2018-03-04_P8.mp4	8:05:04	2018-03-04 21:48:25+00:00
P9	2018-03-04_P9.mp4	8:05:04	2018-03-04 21:48:25+00:00
P12	2018-03-04_P12.mp4	8:05:04	2018-03-04 21:48:25+00:00
P2	2018-03-04_P2.mp4	8:05:06	2018-03-04 21:48:26+00:00
P4	2018-03-04_P4.mp4	8:05:06	2018-03-04 21:48:26+00:00
P5	2018-03-04_P5.mp4	8:05:06	2018-03-04 21:48:27+00:00
P11	2018-03-04_P11.mp4	6:56:14	2018-03-04 21:48:33+00:00""".split(sep="\n")
for s in startdata:
    s = s.split(sep="\t")
    t = s[2].split(sep=":")
    secs = int(t[0]) * 60 * 60 + int(t[1]) * 60 + int(t[2]) + offset[s[0]]
    stream2start[s[1]] = {'time': secs, 'utc': s[3]}

item2price = {
    "ak47": 2700,
    "awp": 4750,
    "cz75a": 500,
    "deagle": 700,
    "famas": 2250,
    "flashbang": 200,
    "galilar": 2000,
    "hegrenade": 300,
    "incgrenade": 600,
    "item_assaultsuit": 1000,
    "item_defuser": 400,
    "item_kevlar": 650,
    "m4a1": 3100,
    "m4a1_silencer": 3100,
    "mac10": 1050,
    "molotov": 400,
    "mp9": 1250,
    "p250": 250,
    "smokegrenade": 300,
    "ssg08": 1700,
    "ump45": 1200
}

actions = []

with open('template.svg', 'r') as content_file:
    svg_template = content_file.read()


### functions
def timestring2seconds(timestring):
    t = timestring.split(":")
    return int(t[0]) * 60 * 60 + int(t[1]) * 60 + int(t[2])


def seconds2timestring(seconds):
    h = int(math.floor(seconds / 3600))
    m = int(math.floor((seconds - h * 3600) / 60))
    s = int(seconds % 60)
    return '{:02d}'.format(h) + ":" + '{:02d}'.format(m) + ":" + '{:02d}'.format(s)


def utc2streamtime(stream, utctime):
    t = stream2start[stream]['time']
    u = stream2start[stream]['utc']
    tmp_utc = utctime.split('T')[1]
    tmp_utc = tmp_utc.split('.')[0]
    u = u.split(' ')[1]
    u = u.split('+')[0]
    return t + (timestring2seconds(tmp_utc) - timestring2seconds(u))
    # return t + (utc-utctime)


def utc2timestring(utctime):
    tmp_utc = utctime.split('T')[1]
    tmp_utc = tmp_utc.split('.')[0]
    return tmp_utc



def timedifference(t1, t2):
    """
    get the difference between two time strings with the HH:MM:SS format in seconds
    :param t1:
    :param t2:
    :return:
    """
    tt1 = timestring2seconds(t1)
    tt2 = timestring2seconds(t2)
    return abs(tt1 - tt2)


def player2team(playerId):
    for k in teams2players.keys():
        if playerId in teams2players[k]:
            return k


def ffmpegcut(video, timepoint, duration, outfile="out.mp4"):
    """
    creates a cut command for ffmpeg
    :param video: the input video (player, usw)
    :param timepoint: in seconds
    :param duration: in seconds
    :param outfile: the output video file.
    :return: a string to call ffmpeg
    """
    cmd = "ffmpeg -ss {} -i {} -ss {} -t {} -c copy {}".format(seconds2timestring(timepoint - 60), video,
                                                               seconds2timestring(60), seconds2timestring(duration),
                                                               outfile)
    return cmd


### main
currentRound = 0
tmp_streaks = {}
tmp_economy = {"FaZe Clan": 0, "Fnatic": 0}
rounds = []
streaks = []
items = []
economy = []
with open(data_path + 'timelines/11.json') as f:
    data = json.load(f)
    for d in data:
        # collect all possible actions
        if d["type"] not in actions:
            actions.append(d["type"])

        # switch state of the rounds and print streaks
        if currentRound != d["roundIdx"]:
            # print(str(currentRound) + str(tmp_streaks))
            streaks.append(tmp_streaks.copy())
            economy.append(tmp_economy.copy())
            tmp_streaks = {}
            tmp_economy = {"FaZe Clan": 0, "Fnatic": 0}
            currentRound = d["roundIdx"]

        # collect data on the kills
        if d["type"] == "kill":
            if not d["data"]["actor"]["playerId"] in tmp_streaks:
                tmp_streaks[d["data"]["actor"]["playerId"]] = [{'date': d["date"]}]
            else:
                tmp_streaks[d["data"]["actor"]["playerId"]].append({'date': d["date"]})
        # collect data on the round end
        if d["type"] == "round_end":
            rounds.append({'team': teamid2team[d["data"]["teamId"]], 'date': d["date"]})
        # collect data on the economy
        if d["type"] == "purchase":
            price = item2price[d["data"]["item"]]
            tmp_economy[player2team(d["data"]["actor"]["playerId"])] += price

score = {"FaZe Clan": 0, "Fnatic": 0}
for r in range(0, len(rounds)):
    score[rounds[r]['team']] += 1
    print("{}\t{}".format(score["FaZe Clan"], score["Fnatic"]))
print(rounds)
print(actions)
print(economy)

# analyze kill streaks ..
for i in range(0, len(streaks)):
    for player in streaks[i].keys():
        if len(streaks[i][player]) > 2:
            length = timedifference(
                utc2timestring(streaks[i][player][0]['date']),
                utc2timestring(streaks[i][player][-1]['date']))
            if length < len(streaks[i][player]) * 6:  # if the kill streak is within kills*6 seconds
                # print(i + 1, player, len(streaks[i][player]), length)
                # create cut list for kill streaks
                print(ffmpegcut(data_path + player2stream[player],
                      utc2streamtime(player2stream[player], streaks[i][player][0]['date']) -3,
                      length + 6, 'killstreak_round{:02d}_player_{}_kills_{}.mp4'.format(i+1, player, len(streaks[i][player]))))
                # for k in stream2start.keys():  # print all streams for a particular event
                #     print(ffmpegcut(data_path + k,
                #           utc2streamtime(k, streaks[i][player][0]['date']) - 15,
                #           length + 30, 'killstreak_round{:02d}_player_{}_kills_{}_{}.mp4'.format(i+1, player, len(streaks[i][player]), k.replace('.mp4', ''))))
# analyze round ends ...
vid = "2018-03-04_P11.mp4"  # P11 is the commentator
for i in range(0, len(rounds)-1):
    print(ffmpegcut(data_path + vid, utc2streamtime(vid, rounds[i]['date'])-5, 10,
                    'round_end_comments_round{:02d}.mp4'.format(i+1)))
print(ffmpegcut(data_path + vid, utc2streamtime(vid, rounds[-1]['date'])-10, 30,
                'round_end_comments_round{:02d}.mp4'.format(len(rounds))))

# analyze round ends ...
vid = "2018-03-04_P12.mp4"  # P12 is the map
for i in range(0, len(rounds)):
    print(ffmpegcut(data_path + vid, utc2streamtime(vid, rounds[i]['date'])-5, 10,
                    'round_end_map_round{:02d}.mp4'.format(i+1)))

vid = "2018-03-04_P10.mp4"
print(rounds[0]['date'], utc2streamtime(vid, rounds[0]['date']))
# print(ffmpegcut(vid, utc2streamtime(vid, rounds[0]['date']), 60))

## create ffmpeg cut list for kill streaks
# note: it's only 4 secs per card in the stats video

## create cards:
if not 1:
    score = {"FaZe Clan": 0, "Fnatic": 0}
    for r in range(0, len(rounds)):
        score[rounds[r]['team']] += 1
        round = str(r + 1)
        team_win = rounds[r]['team']
        team_a = "FaZe Clan"
        team_b = "Fnatic"
        eco_a = str(economy[r][team_a])
        eco_b = str(economy[r][team_b])
        curr_score = "{}-{}".format(score["FaZe Clan"], score["Fnatic"])
        streak_a = ""
        streak_b = ""

        # finding the kill streaks
        for i in range(0, len(streaks)):
            for player in streaks[i].keys():
                if len(streaks[i][player]) > 2:
                    if i == r:  # it's the current round
                        if player in teams2players[team_a]:
                            streak_a = "{} kills {}".format(player, len(streaks[i][player]))
                        else:
                            streak_b = "{} kills {}".format(player, len(streaks[i][player]))

        # re-reading the template file
        with open('template.svg', 'r') as content_file:
            svg_template = content_file.read()

        svg_template = svg_template.replace("{score}", curr_score)
        svg_template = svg_template.replace("{round}", round)
        svg_template = svg_template.replace("{team_win}", team_win)
        svg_template = svg_template.replace("{team_a}", team_a)
        svg_template = svg_template.replace("{team_b}", team_b)
        svg_template = svg_template.replace("{eco_a}", eco_a)
        svg_template = svg_template.replace("{eco_b}", eco_b)
        svg_template = svg_template.replace("{streak_a}", streak_a)
        svg_template = svg_template.replace("{streak_b}", streak_b)
        print("Round {}, {} wins, {}".format(str(r + 1), rounds[r]['team'],
                                             "{}-{}".format(score["FaZe Clan"], score["Fnatic"])))
        with open("out/out-{:02d}.svg".format(r + 1), 'w') as outsvg:
            outsvg.write(svg_template)

        # converting to png
        os.system(
            "flatpak run org.inkscape.Inkscape out/out-{:02d}.svg --export-png out/out-{:02d}.png -b white".format(
                r + 1, r + 1))

    os.system("rm out/out*.svg")
    os.system("convert +append ./out/out-{01..18}.png ./out/result/all1.png")
    os.system("convert +append ./out/out-{19..36}.png ./out/result/all2.png")
