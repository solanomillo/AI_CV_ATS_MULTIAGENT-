"""
Construcción del grafo de orquestación utilizando LangGraph.
"""

from langgraph.graph import StateGraph, START, END

from domain.state import EstadoCV
from agents.reader_agent import agente_lector_cv
from agents.extractor_agent import agente_extractor
from agents.ats_agent import agente_analizador_ats
from agents.scoring_agent import agente_scoring
from agents.optimizer_agent import agente_optimizador
from agents.persistence_agent import agente_persistencia


def decidir_siguiente_paso(estado: EstadoCV) -> str:
    """
    Decide si se debe ejecutar el optimizador
    según el score final.
    """

    score = estado.get("score_final")

    if score is None:
        return "persistencia"

    if score < 75:
        return "optimizador"

    return "persistencia"


def construir_grafo():
    """
    Construye y compila el grafo del sistema multi-agente.
    """

    builder = StateGraph(EstadoCV)

    # ----------- NODOS -----------

    builder.add_node("lector_cv", agente_lector_cv)
    builder.add_node("extractor", agente_extractor)
    builder.add_node("analizador_ats", agente_analizador_ats)
    builder.add_node("scoring", agente_scoring)
    builder.add_node("optimizador", agente_optimizador)
    builder.add_node("persistencia", agente_persistencia)

    # ----------- FLUJO PRINCIPAL -----------

    builder.add_edge(START, "lector_cv")
    builder.add_edge("lector_cv", "extractor")
    builder.add_edge("extractor", "analizador_ats")
    builder.add_edge("analizador_ats", "scoring")

    # ----------- DECISIÓN CON MAPA EXPLÍCITO -----------

    builder.add_conditional_edges(
        "scoring",
        decidir_siguiente_paso,
        {
            "optimizador": "optimizador",
            "persistencia": "persistencia"
        }
    )

    # Si pasa por optimizador → luego persistencia
    builder.add_edge("optimizador", "persistencia")

    # Persistencia siempre termina el flujo
    builder.add_edge("persistencia", END)

    grafo = builder.compile()

    return grafo