# EVAREAP
================
### Instructions
1. Clone the repository

### Tools
1. Install [Node.js](https://nodejs.org/en/) If node is not insalled on your machine.
2. Install Python 3.11.0
3. Have your local server running (MAMP, WAMP, XAMPP, etc.)
4. Create a database called "fastapi" in your local server
5. Import the database file from the DB folder

### Running the Backend
1. Open the terminal and navigate to the backend folder using the following command: `cd backend`
2. Create a virtual environment using the following command: `python -m venv venv`
3. Activate the virtual environment using the following command: `venv\Scripts\activate`
4. Install required packages using the following command: `pip install -r requirements.txt`
5. **Since App packages are already installed and the virtual environment is already created, skip step 2 and 4. Just do step 1, 3, 6 and 7 or 8.**
6. Run the following command to start the backend server: `uvicorn main:app --reload`
7. The backend server should be running on http://localhost:8000
8. To view the documentation, go to http://localhost:8000/docs

### Running the Frontend
1. Open a new terminal and navigate to the frontend folder using the following command: `cd frontend`
2. Run the following command to install all the required packages: `npm install`
3. Run the following command to start the frontend server: `npm run dev`
4. The frontend server should be running on http://localhost:5173
5. To view the frontend, go to http://localhost:5173
6. Login using the following credentials:
    - Email: bota@gmail.com
    - Password: secret