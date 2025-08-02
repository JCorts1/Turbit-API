<h1 align="center">Turbit API - Full-Stack Power Curve Analytics 🚀</h1>

<p align="center">
Welcome to the Turbit API project! This is a complete full-stack application designed to ingest, process, and visualize wind turbine performance data. The project features a robust backend built with Python and FastAPI, a containerized MongoDB database managed by Docker, and a sleek, responsive frontend built with React and Vite.
</p>

✨ Features

<ul>
<li><strong>Containerized Environment:</strong> Uses Docker Compose to spin up a reliable MongoDB database.</li>
<li><strong>Dual Data Ingestion:</strong>
<ul>
<li>Loads sample data from the public <code>JSONPlaceholder</code> REST API.</li>
<li>Parses and loads real-world time series data from German-formatted CSV files.</li>
</ul>
</li>
<li><strong>High-Performance Backend:</strong> A modern, asynchronous API built with FastAPI serving all the data.</li>
<li><strong>Advanced Analytics:</strong> Includes API endpoints that perform server-side calculations for statistics and power curve data using MongoDB's Aggregation Pipeline.</li>
<li><strong>Interactive Frontend:</strong> A beautiful, single-page React application for visualizing the power curve, complete with date-range filtering and performance statistics.</li>
</ul>

⚙️ Tech Stack

<ul>
<li><strong>Backend:</strong> Python, FastAPI, Motor (async MongoDB driver), Pymongo</li>
<li><strong>Database:</strong> MongoDB</li>
<li><strong>Frontend:</strong> React, Vite, Recharts</li>
<li><strong>Environment:</strong> Docker, Docker Compose</li>
</ul>

🏁 Getting Started

To get this project up and running on your local machine, please follow these steps.

Prerequisites:

<ul>
<li>Docker & Docker Compose</li>
<li>Python 3.8+ & <code>pip3</code></li>
<li>Node.js & <code>npm</code></li>
</ul>

This project is divided into a backend (FastAPI) and a frontend (React). They need to be run separately in two different terminal windows.

1. Running the Backend API 🐍

The backend is managed by a single script that automates the entire process. From the project's root directory, run:

<pre><code>./start.sh
</code></pre>

This script will perform the following steps automatically:

<ol>
<li>Start the MongoDB database and Mongo Express UI using Docker Compose.</li>
<li>Install all the necessary Python dependencies from <code>requirements.txt</code>.</li>
<li>Run both data loader scripts to populate the database.</li>
<li>Launch the FastAPI server on <code>http://localhost:8000</code>.</li>
</ol>

The server will continue running in this terminal window.

2. Running the Frontend Application ⚛️

In a new, separate terminal window, navigate to the frontend directory and run the following commands:

<pre><code># Navigate into the frontend folder
cd frontend

Install all frontend dependencies
npm install

Start the React development server
npm run dev
</code></pre>

The React application will now be running and accessible in your web browser, typically at http://localhost:5173.

📁 Project Structure

The project is organized into a monorepo structure, with the backend and frontend code clearly separated.

<ul>
<li><strong><code>turbit-data-api/</code></strong>
<ul>
<li><strong><code>app/</code></strong>: All the Python/FastAPI backend code.
<ul>
<li><code>main.py</code>: Main FastAPI app, startup, and old routes.</li>
<li><code>database.py</code>: MongoDB connection logic.</li>
<li><code>models.py</code>: Pydantic models for JSONPlaceholder data.</li>
<li><code>data_loader.py</code>: Script to load JSONPlaceholder data.</li>
<li><code>turbine_models.py</code>: Pydantic models for turbine data.</li>
<li><code>turbine_loader.py</code>: Script to load turbine CSV data.</li>
<li><code>turbine_routes.py</code>: All <code>/turbines</code> API endpoints.</li>
</ul>
</li>
<li><strong><code>data/</code></strong>: Downloaded CSV files are stored here.</li>
<li><strong><code>frontend/</code></strong>: The React + Vite frontend application.</li>
<li><code>.env</code>: Environment variables (credentials).</li>
<li><code>.gitignore</code>: Files and folders ignored by Git.</li>
<li><code>docker-compose.yml</code>: Docker configuration for services.</li>
<li><code>requirements.txt</code>: Python dependencies.</li>
<li><code>start.sh</code>: The main startup script.</li>
</ul>
</li>
</ul>

🔗 Key API Endpoints

Once the backend is running, you can explore the API documentation and endpoints:

<ul>
<li><strong>Interactive Docs (Swagger):</strong> <a href="http://localhost:8000/docs">http://localhost:8000/docs</a></li>
<li><strong>Database UI (Mongo Express):</strong> <a href="http://localhost:8081">http://localhost:8081</a></li>
<li><strong>Get Turbine Info:</strong> <code>GET /turbines/</code></li>
<li><strong>Get Turbine Power Curve:</strong> <code>GET /turbines/{turbine_id}/power-curve</code></li>
<li><strong>Get Turbine Statistics:</strong> <code>GET /turbines/{turbine_id}/statistics</code></li>
</ul>
