Quiz Application API
This is a FastAPI-based REST API for managing quiz questions and multiple-choice answers. It uses PostgreSQL as the database and supports basic CRUD operations (Create, Read, Update, Delete).

Features
Create, read, update, and delete quiz questions


Manage multiple-choice answers for each question


Backend uses FastAPI and SQLAlchemy
Database: PostgreSQL


Installation
Prerequisites
Python 3.8+
PostgreSQL database



API Endpoints
GET /questions/{question_id} – Get a specific question by ID.
GET /choices/{question_id} – Get all choices for a question.
POST /questions/ – Create a new question with choices.
PUT /questions/{question_id} – Update an existing question and choices.
DELETE /questions/{question_id} – Delete a question and its choices.


Database Models
Questions: Stores the quiz question text.
Choices: Stores the answer options and whether they’re correct, linked to a question.


