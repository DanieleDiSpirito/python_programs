from classes import Main

if __name__ == "__main__":
    main = Main()
    main.start()
    print("STARTING SIMULATION:")
    main.print_nodes()
    print("=" * 50)
    main.make_transaction()
    main.print_nodes()
