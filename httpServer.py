from src.resolution import Node
from src.tirage import tirage
from time import time

from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Utils
def formatHTTPResponse(data):
    return {
        "status": True,
        "responseData": data
    }

class resolutionPayload(BaseModel):
    tirage: list[int]
    objectif: int

# HTTP Endpoints

# GET /
@app.get("/")
def tirages():
    return formatHTTPResponse('Hello World')

# GET /tirages
@app.get("/tirages")
def tirages():
    jeu = tirage()

    return formatHTTPResponse(jeu)


# POST /resolution
@app.post("/tirages")
def tirages(_resolutionPayload: resolutionPayload):
    startTimeStamp = time()
    parent_node = Node(_resolutionPayload.tirage, _resolutionPayload.objectif)

    parent_node.generate_tree()
    solutions = parent_node.get_list_of_solutions()
    firstSolution = None;

    if len(solutions):
        ### Find minimal depth solution
        _min = 0
        for i in range(len(solutions)):
            if solutions[i].depth < solutions[_min].depth:
                _min = i
        
        firstSolution = str(solutions[_min])
    else:
        ### Parcourir l'arbre pour trouver la solution la plus proche
        solution = parent_node.find_best_solution()
        firstSolution = str(solution)

    ### Convert Response to JSON Adapter
    _parsedSolution = firstSolution.split('\n')
    parsedSolution = []

    for line in _parsedSolution:
        if (line == ""): continue

        calcul = line.split('=')
        
        # Remove last space from '=' and remove first space after '='
        calcul[0] = calcul[0][:-1]
        calcul[1] = calcul[1][1:]

        parsedSolution.append(calcul)
        
    return formatHTTPResponse({
       "timeStamp": round(time() - startTimeStamp, 3),
        "solution": parsedSolution
    })
    