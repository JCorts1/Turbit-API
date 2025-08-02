Turbit API - Full-Stack Power Curve Analytics 🚀
Welcome to the Turbit API project! This is a complete full-stack application designed to ingest, process, and visualize wind turbine performance data. The project features a robust backend built with Python and FastAPI, a containerized MongoDB database managed by Docker, and a sleek, responsive frontend built with React and Vite.

✨ Features

Containerized Environment: Uses Docker Compose to spin up a reliable MongoDB database.

Dual Data Ingestion:

Loads sample data from the public JSONPlaceholder REST API.

Parses and loads real-world time series data from German-formatted CSV files.

High-Performance Backend: A modern, asynchronous API built with FastAPI serving all the data.

Advanced Analytics: Includes API endpoints that perform server-side calculations for statistics and power curve data using MongoDB's Aggregation Pipeline.

Interactive Frontend: A beautiful, single-page React application for visualizing the power curve, complete with date-range filtering and performance statistics.

⚙️ Tech Stack

Backend: Python, FastAPI, Motor (async MongoDB driver), Pymongo

Database: MongoDB

Frontend: React, Vite, Recharts

Environment: Docker, Docker Compose

🏁 Getting Started

To get this project up and running on your local machine, please follow these steps.

Prerequisites:

Docker & Docker Compose

Python 3.8+ & pip3

Node.js & npm

This project is divided into a backend (FastAPI) and a frontend (React). They need to be run separately in two different terminal windows.

1. Running the Backend API 🐍

The backend is managed by a single script that automates the entire process. From the project's root directory, run:

./start.sh

This script will perform the following steps automatically:

Start the MongoDB database and Mongo Express UI using Docker Compose.

Install all the necessary Python dependencies from requirements.txt.

Run both data loader scripts to populate the database.

Launch the FastAPI server on http://localhost:8000.

The server will continue running in this terminal window.

2. Running the Frontend Application ⚛️

In a new, separate terminal window, navigate to the frontend directory and run the following commands:

# Navigate into the frontend folder
cd frontend

# Install all frontend dependencies
npm install

# Start the React development server
npm run dev

The React application will now be running and accessible in your web browser, typically at http://localhost:5173.

📁 Project Structure

The project is organized into a monorepo structure, with the backend and frontend code clearly separated.

turbit-data-api/
├── app/                  # All the Python/FastAPI backend code
│   ├── __init__.py
│   ├── main.py           # Main FastAPI app, startup, and old routes
│   ├── database.py       # MongoDB connection logic
│   ├── models.py         # Pydantic models for JSONPlaceholder data
│   ├── data_loader.py    # Script to load JSONPlaceholder data
│   ├── turbine_models.py # Pydantic models for turbine data
│   ├── turbine_loader.py # Script to load turbine CSV data
│   └── turbine_routes.py # All /turbines API endpoints
├── data/                 # Downloaded CSV files are stored here
├── frontend/             # The React + Vite frontend application
│   ├── src/
│   │   ├── App.css
│   │   ├── App.jsx
│   │   └── ...
│   └── ...
├── .env                  # Environment variables (credentials)
├── .gitignore            # Files and folders ignored by Git
├── docker-compose.yml    # Docker configuration for services
├── requirements.txt      # Python dependencies
└── start.sh              # The main startup script

🔗 Key API Endpoints

Once the backend is running, you can explore the API documentation and endpoints:

Interactive Docs (Swagger): http://localhost:8000/docs

Database UI (Mongo Express): http://localhost:8081

Get Turbine Info: GET /turbines/

Get Turbine Power Curve: GET /turbines/{turbine_id}/power-curve

Get Turbine Statistics: GET /turbines/{turbine_id}/statistics
