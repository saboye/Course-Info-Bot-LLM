
<div align="center">
  <h1>Course- Info Bot LLM</h1>
</div>

<p align="center">
    <img src="https://img.shields.io/github/contributors/saboye/Course-Info-Bot-LLM?color=blue&logo=github&style=for-the-badge" alt="GitHub contributors" />
    <img src="https://img.shields.io/github/forks/saboye/Course-Info-Bot-LLM?logo=github&style=for-the-badge" alt="GitHub forks" />
    <img src="https://img.shields.io/github/issues-raw/saboye/Course-Info-Bot-LLM?style=for-the-badge" alt="GitHub issues" />
    <img src="https://img.shields.io/github/license/saboye/Course-Info-Bot-LLM?style=for-the-badge" alt="GitHub license" />
    <img src="https://img.shields.io/github/last-commit/saboye/Course-Info-Bot-LLM?style=for-the-badge" alt="GitHub last commit" />
    <img src="https://img.shields.io/badge/flask-2.1.2-blue?style=for-the-badge&logo=flask" alt="Flask" />
    <img src="https://img.shields.io/badge/scikit--learn-0.24.2-blue?style=for-the-badge&logo=scikit-learn" alt="scikit-learn" />
    <img src="https://img.shields.io/badge/pandas-1.3.5-blue?style=for-the-badge&logo=pandas" alt="Pandas" />
    <img src="https://img.shields.io/badge/numpy-1.20.3-blue?style=for-the-badge&logo=numpy" alt="NumPy" />
    <img src="https://img.shields.io/badge/ollama-1.0.0-blue?style=for-the-badge&logo=ollama" alt="Ollama" />
    <img src="https://img.shields.io/badge/LLM-1.0.0-blue?style=for-the-badge&logo=LLM" alt="LLM" />
</p>

## Project Overview

The Course-Info-Bot-LLM project aims to develop an intelligent chatbot powered by a Large Language Model (LLM) to interface with a Student Information System (SIS). The chatbot retrieves detailed course information and provides personalized advice to students, enhancing their academic planning and course selection experience.

## Business Problem

Educational institutions often struggle with providing timely and accurate course information to students. Traditional methods of retrieving information from SIS can be time-consuming and inefficient. This project seeks to develop an AI-driven chatbot that offers quick and precise course information and recommendations.

## Objectives

- Develop a chatbot that integrates with the SIS to retrieve and provide course information.
- Enhance the student experience by offering personalized course recommendations.
- Improve decision-making in academic planning through AI-driven insights.

## Data Collection

### Data Source

The primary data source is the 'University Student Enrollment Data' dataset available on Kaggle. This dataset includes comprehensive details on university student enrollment, course registrations, and other related academic activities.

[University Student Enrollment Data on Kaggle](https://www.kaggle.com/datasets/thedevastator/university-student-enrollment-data)

### Features Included

- **Course ID**: Unique identifier for each course.
- **Course Name**: Name of the course.
- **Credit Hours**: Number of credit hours assigned to the course.
- **Department**: Department offering the course.
- **Prerequisites**: Prerequisites required to enroll in the course.
- **Core Area**: Core area classification of the course.
- **Inquiry Area**: Inquiry area classification of the course.
- **Recommendation**: Course recommendation status.


## Model 

### Model Overview

The chatbot leverages Natural Language Processing (NLP) techniques and integrates with a Large Language Model (LLM) to interact with students and provide course information. The chatbot is designed to handle various types of queries, including course descriptions, prerequisites, and personalized course recommendations.

### Architecture of the Chatbot

![image](https://github.com/user-attachments/assets/758c01ca-49c2-4d5c-b965-f52c638606d9)


#### Data Layer

- **Course Data Storage**: Stores detailed course information, such as course IDs, names, credit hours, departments, prerequisites, core areas, inquiry areas, and recommendations.
- **Vector Database**: Uses Chroma for efficient retrieval of course information based on text embeddings.

#### Preprocessing Layer

- **Data Cleaning and Transformation**: Scripts to clean and preprocess the course data before loading it into the vector database.
- **Text Splitter**: A module (e.g., `RecursiveCharacterTextSplitter`) to split course descriptions and other text data into manageable chunks for embedding.

#### Embedding Layer

- **Embedding Model**: A pre-trained model (e.g., `HuggingFaceEmbeddings`) that converts course text data into embeddings (numerical representations).
- **Embedding Storage**: Storage of these embeddings in the vector database for fast retrieval.

#### API Layer

- **Flask API**: A RESTful API built with Flask to handle incoming requests from users. It processes user queries, retrieves relevant data, and returns responses.
- **Session Management**: Flask sessions to manage ongoing conversations and context.

#### Retrieval Layer

- **Retriever**: A component to query the vector database and retrieve the most relevant course information based on user input.
- **Document Formatter**: A module to format the retrieved documents and their metadata into a user-friendly response.

#### Conversational Layer

- **Ollama Model**: A conversational AI model (e.g., `llama3`) that handles small talk and enhances the user interaction experience. It can generate human-like responses for non-course-related queries.
- **Small Talk Handler**: A module to handle predefined small talk scenarios and provide appropriate responses.

#### Integration Layer

- **Query Handler**: A core module that integrates the retriever and conversational model. It processes the user input, decides whether the query is course-related or general small talk, and generates the appropriate response.
- **Response Cleaner**: A component to clean and format the final response before sending it back to the user.

## Web Application

### Model Deployment

- **Web Interface**: Design an easy-to-use web interface for users to input data and receive predictions. The interface includes a chat window where users can type their queries and receive responses in real-time.
- **Backend Integration**: Integrate the chatbot with the SIS backend to securely access and retrieve data.
- **Deployment Platform**: Deploy the chatbot on a cloud platform (e.g., AWS, Azure, Google Cloud) to ensure scalability and accessibility.


## Usage

### Prerequisites

- Python 3.7 or higher
- Virtual environment (optional but recommended)

### Installation

1. **Clone the repository**:

    ```bash
    git clone https://github.com/saboye/Course-Info-Bot-LLM.git
    cd Course-Info-Bot-LLM
    ```

2. **Create a virtual environment** (optional but recommended):

    ```bash
    python -m venv venv
    ```

3. **Activate the virtual environment**:

    - On Windows:

        ```bash
        .\venv\Scripts\activate
        ```

    - On macOS/Linux:

        ```bash
        source venv/bin/activate
        ```

4. **Install the dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

5. **Run the Flask application**:

    ```bash
    python app.py
    ```

6. **Access the application**:

    Open your web browser and navigate to `http://127.0.0.1:5000`.


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

