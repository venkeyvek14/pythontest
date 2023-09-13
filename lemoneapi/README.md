# LemOneAI
VAPT Autopilot repository for Frontend

## Table of Contents

- [LemOneAI](#lemoneai)
  - [Table of Contents](#table-of-contents)
  - [About](#about)
  - [Installation](#installation)
      - [Prerequisites](#prerequisites)
      - [Environment Setup](#environment-setup)
    - [Installation](#installation-1)
      - [Update Configuration](#update-configuration)
      - [Execution](#execution)

## About

Backend for LemOneAi application

## Installation

#### Prerequisites

Before you begin, ensure that you have the following software versions installed:

- Python version: v3.8.0
- pip version: 23.2.1

#### Environment Setup

To set up the environment for running the app on your local machine, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/lemoneai/backend.git
2. Navigate to the project directory:
   ```bash
   cd backend
### Installation

1. **Create a virtual environment**:

    ```bash
    python3 -m venv venv
    ```

2. **Activate the virtual environment**:

    - On Windows:

        ```bash
        venv\Scripts\activate
        ```

    - On macOS and Linux:

        ```bash
        source venv/bin/activate
        ```

3. **Install project dependencies**:

    ```bash
    pip install -r requirements.txt
    ```




#### Update Configuration
Retrieve the required data from the vault and update the .env file with the necessary information.

#### Execution 
To run the app, execute the following command:
```bash
python3 manage.py runserver