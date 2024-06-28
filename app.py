# app.py

from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from datastore_manager import store_profile_question, submit_answer, store_chat_history

app = Flask(__name__)
api = Api(app)

# Define the resource class for posting multiple profile questions
class PostProfileQuestions(Resource):
    def post(self):
        data = request.get_json()

        if not isinstance(data, list):
            return {"status": False, "message": "Invalid JSON format, expected a list of questions", "response": {}}, 400

        response_data = []
        for question_data in data:
            question_id = question_data.get('id')
            question_text = question_data.get('question')

            if not question_id or not question_text:
                return {"status": False, "message": "Missing required fields in one of the questions", "response": {}}, 400

            # Store question in Datastore with blank answer
            key = store_profile_question(question_id, question_text, "")

            response_data.append({"question_id": key.id_or_name})

        return {
            "status": True,
            "message": "Questions posted successfully",
            "response": response_data
        }

# Define the resource class for submitting answers to profile questions
class SubmitAnswers(Resource):
    def post(self):
        data = request.get_json()

        if not isinstance(data, list):
            return {"status": False, "message": "Invalid JSON format, expected a list of answers", "response": {}}, 400

        response_data = []
        for answer_data in data:
            question_id = answer_data.get('question_id')
            answer_text = answer_data.get('answer')

            if not question_id or not answer_text:
                return {"status": False, "message": "Missing required fields in one of the answers", "response": {}}, 400

            # Submit answer to the question in Datastore
            submitted = submit_answer(question_id, answer_text)

            if submitted:
                response_data.append({"question_id": question_id})
            else:
                return {"status": False, "message": f"Question with id {question_id} not found", "response": {}}, 404

        return {
            "status": True,
            "message": "Answers submitted successfully",
            "response": response_data
        }
    
# Define the resource class for storing chat history
class StoreChatHistory(Resource):
    def post(self):
        data = request.get_json()

        if not isinstance(data, list):
            return {"status": False, "message": "Invalid JSON format, expected a list of chat entries", "response": {}}, 400

        response_data = []
        for entry_data in data:
            question_id = entry_data.get('question_id')
            question_text = entry_data.get('question_text')
            answer = entry_data.get('answer')

            if not question_id or not question_text or not answer:
                return {"status": False, "message": "Missing required fields in one of the chat entries", "response": {}}, 400

            # Store chat history entry in Datastore
            key = store_chat_history(question_id, question_text, answer)

            response_data.append({"chat_entry_id": key.id_or_name})

        return {
            "status": True,
            "message": "Chat history stored successfully",
            "response": response_data
        }

# Adding resources to the API
api.add_resource(PostProfileQuestions, '/profile/questions')
api.add_resource(SubmitAnswers, '/profile/answers')
api.add_resource(StoreChatHistory, '/profile/chat-history')

if __name__ == '__main__':
    app.run(debug=True)
