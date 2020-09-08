from pymongo import MongoClient
import random
import string
client = MongoClient()
db = client.DiscordServers
servers = db.servers

def generatePass():

    letters_and_digits = string.ascii_letters + string.digits
    result_str = ''.join((random.choice(letters_and_digits) for i in range(20)))

    return result_str

result = db.servers.find({})

for server in result:
    password = generatePass()
    server['password'] = password
    servers.replace_one({"id":server['id']},server)
