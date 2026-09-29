from langchain.tools import tool
from constants import COURSES_CATALOGUE

@tool
def search_AI_training(nivel: str) -> str:
    """
    Looks for courses by level: basico, intermedio o avanzado.
    """
    programa = COURSES_CATALOGUE.get(nivel.lower())
    if not programa:
        return "Programa no encontrado."
    return f"{programa['nombre']}: {programa['precio_por_persona']}€/persona, {programa['duracion_horas']}h"

@tool
def calculate_budget(nivel: str, num_participantes: int) -> str:
    """
    Calculates the total budget for a number of participants.
    """
    programa = COURSES_CATALOGUE.get(nivel.lower())
    if not programa:
        return "No se pudo calcular, programa no encontrado."
    total = programa["precio_por_persona"] * num_participantes
    return f"Presupuesto total: {total}€ para {num_participantes} participantes"
