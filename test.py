from telethon import TelegramClient
from telethon.tl.types import Channel, User
import time

api_id = 126271
api_hash = 'a604474f883f0371b331c13c28a26a8c'
phone = '80508293924'

client = TelegramClient('statistics', api_id, api_hash)
client.connect()

# If you already have a previous 'session_name.session' file, skip this.
if not client.is_user_authorized():
    client.send_code_request(phone)
    client.sign_in(phone, input('Enter the code: '))

dialogs = client.get_dialogs(limit=None)

friends = dict()
channels = dict()

print("Dialogs " + str(len(dialogs)))
i = 0
for dialog in dialogs:
    print("Dialog " + str(i) + " of " + str(len(dialogs)))
    start_time = time.time()
    messages = client.get_messages(dialog.input_entity, limit=None)
    print("--- get history function --- "+str(len(messages))+" --- %s seconds ---" % (time.time() - start_time))
    if isinstance(dialog.entity, Channel):
        key = str(dialog.entity.title)
        channels[key] = messages.total
    elif isinstance(dialog.entity, User):
        partner = client.get_entity(messages[0].to_id if messages[0].out else messages[0].from_id)
        if partner.first_name is not None and partner.last_name is not None:
            key = str(partner.first_name) + " " + str(partner.last_name)
        elif partner.first_name is not None:
            key = str(partner.first_name)
        elif partner.last_name is not None:
            key = str(partner.last_name)
        friends[key] = messages.total
    i += 1

print("Friends:")
print(sorted(friends.items(), key=lambda x: -x[1]))
print("Channels:")
print(sorted(channels.items(), key=lambda x: -x[1]))