import os
import pandas as pd
import ollama
from langchain.schema import Document
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from flask import Flask, render_template, request, jsonify, session


# Initialize Flask application
app = Flask(__name__)

# Load the course data from the CSV file
course_data_path = 'data/cleaned_merged_data.csv'
course_data = pd.read_csv(course_data_path)


def format_course_info(metadata):
    """
    Format course information for better readability.

    Args:
        metadata (dict): Metadata from the retrieved document.

    Returns:
        str: Formatted course information.
    """
    return (
        f"Course Code: {metadata.get('course_code', 'N/A')}\n"
        f"Title: {metadata.get('title', 'N/A')}\n"
        f"Credits: {metadata.get('credits', 'N/A')}\n"
        f"Department: {metadata.get('dept_code', 'N/A')}\n"
        f"Pre-requisites: {metadata.get('pre_reqs', 'N/A')}\n"
        f"Core Area: {metadata.get('core_area', 'N/A')}\n"
        f"Inquiry Area: {metadata.get('inquiry_area', 'N/A')}\n"
        f"Recommendation: {metadata.get('recommendation', 'N/A')}\n"
    )


def load_documents():
    """
    Load course documents into a vector database for retrieval.

    Returns:
        Chroma: A Chroma vector database containing the course documents.
    """
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=7500, chunk_overlap=100)

    # Create a list to hold Document objects
    documents = []
    for index, row in course_data.iterrows():
        # Combine all non-null values in a row into a single string and create a Document
        document = Document(
            page_content=" ".join([str(val) for val in row.values if pd.notnull(val)]),
            metadata={
                "index": index,
                "course_code": row.get('course_code', 'N/A'),
                "title": row.get('title', 'N/A'),
                "credits": row.get('credits', 'N/A'),
                "dept_code": row.get('dept_code', 'N/A'),
                "pre_reqs": row.get('pre_reqs', 'N/A'),
                "core_area": row.get('core_area', 'N/A'),
                "inquiry_area": row.get('inquiry_area', 'N/A'),
                "recommendation": row.get('recommendation', 'N/A')
            }
        )
        documents.append(document)

    # Split documents into chunks
    chunks = text_splitter.split_documents(documents)

    # Initialize the embedding model
    embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    # Initialize the vector database
    vector_db = Chroma(collection_name="local-rag", embedding_function=embedding_model)

    # Add documents to the vector database in batches
    batch_size = 5000  # Adjust this to be below the limit
    for i in range(0, len(chunks), batch_size):
        batch = chunks[i:i + batch_size]
        vector_db.add_documents(batch)

    return vector_db


def clean_response(text):
    """
    Clean and format the response text.

    Args:
        text (str): The text to clean and format.

    Returns:
        str: The cleaned and formatted text.
    """
    lines = text.split('\n')
    unique_lines = list(dict.fromkeys(lines))  # Remove duplicates while preserving order
    formatted_lines = [line.strip() for line in unique_lines if line.strip()]  # Remove empty lines and strip spaces
    return '\n'.join(formatted_lines)


def handle_small_talk(user_input):
    """
    Handle small talk queries using the Ollama model.

    Args:
        user_input (str): The user's input query.

    Returns:
        str: The response from the Ollama model or an error message if the query could not be understood.
    """
    try:
        # Get previous conversation from session
        messages = session.get('messages', [])

        # Add the current user input to the conversation
        messages.append({'role': 'user', 'content': user_input})

        # Make a request to the Ollama model
        response_chunks = ollama.chat(
            model='llama3',
            messages=messages,
            stream=True,

        )

        reply = ""
        for chunk in response_chunks:
            if 'message' in chunk and 'content' in chunk['message']:
                reply += chunk['message']['content']

        # Add the bot's reply to the conversation
        messages.append({'role': 'bot', 'content': reply})

        # Update the session with the latest conversation
        session['messages'] = messages

        return reply if reply else "Sorry, I couldn't understand your query. Please try again."
    except Exception as e:
        print(f"Error: {e}")
        return "Sorry, I couldn't understand your query. Please try again."


def handle_course_queries(user_input):
    """
    Handle course-related queries using the vector database.

    Args:
        user_input (str): The user's input query.

    Returns:
        str: The response from the vector database or None if not a course-related query.
    """
    course_keywords = ["course", "credit", "department", "prerequisite", "core area", "inquiry area", "recommendation"]
    if any(keyword in user_input for keyword in course_keywords):
        try:
            retriever = vector_db.as_retriever()
            print(f"Querying for: {user_input}")  # Debugging: Print the query
            relevant_docs = retriever.get_relevant_documents(user_input)

            print(f"Retrieved documents: {relevant_docs}")  # Debugging: Print retrieved documents
            if relevant_docs:
                # Concatenate content from retrieved documents and clean it
                reply = "\n".join([format_course_info(doc.metadata) for doc in relevant_docs])
                response = clean_response(reply).strip()
                return response
            else:
                return "Sorry, no relevant course information found."
        except Exception as e:
            print(f"Error: {e}")
            return None
    return None


@app.route('/')
def home():
    """
    Render the home page.

    Returns:
        str: Rendered HTML template for the home page.
    """
    return render_template('index.html')


@app.route('/get_response', methods=['POST'])
def get_response():
    """
    Handle the chatbot response for a given user query.

    Returns:
        json: The response from the chatbot.
    """
    user_input = request.json.get('user_input', '').strip().lower()

    if not user_input:
        return jsonify({'response': 'Please enter a query.'})

    # Check for course-related queries
    response = handle_course_queries(user_input)

    # If no course-related query, handle small talk or use vector database
    if response is None:
        response = handle_small_talk(user_input)

    return jsonify({'response': response})


if __name__ == '__main__':
    # Load documents into the vector database
    vector_db = load_documents()
    app.run(debug=True)
