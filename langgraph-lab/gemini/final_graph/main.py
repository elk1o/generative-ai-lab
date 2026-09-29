from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.types import Command
from constants import DB_FILE, USER_PROMPT, THREAD_ID
from graph import workflow

if __name__ == "__main__":
    # Setting up memory and checkpointers
    with SqliteSaver.from_conn_string(DB_FILE) as checkpointer:
        final_graph = workflow.compile(checkpointer=checkpointer)
        #final_graph.get_graph().draw_mermaid_png(output_file_path="graph.png")
        initial_input = {
            "message": USER_PROMPT,
            "initial_data_tries": 0,
            "draft_edit_tries": 0,
            "log": []
        }
        config = {"configurable": {"thread_id": THREAD_ID}}


        print(""" *****************
        Creando un grafo final completo
        **************** """)

        print("Superstep 1: START")
        final_exec = final_graph.invoke(initial_input, config=config)

        while "__interrupt__" in final_exec:
            informacion_usuario = final_exec["__interrupt__"][0].value
            print("\n--- El grafo necesita tu respuesta ---")
            print(informacion_usuario)

            respuesta_usuario = input("\nTu respuesta: ")

            final_exec = final_graph.invoke(
                Command(resume=respuesta_usuario),
                config=config
            )

        print("\n--- Resultado final ---")
        print(final_exec.get("respuesta_final"))
        print("Orden de ejecución:")
        print(final_exec.get("log"))