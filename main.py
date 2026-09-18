from agent import Agent

def main():
    agent = Agent()
    print("Datazoic Scalable Agentic System — demo (mock APIs only)")
    print("Type 'exit' to quit.")
    while True:
        try:
            message = input("\nYou: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break
        if message.lower() in {"exit", "quit"}:
            print("Goodbye!")
            break
        if message:
            print("Agent:", agent.handle(message))

if __name__ == "__main__":
    main()
