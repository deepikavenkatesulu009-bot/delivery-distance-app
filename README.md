Delivery Distance App

A full-stack application to calculate and visualize delivery distances between addresses.
Built with a FastAPI backend and a Svelte frontend, using PostgreSQL (Neon) for storage and Redis (Upstash) for caching.

Clone the Repository
git clone https://github.com/deepikavenkatesulu009-bot/delivery-distance-app.git
cd delivery-distance-app

Database and Redis Setup

The backend uses PostgreSQL and Redis.
You can run local instances for development, or connect directly to the existing production databases (Neon for Postgres and Upstash for Redis).

Update your .env file

Create a file named .env in the project root (same folder as app/ or main.py) and include:

Example .env
PORT=8000
DATABASE_URL=postgresql://postgres:password@localhost:5432/mydb
REDIS_URL=redis://localhost:6379
USER_AGENT=delivery-distance-app/1.0 (your_email@example.com)
NOMINATIM_CONTACT_EMAIL=your_email@example.com
CORS_ORIGINS=*


Important Notes

Do not include quotation marks around any values.

If you do not have local Postgres or Redis installed, the backend will automatically use the production Neon and Upstash links defined in your environment.

For production Redis (Upstash), always use the rediss:// scheme to enable TLS encryption.

Backend Setup (FastAPI)
1. Create a virtual environment
python3 -m venv venv
source venv/bin/activate   # macOS/Linux
 OR (Windows)
venv\Scripts\activate

2. Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

3. Start the backend
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload


If your FastAPI app is defined in a different file (e.g., main.py in the root), use:

uvicorn main:app --reload


Once it starts, open your browser at:

http://localhost:8000/docs

Test Endpoints
curl http://localhost:8000/health


Expected output:

{"status": "ok"}

Frontend Setup (Svelte)
1. Navigate to frontend folder

If your frontend is located in a folder named frontend or ui, navigate into it:

cd frontend
or cd ui

2. Install dependencies
npm install

3. Start the development server
npm run dev


The frontend will start on:

http://localhost:5173


Make sure your frontend API configuration (e.g., .env or constants file) points to your backend URL:

http://localhost:8000

Run Both Together

Open two terminals.

Terminal 1 – Backend:

uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload


Terminal 2 – Frontend:

cd frontend
npm run dev


Now open:

Frontend: http://localhost:5173
Backend:  http://localhost:8000


The frontend should communicate with the backend successfully.

Run with Docker (optional)

If you prefer to use Docker instead of a Python virtual environment:

docker build -t delivery-distance-app .
docker run --rm --platform=linux/amd64 --env-file .env -p 8000:8000 delivery-distance-app


Then open:

http://localhost:8000/docs

Troubleshooting
Problem	Likely Cause	Fix
500 Internal Server Error	Redis not reachable	Use rediss:// for Upstash (TLS required)
Database connection failed	Bad credentials or SSL not enabled	Add sslmode=require to your Postgres URL
"8000" is not a valid port number	Quoted value in .env	Remove quotes from all env values
Frontend not calling backend	Wrong API base URL	Update to http://localhost:8000 in frontend config
Author

Deepika Venkatesulu
Email: deepikavenkatesulu009@gmail.com

License

MIT © 2025 Deepika Venkatesulu

Quickstart Summary
# Clone repo
git clone https://github.com/deepikavenkatesulu009-bot/delivery-distance-app.git
cd delivery-distance-app

# Setup .env file (see example above)

# Setup backend
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload

# Setup frontend (in new terminal)
cd frontend
npm install
npm run dev

# Open in browser
Backend:  http://localhost:8000/docs
Frontend: http://localhost:5173

