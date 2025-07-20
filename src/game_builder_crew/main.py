import sys
import os
import yaml
import subprocess
from dotenv import load_dotenv
from game_builder_crew.crew import GameBuilderCrew


def check_langsmith_tracing():
    """Checks and prints the status of LangSmith tracing."""
    print("## Checking LangSmith Tracing Configuration")

    print("--- All Environment Variables ---")
    for key, value in os.environ.items():
        print(f"{key}: {value}")
    print("-------------------------------")
    # The primary variable to enable tracing is LANGCHAIN_TRACING_V2.
    if os.environ.get("LANGCHAIN_TRACING_V2") == "true":
        print("LangSmith tracing is enabled.")

        # The API key is also essential.
        api_key = os.environ.get("LANGCHAIN_API_KEY")
        if api_key:
            print("  - LANGCHAIN_API_KEY is set.")
        else:
            print("  - WARNING: LANGCHAIN_API_KEY is not set. Tracing will likely fail.")

        # The project name is optional.
        project = os.environ.get("LANGCHAIN_PROJECT")
        if project:
            print(f"  - Logging to LangSmith project: '{project}'")
        else:
            print("  - Logging to the default LangSmith project.")
    else:
        print("LangSmith tracing is not enabled (LANGCHAIN_TRACING_V2 is not set to 'true').")

def run():
    # Replace with your inputs, it will automatically interpolate any tasks and agents information
    load_dotenv()
    check_langsmith_tracing()
    print("## Welcome to the Game Crew")
    print('-------------------------------')

    with open('src/game_builder_crew/config/gamedesign.yaml', 'r', encoding='utf-8') as file:
        examples = yaml.safe_load(file)

    inputs = {
        'game' :  examples['example3_snake']
    }
    game= GameBuilderCrew().crew().kickoff(inputs=inputs)

    print("\n\n########################")
    print("## Here is the result")
    print("########################\n")
    print("final code for the game:")
    print(game)

    game_file_path = 'src/game_builder_crew/game.py'
    with open(game_file_path, 'w', encoding='utf-8') as file:
        file.write(game.__str__())

    print("\n########################")
    print(f"## Game code saved to '{game_file_path}'. Running it now...")
    print("########################\n")
    subprocess.run([sys.executable, game_file_path], check=False)
    

# def train():
#     """
#     Train the crew for a given number of iterations.
#     """

#     with open('src/game_builder_crew/config/gamedesign.yaml', 'r', encoding='utf-8') as file:
#         examples = yaml.safe_load(file)

#     inputs = {
#         'game' : examples['example1_pacman']
#     }
#     try:
        
#         GameBuilderCrew().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

#     except Exception as e:
#         raise Exception(f"An error occurred while training the crew: {e}")


if __name__ == "__main__":
    run()
