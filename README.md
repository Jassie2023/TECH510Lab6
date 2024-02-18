# Lab 6 - AI CV feedback

Jassie

This practice provides professional feedback on resumes by leveraging the power of machine learning and language models. Designed to assist job seekers in refining their resumes, the application evaluates various aspects of a resume and offers detailed, constructive feedback tailored to the candidate's target role.

## Getting Started

1. `python -m venv venv`
2. `source venv/bin/activate`
3. `pip install -r requirements.txt`
4. `cp .env.sample .env`
4. Change the `.env` file to match your environment
5. `streamlit run app.py`

## Components
app.py: The main Streamlit application script.
requirements.txt: A file listing all the necessary Python packages for running the application.
Integration with OpenAI's language models for generating feedback.
Use of llama_index and dotenv for indexing documents and managing environment variables, respectively.

## Lessons Learned
Streamlit for Web Applications: How to use Streamlit to create interactive, web-based applications.
Environment Management: The importance of using requirements.txt for consistently managing Python dependencies.
Language Models in Practice: Utilizing language models like OpenAI's GPT for real-world applications such as resume feedback.

## Questions
How can the feedback mechanism be further customized to cater to different industries or roles?
