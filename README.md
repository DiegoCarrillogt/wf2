# Data Processing API

A FastAPI-based REST API for data processing operations including filtering and aggregation.

## Features

- Filter collections based on field conditions
- Aggregate data with operations like sum, average, count, min, and max
- Interactive API documentation (Swagger UI)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/DiegoCarrillogt/wf2.git
cd wf2
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the server:
```bash
python app.py
```

2. Access the API documentation at: http://localhost:8001/docs

## API Endpoints

### POST /filter
Filter a collection based on field conditions.

Example request:
```json
{
    "collection": [
        {"id": 1, "name": "John", "age": 30},
        {"id": 2, "name": "Jane", "age": 25}
    ],
    "conditions": {
        "age": 30
    }
}
```

### POST /aggregate
Aggregate data by grouping and performing operations.

Example request:
```json
{
    "collection": [
        {"department": "IT", "salary": 5000},
        {"department": "IT", "salary": 6000},
        {"department": "HR", "salary": 4000}
    ],
    "group_by": "department",
    "aggregate_field": "salary",
    "operation": "avg"
}
```

## License

MIT
