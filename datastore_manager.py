from google.cloud import datastore
from datetime import datetime

# Initialize Datastore client
client = datastore.Client()

# Function to store profile question
def store_profile_question(question_id, question, answer):
    key = client.key('ProfileQuestion', question_id)
    question_entity = datastore.Entity(key=key)
    question_entity.update({
        'question': question,
        'answer': answer
    })
    client.put(question_entity)
    return question_entity.key

# Function to submit answer to a specific profile question
def submit_answer(question_id, answer):
    key = client.key('ProfileQuestion', question_id)
    question_entity = client.get(key)
    if question_entity:
        # Extract necessary details from the question entity
        question_text = question_entity.get('question')

        # Update answer field in the question entity
        question_entity['answer'] = answer
        client.put(question_entity)

        # Store chat history entry
        store_chat_history(question_id, question_text, answer)

        return True
    return False

# Function to store chat history
def store_chat_history(question_id, question_text, answer):
    key = client.key('ChatHistory')
    chat_entity = datastore.Entity(key=key)
    chat_entity.update({
        'question_id': question_id,
        'question_text': question_text,
        'answer': answer,
        'timestamp': datetime.utcnow()  # Optionally, you can add a timestamp
    })
    client.put(chat_entity)
    return chat_entity.key

# Function to retrieve all chat history
def get_all_chat_history():
    query = client.query(kind='ChatHistory')
    return list(query.fetch())  

# Function to retrieve all profile questions
def get_all_profile_questions():
    query = client.query(kind='ProfileQuestion')
    return list(query.fetch())

# Function to retrieve a specific profile question by ID
def get_profile_question(question_id):
    key = client.key('ProfileQuestion', question_id)
    question_entity = client.get(key)
    return question_entity
