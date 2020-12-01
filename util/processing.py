from util import train
from models.models import *
import threading
from sqlalchemy.orm import scoped_session, sessionmaker

processing_queue = []
session_factory = None

def init_sessionfactory(app):
    global session_factory
    session_factory = sessionmaker(app)

def in_queue(file_id):
    global processing_queue
    for existing in processing_queue:
        if existing.id == file_id:
            return True
    return False

def add_to_queue(data):
    global processing_queue
    processing_queue.append(data)
    process_check()

def remove_from_queue(file_id):
    global processing_queue
    for i in range(len(processing_queue)):
        if processing_queue[i].id == file_id:
            del processing.processing_queue[i]
            break
    process_check()

def process_check():
    print("Processing check...")
    global processing_thread
    global processing_queue
    if processing_queue and not processing_thread.is_alive():
        processing_thread = threading.Thread(target=background_process)
        processing_thread.start()

def background_process():
    global db
    global processing_queue
    global session_factory
    Session = scoped_session(session_factory)
    
    while processing_queue:
        print("QUEUE SIZE  -  " + str(len(processing_queue)))
        processing_data = processing_queue.pop(0)
        conversation = processing_data["conversation"]
        model_name = processing_data["name"]
        print("Traning bot " + conversation.name + " ...", flush=True)
        bot = train.train_bot(conversation.data.decode("utf-8"), None)
        bot_data = bot.save()
        print("Finished training bot " + conversation.name, flush=True)
        trained_model = TrainedModel(
            name=conversation.name,
            data=bytes(bot_data, 'utf-8'),
            data_size=len(bot_data),
            file_id = conversation.id)
        Session.add(trained_model)
        Session.commit()
    Session.remove()

processing_thread = threading.Thread(target=background_process)