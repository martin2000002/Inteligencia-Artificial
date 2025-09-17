# Build ontology for the assignment using OWL (RDF/XML)
# Ontología en español basada en las instrucciones de la tarea.
# Requires: pip install owlready2

from pathlib import Path
from owlready2 import get_ontology, Thing, ObjectProperty, DataProperty

BASE_IRI = "http://example.org/inteligencia-artificial/tarea1#"


def build_and_save(output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)

    onto = get_ontology(BASE_IRI)

    with onto:
        # Clases
        class Asignacion(Thing):
            pass

        class Ejercicio(Thing):
            pass

        class Problema(Thing):
            pass

        class Rompecabezas(Problema):
            pass

        class Juego(Problema):
            pass

        class ProblemaLogico(Problema):
            pass

        class Algoritmo(Thing):
            pass

        class AlgoritmoBusqueda(Algoritmo):
            pass

        class Estrategia(Algoritmo):
            pass

        class Heuristica(Thing):
            pass

        class Herramienta(Thing):
            pass

        class Lenguaje(Thing):
            pass

        class Artefacto(Thing):
            pass

        class Estado(Thing):
            pass

        class Restriccion(Thing):
            pass

        # Propiedades de objeto
        class tieneEjercicio(ObjectProperty):
            domain = [Asignacion]
            range = [Ejercicio]

        class modelaProblema(ObjectProperty):
            domain = [Ejercicio]
            range = [Problema]

        class usaAlgoritmo(ObjectProperty):
            domain = [Ejercicio]
            range = [Algoritmo]

        class usaHeuristica(ObjectProperty):
            domain = [Ejercicio]
            range = [Heuristica]

        class requiereLenguaje(ObjectProperty):
            domain = [Ejercicio]
            range = [Lenguaje]

        class produceArtefacto(ObjectProperty):
            domain = [Ejercicio]
            range = [Artefacto]

        class tieneRestriccion(ObjectProperty):
            domain = [Problema]
            range = [Restriccion]

        class tieneEstadoInicial(ObjectProperty):
            domain = [Problema]
            range = [Estado]

        class tieneEstadoObjetivo(ObjectProperty):
            domain = [Problema]
            range = [Estado]

        class visualizaCon(ObjectProperty):
            domain = [Ejercicio]
            range = [Herramienta]

        class verifica(ObjectProperty):
            domain = [Ejercicio]
            range = [Ejercicio]

        # Propiedades de datos
        class formatoSerializacion(DataProperty):
            domain = [Artefacto]
            range = [str]

        # Individuos comunes
        tarea1 = Asignacion("Tarea1"); tarea1.label = ["Tarea I"]
        protege = Herramienta("Protege"); protege.label = ["Protégé"]
        python = Lenguaje("Python")
        prolog = Lenguaje("Prolog")

        bfs = AlgoritmoBusqueda("BusquedaEnAmplitud")
        dfs = AlgoritmoBusqueda("BusquedaEnProfundidad")
        mejor_primero = AlgoritmoBusqueda("MejorPrimero")
        backtracking = Estrategia("Backtracking")

        h_manhattan = Heuristica("DistanciaManhattan")
        h_euclidiana = Heuristica("DistanciaEuclidiana")
        h_baldosas = Heuristica("BaldosasCorrectas")

        # Ejercicio 1: 8-fichas (8-Tile)
        e1 = Ejercicio("E1_OchoFichas"); e1.label = ["8-Tile"]
        p1 = Rompecabezas("P_OchoFichas")
        tarea1.tieneEjercicio.append(e1)
        e1.modelaProblema.append(p1)
        e1.usaAlgoritmo += [bfs, dfs, mejor_primero]
        e1.usaHeuristica += [h_manhattan, h_euclidiana, h_baldosas]

        s1_i = Estado("E1_Inicial")
        s1_g = Estado("E1_Objetivo")
        p1.tieneEstadoInicial.append(s1_i)
        p1.tieneEstadoObjetivo.append(s1_g)

        # Ejercicio 2: N-Reinas (backtracking)
        e2 = Ejercicio("E2_NReinas")
        p2 = Rompecabezas("P_NReinas")
        tarea1.tieneEjercicio.append(e2)
        e2.modelaProblema.append(p2)
        e2.usaAlgoritmo.append(backtracking)
        e2.requiereLenguaje.append(python)

        # Ejercicio 3: 4-en-raya (Mejor-Primero + heurísticas)
        e3 = Ejercicio("E3_CuatroEnRaya")
        p3 = Juego("P_CuatroEnRaya")
        tarea1.tieneEjercicio.append(e3)
        e3.modelaProblema.append(p3)
        e3.usaAlgoritmo.append(mejor_primero)
        e3.usaHeuristica += [h_manhattan, h_euclidiana]

        # Ejercicio 4a: Granjero, Lobo, Cabra, Col (Prolog + backtracking)
        e4a = Ejercicio("E4a_FWGC")
        p4a = ProblemaLogico("P_FWGC")
        tarea1.tieneEjercicio.append(e4a)
        e4a.modelaProblema.append(p4a)
        e4a.usaAlgoritmo.append(backtracking)
        e4a.requiereLenguaje.append(prolog)

        c_fwgc1 = Restriccion("NoLoboConCabraSinGranjero")
        c_fwgc2 = Restriccion("NoCabraConColSinGranjero")
        p4a.tieneRestriccion += [c_fwgc1, c_fwgc2]
        p4a.tieneEstadoInicial.append(Estado("FWGC_Inicial"))
        p4a.tieneEstadoObjetivo.append(Estado("FWGC_Objetivo"))

        # Ejercicio 4b: Misioneros y Caníbales (Prolog + backtracking)
        e4b = Ejercicio("E4b_MisionerosCanibales")
        p4b = ProblemaLogico("P_MisionerosCanibales")
        tarea1.tieneEjercicio.append(e4b)
        e4b.modelaProblema.append(p4b)
        e4b.usaAlgoritmo.append(backtracking)
        e4b.requiereLenguaje.append(prolog)

        c_mc = Restriccion("NoCanibalesSuperanMisioneros")
        p4b.tieneRestriccion.append(c_mc)
        p4b.tieneEstadoInicial.append(Estado("MC_Inicial"))
        p4b.tieneEstadoObjetivo.append(Estado("MC_Objetivo"))

        # Ejercicio 5: Verificación (imperativo)
        e5 = Ejercicio("E5_Verificacion")
        tarea1.tieneEjercicio.append(e5)
        e5.requiereLenguaje.append(python)
        # Verifica los dos ejercicios de Prolog
        e5.verifica += [e4a, e4b]

        # Ejercicio 6: Redes Semánticas (RDF/OWL + Protégé)
        e6 = Ejercicio("E6_RedesSemanticas")
        tarea1.tieneEjercicio.append(e6)
        e6.visualizaCon.append(protege)
        # Artefacto a entregar: la ontología
        ont_artifact = Artefacto("OntologiaOWL")
        ont_artifact.formatoSerializacion.append("RDF/XML (OWL)")
        e6.produceArtefacto.append(ont_artifact)

    # Guardar solo en OWL (RDF/XML)
    owl_path = output_dir / "ontology.owl"
    onto.save(file=str(owl_path), format="rdfxml")
    return owl_path


def main():
    here = Path(__file__).resolve().parent
    out_dir = here / "ontology"
    owl_file = build_and_save(out_dir)
    print(f"Ontología guardada en: {owl_file}")


if __name__ == "__main__":
    main()
