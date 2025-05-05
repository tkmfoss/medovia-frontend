💊 Pharmacy Dashboard
📌 Project Overview
The Pharmacy Dashboard is a modern, responsive web application designed to streamline pharmacy operations. It provides pharmacists with an intuitive interface to manage medicine inventories, track stock levels, view reports, and prepare for real-time sales tracking and data integration.

This project demonstrates strong front-end skills with advanced JavaScript interactivity, and also includes a backend scaffold using Flask (Python) and modern frontend tooling powered by Vite and pnpm.

🛠️ Tech Stack
Technology	Role
HTML5	Structure and layout of the web pages
CSS3	Styling and responsive design (Flexbox, Grid)
JavaScript	UI interactions, transitions, collapsible sidebar
Flask (Python)	Backend API handling (form processing, routing)
Vite	Frontend development build tool
pnpm	Package manager (faster and lighter alternative to npm)
Jinja2	Templating engine used by Flask

🎯 Features
✅ Core Functionalities
Collapsible Sidebar with intuitive icons and labels

Inventory Management Panel

View medicine name, stock, expiry, and availability

Add Medicine Form

Form-based UI to simulate adding new entries

Home Panel

Placeholder for metrics (total stock, sales, low stock alerts)

Reports Section

Simulated reports for weekly/monthly overviews

Fully Responsive UI

Adapts to desktop, tablet, and mobile views

Frontend-Backend Connection Ready

Flask routes and form handling are pre-configured for expansion

🚀 Future Enhancements
Real-time stock and expiry alerts

Role-based authentication (Admin, Pharmacist)

Database integration (MongoDB or SQLAlchemy)

Advanced sales analytics and chart visualizations

Export reports (PDF, Excel)

Search/filter inventory

Dark mode toggle

🎨 UI/UX Highlights
Clean, calm, and professional color palette

Smooth collapsible sidebar transitions

Card-based layout for clarity and structure

Tooltip-like hover effects for better usability

🧪 How to Run the Project Locally
✅ Make sure Python 3.10+, Node.js, and pnpm are installed before proceeding.

1. Clone the Repository
bash
Copy
Edit
git clone https://github.com/Adithyan19/Pharmacy-Dashboard.git
cd Pharmacy-Dashboard
2. Install Frontend Dependencies (Vite + pnpm)
bash
Copy
Edit
pnpm install
3. Run the Frontend
bash
Copy
Edit
pnpm run dev
This will start the frontend at: http://localhost:5173

4. Run the Backend (Flask)
bash
Copy
Edit
# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install Flask
pip install flask

# Run the Flask server
python app.py
Backend will run at: http://localhost:5000

5. Open the App in Your Browser
Depending on your integration, access via:

Frontend Interface

Backend API/forms (Flask)

🧑‍💻 Project Structure (Overview)
vbnet
Copy
Edit
📦 Pharmacy-Dashboard/
 ┣ 📁 static/           → CSS, JS, assets (served by Flask)
 ┣ 📁 templates/        → HTML templates for Jinja2 rendering
 ┣ 📁 src/              → Source files for Vite frontend (optional)
 ┣ 📁 public/           → Public assets (favicon, etc.)
 ┣ 📄 app.py            → Flask backend
 ┣ 📄 index.html        → Entry HTML for simple static render
 ┣ 📄 vite.config.js    → Vite config
 ┣ 📄 package.json      → Frontend dependencies
 ┣ 📄 README.md         → 📘 You're here!
