"""
Construcción del grafo de orquestación utilizando LangGraph.
Versión optimizada: flujo lineal profesional.
"""

from langgraph.graph import StateGraph, START, END
from domain.state import EstadoCV

from agents.reader_agent import agente_lector_cv
from agents.extractor_agent import agente_extractor
from agents.ats_agent import agente_analizador_ats
from agents.scoring_agent import agente_scoring
from agents.optimizer_agent import agente_optimizador
from agents.persistence_agent import agente_persistencia


def construir_grafo():
    """
    Grafo lineal: lector → extractor → analizador → scoring → optimizador → persistencia
    El optimizador decide internamente cómo optimizar según el score.
    """

    builder = StateGraph(EstadoCV)

    # ---- NODOS ----
    builder.add_node("lector_cv", agente_lector_cv)
    builder.add_node("extractor", agente_extractor)
    builder.add_node("analizador_ats", agente_analizador_ats)
    builder.add_node("scoring", agente_scoring)
    builder.add_node("optimizador", agente_optimizador)
    builder.add_node("persistencia", agente_persistencia)

    # ---- FLUJO LINEAL ----
    builder.add_edge(START, "lector_cv")
    builder.add_edge("lector_cv", "extractor")
    builder.add_edge("extractor", "analizador_ats")
    builder.add_edge("analizador_ats", "scoring")
    builder.add_edge("scoring", "optimizador")  # siempre pasa por optimizador
    builder.add_edge("optimizador", "persistencia")
    builder.add_edge("persistencia", END)

    grafo = builder.compile()
    return grafo