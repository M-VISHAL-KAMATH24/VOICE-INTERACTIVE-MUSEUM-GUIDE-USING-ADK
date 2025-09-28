from src.intent_classifier import classify_intent

personas = {
    "ask": lambda q: "Here's some info about that exhibit.",
    "navigate": lambda q: "Heading to the space gallery.",
    "compare": lambda q: "Monet and Renoir had distinct styles. Here are the details...",
    "kid_mode": lambda q: "This is a fun and simple explanation for kids.",
    "unknown": lambda q: "Sorry, I didn't understand. Can you rephrase?"
}

def route_to_persona(text):
    intent = classify_intent(text)
    response = personas.get(intent, personas["unknown"])(text)
    return intent, response
