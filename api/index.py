from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="API Distribuida - Laboratorio IV")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Tarea(BaseModel):
    id: Optional[int] = None
    titulo: str
    descripcion: str
    completada: bool = False

tareas: List[Tarea] = []

@app.get("/api/tareas")
def listar_u_obtener_tareas(tarea_id: Optional[int] = Query(default=None)):
    if tarea_id is None:
        return tareas

    for tarea in tareas:
        if tarea.id == tarea_id:
            return tarea

    raise HTTPException(status_code=404, detail="Tarea no encontrada")

@app.post("/api/tareas")
def crear_tarea(tarea: Tarea):
    tarea.id = len(tareas) + 1
    tareas.append(tarea)
    return {"mensaje": "Tarea creada exitosamente", "tarea": tarea}

@app.put("/api/tareas")
def actualizar_tarea(tarea_actualizada: Tarea, tarea_id: int = Query(...)):
    for i, tarea in enumerate(tareas):
        if tarea.id == tarea_id:
            tarea_actualizada.id = tarea_id
            tareas[i] = tarea_actualizada
            return {
                "mensaje": "Tarea actualizada exitosamente",
                "tarea": tarea_actualizada
            }

    raise HTTPException(status_code=404, detail="Tarea no encontrada")

@app.delete("/api/tareas")
def eliminar_tarea(tarea_id: int = Query(...)):
    for i, tarea in enumerate(tareas):
        if tarea.id == tarea_id:
            del tareas[i]
            return {"mensaje": "Tarea eliminada exitosamente"}

    raise HTTPException(status_code=404, detail="Tarea no encontrada")
