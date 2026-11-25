"""
Entry point for all four parts of the weather station.
The role is passed as the first argument: server, pi4, zero or ui.
Without an argument the Streamlit UI starts, so `streamlit run main.py` keeps working.
"""
import sys

ROLES = ("server", "pi4", "zero", "ui")


def main(role: str) -> None:
    """Starts the program for the given role."""
    match role:
        case "pi4":
            from pi4.pi4_main import pi4_main
            pi4_main()
        case "server":
            from server_pi3.server_main import server_main
            server_main()
        case "zero":
            from pi_zero.zero_main import zero_main
            zero_main()
        case "ui":
            from ui.app import app
            app()
        case _:
            sys.exit(f"Unknown role '{role}'. Use one of: {', '.join(ROLES)}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "ui")
