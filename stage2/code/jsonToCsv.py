import pandas as pd
import matplotlib.pyplot as plt

keys = ["Title", "Developer", "Publisher", "Platform", "Genre", "ReleaseDate", "Rating"]

dfH = pd.read_json("HltbScrappy/outHltb.json")
dfG = pd.read_json("GameSpotScrappy/outGamespot.json")
dfH.to_csv("../Data/howLongToBeat.csv", index=False, columns=keys)
dfG.to_csv("../Data/gamespot.csv", index=False, columns=keys)
