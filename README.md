# NetSmart

NetSmart is a web-based cyber awareness portal built with Flask and SQLite. It serves as an educational dashboard that exposes the operational mechanics of 20 modern digital scams and financial fraud vectors.

## Features

* **Threat Database:** Structured details on 20 real-world scams, including AI deepfakes, digital arrest extortion, UPI fraud, and fake loan apps.
* **Granular Breakdown:** Each threat contains a step-by-step explanation of its mechanics, actual message examples used by scammers, and an emergency response protocol for victims.
* **Live Search:** Client-side filtering allowing users to search through threats instantly without reloading the page.
* **Security Blueprint:** A persistent sidebar detailing universal system red flags and a checklist of sensitive variables that must never be shared online.

## Tech Stack

* **Backend:** Python, Flask
* **Database:** SQLite
* **Frontend:** HTML5, Tailwind CSS, JavaScript (Vanilla)

## Directory Structure

```text
netsmart/
│
├── app.py              # Flask application routes and backend logic
├── database.db         # SQLite database file (ignored by version control)
├── schema.sql          # Database schema and initial data seeding script
├── .gitignore          # Git ignore configuration
│
└── templates/
    └── index.html      # Monolithic frontend dashboard UI

```

## Installation and Setup

1. Clone the repository and navigate into the project directory:
```bash
cd netsmart

```


2. Create and activate a Python virtual environment:
```bash
python3 -m venv .venv
source .venv/bin/activate

```


3. Install Flask:
```bash
pip install Flask

```


4. Initialize the database and seed the 20 threat profiles:
```bash
python3 -c "import app; app.init_db()"

```


5. Run the application:
```bash
python app.py

```


6. Open your browser and navigate to:
```text
http://127.0.0.1:5000

```



## Development Notes

* The `database.db` file is automatically excluded from version control via `.gitignore` to ensure local runtime data does not clutter the repository history.
* Frontend styling is pulled dynamically via the Tailwind CSS CDN. No local build step is required for the CSS.