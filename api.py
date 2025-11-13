from fastapi import FastAPI, HTTPException, Body
from typing import Union, Dict, List, Any
import pandas as pd

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/config")
def config():
    return {
        "columns": ["Days to Graduate", "Requested Amount"],
        "message": "Simplified test API - accepts 1-2 variables"
    }


@app.post("/score")
def score(payload: Union[Dict[str, Any], List[Dict[str, Any]]] = Body(...)):
    """
    Simplified scoring endpoint for testing.
    Accepts 1-2 variables (Days to Graduate, Requested Amount) and returns fixed score of 99.
    """
    # Convert single dict to list
    rows = payload if isinstance(payload, list) else [payload]
    
    # Validate not empty
    if not rows:
        raise HTTPException(400, "Empty payload.")
    
    # Process each row
    results = []
    for row in rows:
        # Extract id if present, otherwise generate one
        row_id = row.get("id", f"row-{len(results)}")
        
        # Get optional fields (we don't actually use them, just for validation)
        days_to_graduate = row.get("Days to Graduate", None)
        requested_amount = row.get("Requested Amount", None)
        
        # Return fixed score of 99 and "approve" decision
        results.append({
            "id": row_id,
            "p_approve": 0.99,  # Fixed 99% probability
            "decision": "approve"  # Always approve for testing
        })
    
    return {"results": results}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
