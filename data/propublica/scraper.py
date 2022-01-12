from congress import Congress
import pickle
import os

apikey=os.environ["propublica_key"]
congress = Congress(apikey=apikey)

data = []

for session in [112, 113, 114, 115, 116]:
    for chamber in ["House", "Senate"]:
        data.append(congress.votes.party(chamber, session))
        