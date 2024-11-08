# Spy Cat Agency Management Application


### This is a CRUD application built for the Spy Cat Agency (SCA) to help manage spy cats, missions, and targets.

---

## Features

##### Spy Cats
* Create a Spy Cat: Add a new spy cat with details like name, years of experience, breed, and salary.
* Delete a Spy Cat: Remove a cat from the system.
* Update Spy Cat's Salary: Modify a cat's salary.
* List Spy Cats: Retrieve all spy cats in the system.
* View a Single Spy Cat: Retrieve information about a specific cat.
* Breed Validation: Each breed is validated using TheCatAPI.

##### Missions and Targets
* Create Mission with Targets: Add a new mission with 1-3 targets (name, country, notes, and completion status).
* Delete Mission: Remove a mission from the system if it hasn't been assigned to a cat.
* Update Target: Modify target notes and mark targets as complete.
* Notes can only be updated if the target and mission are not completed.
* Assign Mission to a Cat: Assign an available mission to a cat (one mission per cat).
* List Missions: Retrieve all missions in the system.
* View a Single Mission: Retrieve information about a specific mission.

---

## Backend
* **Docker** - Dockerfile and compose files for building and running the application.
* **FastAPI** - Python framework for building web applications.
* **PostgreSQL** - Database for storing data.
* **SQLAlchemy** - ORM for working with databases.
* **Alembic** - Database migration tool.
* **Pydantic** - Data validation library.

---
## Installation and Usage with Docker

Here's how to get the project up and running using docker and docker compose.

### Setup

1. Clone this repository:

    ```
    git clone git@github.com:nazya08/test-task-DevelopsToday.git
    ```

2. Copy .env file and fill environment variables
   ```
   cp .env.example .env
   ```
3. Build docker images:
   ```
   make build
   ```
4. Run docker images
   ```
   make up
   ```

Your application should now be running at `http://localhost:8000`

## Installation and Usage without Docker

Here's how to get the project up and running on your local machine for development and testing.

### Setup

1. Clone this repository:

    ```
    git clone git@github.com:nazya08/test_task_TheOriginals.git
    ```

2. Create virtual env.

    ```
    python -m venv venv
    ```

3. Activate virtual env.

   on Windows:

   ```
   cd venv/Scripts
   ```

   ```
   ./activate
   ```

   on Linux or Mac:

   ```
   source venv/bin/activate
   ```

4. Install requirements:

   ```
   pip install -r requirements.txt
   ```   

5. Run a project:

   ```
   python -m src.main.main
   ```

## Licence

MIT License

Created by Nazar Filoniuk, email: filoniuk.nazar.dev@gmail.com