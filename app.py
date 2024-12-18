from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from typing import List, Dict, Any
import uvicorn

class FilterRequest(BaseModel):
    collection: List[Dict[str, Any]]
    conditions: Dict[str, Any]  # Format: {"field": "value"}

class AggregateRequest(BaseModel):
    collection: List[Dict[str, Any]]
    group_by: str
    aggregate_field: str
    operation: str  # "sum", "avg", "count", "min", "max"

app = FastAPI(title="Data Processing API")

@app.get("/", include_in_schema=False)
def index():
    return RedirectResponse("/docs", status_code=308)

@app.post("/filter")
def filter_data(request: FilterRequest):
    """Filter a collection of dictionaries based on matching conditions.
    Returns items that match ALL specified conditions."""
    filtered_data = []
    
    for item in request.collection:
        matches = True
        for field, value in request.conditions.items():
            if field not in item or item[field] != value:
                matches = False
                break
        if matches:
            filtered_data.append(item)
    
    return {
        "filtered_data": filtered_data,
        "total_items": len(request.collection),
        "matched_items": len(filtered_data)
    }

@app.post("/aggregate")
def aggregate_data(request: AggregateRequest):
    """Aggregate data by grouping on a specified field and performing
    an aggregation operation (sum, avg, count, min, max) on another field."""
    if request.operation not in ["sum", "avg", "count", "min", "max"]:
        raise HTTPException(status_code=400, detail="Invalid operation")
    
    groups = {}
    for item in request.collection:
        if request.group_by not in item:
            continue
            
        group_key = item[request.group_by]
        if group_key not in groups:
            groups[group_key] = []
            
        if request.aggregate_field in item:
            groups[group_key].append(item[request.aggregate_field])
    
    result = {}
    for group_key, values in groups.items():
        if request.operation == "sum":
            result[group_key] = sum(values)
        elif request.operation == "avg":
            result[group_key] = sum(values) / len(values) if values else 0
        elif request.operation == "count":
            result[group_key] = len(values)
        elif request.operation == "min":
            result[group_key] = min(values) if values else None
        elif request.operation == "max":
            result[group_key] = max(values) if values else None
    
    return {
        "aggregated_data": result,
        "total_groups": len(result)
    }

if __name__ == '__main__':
    uvicorn.run('app:app', host='0.0.0.0', port=8001)
