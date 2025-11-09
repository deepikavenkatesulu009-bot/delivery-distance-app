1. Clone the Repository

git clone https://github.com/deepikavenkatesulu009-bot/delivery-distance-app.git

cd delivery-distance-app


2. Database and Redis Setup

The backend uses PostgreSQL and Redis.
You can run local instances for development, or you can connect directly to the existing production databases (Neon for Postgres and Upstash for Redis).

Update your .env file

Make sure your .env file (in the project root) includes the correct database and cache URLs:
PORT=8000
DATABASE_URL=postgresql://postgres:password@localhost:5432/mydb
REDIS_URL=redis://localhost:6379
USER_AGENT=delivery-distance-app/1.0 (<your_email@example.com>)
NOMINATIM_CONTACT_EMAIL=<your_email@example.com>
CORS_ORIGINS=*



Do not include quotation marks around any values.

Local vs. Production Connections

If you have local Postgres or Redis installed, you can replace these URLs with your local connection strings (for example: postgresql://postgres:password@localhost:5432/mydb and redis://localhost:6379).

3. Backend Setup (FastAPI)

Create a virtual environment
python3 -m venv venv
source venv/bin/activate   # macOS/Linux
# OR
venv\Scripts\activate      # Windows

Install dependencies
pip install --upgrade pip
pip install -r requirements.txt



Start the backend
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

Once it starts, open:

Test endpoints
curl http://localhost:8000/health

Expected output:
{"status": "ok"}


4. Frontend Setup (Svelte)
Navigate to frontend folder
If your frontend is in a frontend or ui subfolder, go there:
cd frontend
# or cd ui

Install dependencies
npm install

Start the development server
npm run dev

The frontend will start on:
http://localhost:5173
If it needs to connect to the backend, make sure the backend URL in your frontend .env or configuration file points to:
http://localhost:8000



5. Run Both Together
Using two terminals
Terminal 1:
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

Terminal 2:
cd frontend
npm run dev

Now open your browser:
http://localhost:5173
The frontend should communicate with backend at http://localhost:8000

6. Run with Docker (optional)
Build and run locally:
docker build -t delivery-distance-app .
docker run --rm --platform=linux/amd64 --env-file .env -p 8000:8000 delivery-distance-app

Then visit:
http://localhost:8000/docs



Author
Deepika Venkatesulu
Email: deepikavenkatesulu009@gmail.com

License
MIT © 2025 Deepika Venkatesulu

Quickstart Summary
# clone repo
git clone https://github.com/deepikavenkatesulu009-bot/delivery-distance-app.git
cd delivery-distance-app

# setup .env file

# setup backend
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload

# setup frontend (in new terminal)
cd frontend
npm install
npm run dev

# open
Backend: http://localhost:8000/docs
Frontend: http://localhost:5173

