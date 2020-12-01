import json
import sys
import string
from nltk.tokenize import RegexpTokenizer
from util.simple_bot import SimpleBot

file_name = None
learn_participant = None
input_participant = None
first_participant = None
bot = None

def process_sentence(s):
    tokenizer = RegexpTokenizer(r'\w+')
    return tokenizer.tokenize(s.lower())

def preprocess(data):
    global first_participant
    global learn_participant
    global input_participant
    
    participants = []
    for entry in data["participants"]:
        participants.append(entry["name"])
    print("Participants:")
    print(participants)
    messages = {}
    for p in participants:
        messages[p] = []
    if learn_participant == None:
        learn_participant = participants[0]
        input_participant = participants[1]
    else:
        input_participant = participants[0] if learn_participant == participants[1] else participants[1]

    combined_string = ""
    last_participant = None
    for m in data["messages"]:
        if "type" not in m.keys() or "content" not in m.keys():
            continue
        message_type = m["type"]
        if message_type != "Generic":
            continue
        
        participant = m["sender_name"]
        content = m["content"]
        if last_participant == None:
            first_participant = participant
            last_participant = participant
            combined_string = content
            continue
        if last_participant == participant:
            combined_string = combined_string + "\n" + content
        else:
            messages[last_participant].append(combined_string)
            last_participant = participant
            combined_string = content
    
    if first_participant != learn_participant:
            for p in participants:
                if p != learn_participant:
                    del messages[p][0]
    messages_len = len(messages[learn_participant])
    for p in participants:
        if p != learn_participant:
            messages[p] = messages[p][:messages_len]

    for p in participants:
        for i in range(len(messages[p])):
            messages[p][i] = process_sentence(messages[p][i])

    return messages

def bot_interface(bot):
    global learn_participant
    global input_participant
    print("Talk with the bot:")
    print("You: ", end="")
    text_input = input()
    while text_input != "exit":
        token_input = process_sentence(text_input)
        print(learn_participant + ": " + bot.predict(token_input, input_participant, learn_participant))
        print("You: ", end="")
        text_input = input()


def train_bot(string_data, participant):
    global learn_participant
    global bot
    learn_participant = participant

    print(f"Parsing string")
    try:
        data = json.loads(string_data)
    except IOError:
        print(f"Error: Cannot parse string")
        return None
    
    messages = preprocess(data)

    # train bot
    bot = SimpleBot(messages)
    bot.train()
    
    return bot

def load_bot(file, participant):
    global file_name
    global learn_participant
    global bot
    learn_participant = participant
    file_name = file.name

    bot = SimpleBot({})
    bot.load(file)
    
    return bot

def main():
    global file_name
    global learn_participant
    global bot

    file_name = "messages.json"
    if len(sys.argv) > 1:
        file_name = sys.argv[1]
    if len(sys.argv) > 2:
        learn_participant = sys.argv[2]
    
    file = open(file_name, "r", encoding="utf-8")
    bot = train_bot(file, "Jure Bevc")
    bot.save("bot.mdl")
    # test bot
    bot_interface(bot)

def main_load():
    global file_name
    global learn_participant
    global bot

    file_name = "bot.mdl"
    file = open(file_name, "r", encoding="utf-8")
    
    bot = load_bot(file, "Jure Bevc")
    # test bot
    bot_interface(bot)

if __name__ == "__main__":
    main_load()