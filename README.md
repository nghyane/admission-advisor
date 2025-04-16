# Admission Advisor Agent

This is an AI agent designed to provide admission advising services for prospective students. The agent can answer questions about academic programs, admission requirements, tuition fees, and more.

## Features

- Provides information about available academic programs
- Checks admission requirements for specific programs
- Calculates tuition fees based on program, credits, and residency status
- Schedules appointments with human advisors
- Checks application status
- Provides information about admission years, majors, careers, and campuses
- Offers detailed admission requirements by major

## Setup

1. Clone the repository
2. Install dependencies:
   ```
   gcloud auth login
gcloud services enable aiplatform.googleapis.com
   ```
   
   if you have not installed poetry before then run `pip install poetry` first. the you can create your virtual environment and install all dependencies using:
   ```
   poetry install
   ```
   To activate the virtual environment run:
   ```
   poetry env activate
   ```

3. Set up your environment variables in the `.env` file:
   ```
   GOOGLE_API_KEY=your_api_key
   GOOGLE_CLOUD_PROJECT=your_project_id
   GOOGLE_CLOUD_LOCATION=your_location
   GOOGLE_GENAI_USE_VERTEXAI=1
   ```

## Usage

```python
from admission_advisor import root_agent

# Run the agent
response = root_agent.run("Tôi muốn biết thông tin về ngành Công nghệ thông tin")
print(response)
```

## Project Structure

```
admission-advisor/
├── admission_advisor/
│   ├── __init__.py
│   ├── agent.py         # Main agent definition
│   ├── config.py        # Configuration settings
│   ├── prompts.py       # Agent instructions
│   ├── entities/        # Data models
│   │   ├── __init__.py
│   │   └── student.py   # Student entity model
│   ├── shared_libraries/
│   │   ├── __init__.py
│   │   └── callbacks.py # Callback functions
│   └── tools/
│       ├── __init__.py
│       └── tools.py     # Tool implementations
├── .env                 # Environment variables
└── README.md            # Documentation
```

## Tools

The agent includes the following tools:

- `get_program_information`: Get details about academic programs
- `check_admission_requirements`: Check if a student meets requirements for a program
- `calculate_tuition_fees`: Calculate tuition costs
- `schedule_advisor_appointment`: Book appointments with human advisors
- `check_application_status`: Check status of submitted applications
- `submit_application`: Submit applications for programs
- `get_admission_years`: Get information about admission years
- `get_majors`: Get information about available majors
- `get_careers_by_major`: Get career prospects for specific majors
- `get_campuses`: Get information about university campuses
- `get_majors_by_campus`: Get majors available at specific campuses
- `get_admission_requirements_by_major`: Get detailed admission requirements

## License

This project is licensed under the Apache License 2.0 - see the LICENSE file for details.
