import ollama

print("1. Ollama Python package imported successfully")

try:
    response = ollama.chat(
        model="llama3.2",
        messages=[
            {
                "role": "user",
                "content": "Reply with exactly: Nivara Ollama test successful"
            }
        ]
    )

    print("2. Ollama connection successful")
    print("3. Model response:")
    print(response["message"]["content"])

except Exception as e:
    print("Ollama test failed")
    print(type(e).__name__)
    print(e)