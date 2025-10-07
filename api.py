import json, joblib
from typing import List, Dict, Any, Union
import numpy as np, pandas as pd
from fastapi import FastAPI, Body, HTTPException

app = FastAPI(title="Triage API")

PIPE = joblib.load("model.joblib")
CFG = json.load(open("model_config.json"))

COLS, POS_LABEL = CFG["columns"], CFG["pos_label"]
LOWER, UPPER = CFG["lower"], CFG["upper"]

clf = PIPE.named_steps.get("clf", PIPE)
CLASSES = list(clf.classes_)
POS_IDX = CLASSES.index(POS_LABEL)

def prep(rows: List[Dict[str, Any]]) -> pd.DataFrame:
    df = pd.DataFrame(rows)
    for c in COLS:
        if c not in df.columns:
            df[c] = np.nan
    return df[COLS]

@app.get("/health")
def health(): return {"status": "ok"}

@app.get("/config")
def config(): return {"columns": COLS, "pos_label": POS_LABEL, "lower": LOWER, "upper": UPPER}

@app.post("/score")
def score(payload: Union[Dict[str, Any], List[Dict[str, Any]]] = Body(...)):
    rows = payload if isinstance(payload, list) else [payload]
    if not rows: raise HTTPException(400, "Empty payload.")
    X = prep(rows)
    proba = PIPE.predict_proba(X)[:, POS_IDX]
    decision = np.where(proba >= UPPER, "approve",
                 np.where(proba <= LOWER, "reject", "review"))
    ids = X["id"].tolist() if "id" in X.columns else list(range(len(X)))
    return {"results": [{"id": i, "p_approve": float(p), "decision": d} for i,p,d in zip(ids, proba, decision)]}
