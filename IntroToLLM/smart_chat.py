from smart_agent import SmartAgent

smart_agent = SmartAgent("gemma3:1b")

question = input("Enter your question: ").strip()
while question != "/pa":
    if question != "":
        answer_text = smart_agent.chat(question)
        print(answer_text)
    question = input("Enter your question: ").strip()