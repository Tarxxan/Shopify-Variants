import json
from urllib.parse import urlparse
import re
import requests
import discord
from dotenv import load_dotenv
import os

client = discord.Client()
load_dotenv('.env')

output_vars = []
output_links = []
output_size = []
variants = ""


def url_input(discordLink):
    UserInput = discordLink
    url = UserInput + ".json"
    if re.search("^https", url):
        r = requests.get(url)
        global variants
        variants = json.loads(r.text)
        return variants



    else:
        url = "https://" + url
        r = requests.get(url)
        variants = json.loads(r.text)
        return variants


def var_and_size(variants, url_json):
    size_count = 0
    global product_title
    product_title = variants["product"]["title"]
    for x in variants["product"]["variants"]:
        output_vars.append(variants["product"]["variants"][size_count]["id"])
        output_size.append(variants["product"]["variants"][size_count]["title"])
        output_links.append(atc_link(variants["product"]["variants"][size_count]["id"], url_json))
        size_count += 1


def atc_link(v, url):
    parsed = urlparse(url)
    return parsed[0] + "://" + parsed[1] + "/cart/" + str(v) + ":1"


def main(i):
    try:
        return var_and_size(url_input(i), i)
    except KeyError:
        return "No variants can be pulled"


@client.event
async def on_ready():
    print("lets GOOOO")


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith('$atc'):
        user_url = message.content.split(" ")
        i = user_url[1]
        main(i)
        embeded = discord.Embed(title=product_title, description="ATC link and Variants", color=0x00ff00)
        embeded.set_footer(text="Tarxxan#0666")
       # embeded.set_thumbnail(url="")
        for x in range(len(output_vars)):
            embeded.add_field(name="Size : " + output_size[x],
                              value="Variants : " + str(output_vars[x]) + "\n" + (output_links[x]),
                              inline=True)
        await message.channel.send(embed=embeded)
        output_links.clear()
        output_size.clear()
        output_vars.clear()
    if message.content.startswith('whos the captain'):
        await message.channel.send("Im the captain Now")

client.run(os.getenv('token'))

