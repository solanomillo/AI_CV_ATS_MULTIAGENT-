"""
Construcción del grafo de orquestación utilizando LangGraph.
"""
from agents.scoring_agent import agente_scoring
from langgraph.graph import StateGraph, START, END
from domain.state import EstadoCV
from agents.extractor_agent import agente_extractor
from agents.ats_agent import agente_analizador_ats
from agents.optimizer_agent import agente_optimizador


def decidir_siguiente_paso(estado: EstadoCV) -> str:
    score = estado.get("score_final")

    if score is None:
        return END

    if score < 75:
        return "optimizador"

    return END


def construir_grafo():
    """
    Construye y compila el grafo del sistema multi-agente.
    """

    builder = StateGraph(EstadoCV)

    # Nodos
    builder.add_node("extractor", agente_extractor)
    builder.add_node("analizador_ats", agente_analizador_ats)
    builder.add_node("optimizador", agente_optimizador)

    # 🔥 CONEXIÓN DESDE START
    builder.add_node("scoring", agente_scoring)
    builder.add_edge(START, "extractor")
    builder.add_edge("extractor", "analizador_ats")
    builder.add_edge("analizador_ats", "scoring")
    builder.add_conditional_edges(
        "scoring",
        decidir_siguiente_paso
    )

    builder.add_edge("optimizador", END)

    grafo = builder.compile()

    return grafo