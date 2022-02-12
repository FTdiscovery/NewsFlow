"""
Creates json for stock
"""

import os
import openai
import json

openai.organization = "org-GhuqPhpoi029dThqqUHRulbB"
openai.api_key = input("Input your API key:") #use ur own key
openai.Engine.list()

# Opening JSON file
f = open('data/wsj/2022-02-11.json')

# returns JSON object as
# a dictionary
data = json.load(f)

predictions = []

for elem in data:
    try:
        blurb = "What are the names and stock tickers of the companies most associated with the news?\n\n"
        blurb += "\"Title: " + elem["title"] + " Summary:" + elem["summary"]+"\""

        openai.Engine.retrieve("text-davinci-001")
        response = openai.Completion.create(
          engine="text-davinci-001",
          prompt=blurb,
          max_tokens=64,
          temperature=0.3)

        # print("Stocks affected:", response["choices"][0]["text"])
        stocks_affected = response["choices"][0]["text"]
        blurb += "\n\n" + response["choices"][0]["text"]
        blurb += "\n\nHow will the prices of each of these companies change as a result of this news? Explain."
        response = openai.Completion.create(
            engine="text-davinci-001",
            prompt=blurb,
            max_tokens=128,
            temperature=0)

        # print("----")
        #
        # print(response["choices"][0]["text"])
        # print("-"*80)

        elem["Prediction"] = stocks_affected + response["choices"][0]["text"]
        predictions.append(elem)

    except:
        print("Article is invalid for prediction.")

with open('data/wsj-predictions/2022-02-11.json', "w") as f:
    json.dump(predictions, f)

