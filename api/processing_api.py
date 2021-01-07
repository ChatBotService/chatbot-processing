import flask
from flask_restful import Resource
from flask import request, jsonify, redirect, Response
from models.models import *
from util import processing
import requests
from flask import current_app as app

class ProcessingAPI(Resource):
    def get(self):
        stop_processing = False
        try:
            resp = requests.get(app.config["REMOTE_CONFIG_PATH"] + "/stop_processing")
            if resp.ok:
                stop_processing = resp.content.decode('utf-8') == "true"
                print(resp.content.decode('utf-8'), flush=True)

        except Exception as e:
            pass

        print("stop processing:", flush=True)
        print(stop_processing, flush=True)

        #Return current processing queue status
        conversation_schema = ConversationFileSchema(many=True)
        return jsonify(conversation_schema.dump(processing.processing_queue))
        
    def post(self):
        stop_processing = False
        try:
            resp = requests.get(app.config["REMOTE_CONFIG_PATH"] + "/stop_processing")
            if resp.ok:
                stop_processing = resp.content.decode('utf-8') == "true"
        except:
            print("Remote config not available.", flush=True)

        if stop_processing:
            return Response("Bad Request:\nProcessing is currently turned off.",status=503);

        is_prompt = file_id = request.args.get("prompt")
        if is_prompt:
            # Prompt bot
            model_id = request.args.get("id")
            text = request.args.get("text")
            participant1 = request.args.get("prompt_participant")
            participant2 = request.args.get("reply_participant")
            print(model_id, flush=True)
            print(text, flush=True)
            print(participant1, flush=True)
            print(participant2, flush=True)
            if model_id:
                model = TrainedModel.query.filter_by(id=model_id).first()
                if model:
                    prompt_response = processing.prompt_bot(model, text, participant1, participant2)
                    if prompt_response:
                        return Response(prompt_response,status=200)
                    else:
                        return Response("Bad prompt response",status=400)
                else:
                    return Response("Bad Request:\nCould not find or load existing model.",status=400)
            else:
                return Response("Bad Request:\nBad model id.",status=400)
        else:
            # Add process to queue
            file_id = request.args.get("id")
            name = request.args.get("name")
            print(file_id, flush=True)
            print(name, flush=True)
            if file_id:
                conversations = ConversationFile.query.filter_by(id=file_id).first()
                if conversations:
                    if processing.in_queue(int(file_id)):
                            return Response(f"File with id {file_id} already in queue.",status=200)  
                    processing.add_to_queue({"conversation":conversations, "name" : name})
                    return Response(f"File with id {file_id} was added to queue.",status=200)
                else:
                    return Response("Bad Request:\nCould not find or load existing conversation file.",status=400)
            else:
                return Response("Bad Request:\nBad file id.",status=400)
    
    def delete(self):
        # Remove a process from queue
        file_id = request.args.get("id")
        if file_id:
            processing.remove_from_queue(int(file_id))
        return Response(status=200)