import os
import subprocess
import sys
import webbrowser

import questionary

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
PIPELINE_DIR = os.path.join(PROJECT_ROOT, "pipeline")
COMPOSE_NETWORK = "learningdataengineering_default"


def run(cmd, cwd=None, confirm=False):
    if confirm and not questionary.confirm(f"Run: {cmd}").ask():
        return
    print(f"\n> {cmd}\n")
    subprocess.run(cmd, shell=True, cwd=cwd or PROJECT_ROOT)
    input("\nPress Enter to continue...")


def infrastructure_menu():
    while True:
        choice = questionary.select(
            "Infrastructure",
            choices=[
                "Start all services (detached)",
                "Start all services (attached)",
                "Start Kestra only",
                "Stop services",
                "Stop services + wipe volumes",
                "Check running containers",
                "Stream Kestra logs",
                "Back",
            ],
        ).ask()
        if choice is None or choice == "Back":
            break
        elif choice == "Start all services (detached)":
            run("docker compose up -d")
        elif choice == "Start all services (attached)":
            run("docker compose up")
        elif choice == "Start Kestra only":
            run("docker compose up -d kestra")
        elif choice == "Stop services":
            run("docker compose down")
        elif choice == "Stop services + wipe volumes":
            run("docker compose down -v", confirm=True)
        elif choice == "Check running containers":
            run("docker ps")
        elif choice == "Stream Kestra logs":
            run("docker compose logs -f kestra")


def pipeline_menu():
    while True:
        choice = questionary.select(
            "Data Pipeline",
            choices=[
                "Run ingest (yellow taxi Jan 2021)",
                "Connect to DB (pgcli)",
                "Open pgAdmin (browser)",
                "Open Kestra UI (browser)",
                "Back",
            ],
        ).ask()
        if choice is None or choice == "Back":
            break
        elif "ingest" in choice:
            run(
                f"docker run -it --rm"
                f" --network={COMPOSE_NETWORK}"
                f" taxi_ingest:v001"
                f" --pg_user=root --pg_pass=root"
                f" --pg_host=pgdatabase --pg_port=5432"
                f" --pg_db=ny_taxi"
                f" --target_table=yellow_taxi_trips"
            )
        elif "pgcli" in choice:
            run("uv run pgcli -h localhost -p 5432 -u root -d ny_taxi", cwd=PIPELINE_DIR)
        elif "pgAdmin" in choice:
            webbrowser.open("http://localhost:8085")
            print("Opened pgAdmin in browser.")
            input("\nPress Enter to continue...")
        elif "Kestra" in choice:
            webbrowser.open("http://localhost:8080")
            print("Opened Kestra UI in browser.")
            input("\nPress Enter to continue...")


def build_menu():
    while True:
        choice = questionary.select(
            "Build",
            choices=[
                "Build ingest image",
                "Back",
            ],
        ).ask()
        if choice is None or choice == "Back":
            break
        elif "Build" in choice:
            run("docker build --no-cache -t taxi_ingest:v001 pipeline/")


def cleanup_menu():
    while True:
        choice = questionary.select(
            "Cleanup",
            choices=[
                "Remove stopped containers",
                "Remove unused images",
                "Remove unused volumes",
                "Remove unused networks",
                "Full system cleanup (removes EVERYTHING)",
                "Back",
            ],
        ).ask()
        if choice is None or choice == "Back":
            break
        elif "containers" in choice:
            run("docker container prune", confirm=True)
        elif "images" in choice:
            print("\n WARNING: This removes ALL unused images, including Kestra (3.1GB re-download if removed).")
            print("         Only proceed if you're sure you won't need them soon.\n")
            run("docker image prune -a", confirm=True)
        elif "volumes" in choice:
            print("\n WARNING: This deletes all volume data — Postgres data, pgAdmin config, Kestra state.")
            print("         Your database will be empty after this.\n")
            run("docker volume prune", confirm=True)
        elif "networks" in choice:
            run("docker network prune", confirm=True)
        elif "EVERYTHING" in choice:
            print("\n WARNING: This removes ALL containers, images, volumes, and networks.")
            print("         Includes the 3.1GB Kestra image and ALL database data.")
            print("         Everything will need to be re-downloaded and re-set-up.\n")
            if not questionary.confirm("Type 'yes' to confirm — are you absolutely sure?").ask():
                continue
            run("docker system prune -a --volumes", confirm=True)


def main():
    print("\nData Engineering Zoomcamp — Command Runner")
    print("=" * 43)

    while True:
        try:
            choice = questionary.select(
                "Main Menu",
                choices=[
                    "Infrastructure",
                    "Data Pipeline",
                    "Build",
                    "Cleanup",
                    "Exit",
                ],
            ).ask()
            if choice is None or choice == "Exit":
                print("Bye!")
                break
            elif choice == "Infrastructure":
                infrastructure_menu()
            elif choice == "Data Pipeline":
                pipeline_menu()
            elif choice == "Build":
                build_menu()
            elif choice == "Cleanup":
                cleanup_menu()
        except KeyboardInterrupt:
            print("\nBye!")
            break


if __name__ == "__main__":
    main()
