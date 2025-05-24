
def main():
    #program = "server_main"
    #program = "pi4_main"
    #program = "zero_main"
    program = "ui_main"

    match program:
        case "pi4_main":
            from pi4.pi4_main import pi4_main
            pi4_main()
        case "server_main":
            from server_pi3.server_main import server_main
            server_main()
        case "zero_main":
            from pi_zero.zero_main import zero_main
            zero_main()
        case "ui_main":
            from ui.app import app
            app()
        case _:
            print("Program not found")

if __name__ == "__main__":
    main()




