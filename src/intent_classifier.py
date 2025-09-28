def classify_intent(text):
    text = text.lower()
    if any(kw in text for kw in ["where is", "go to", "navigate", "direction"]):
        return "navigate"
    elif any(kw in text for kw in ["tell me", "what is", "who is", "explain", "describe"]):
        return "ask"
    elif any(kw in text for kw in ["compare", "difference", "vs", "versus"]):
        return "compare"
    elif any(kw in text for kw in ["kids", "children", "child", "simple", "easy"]):
        return "kid_mode"
    else:
        return "unknown"
