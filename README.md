# explain-ai

A Python package that uses LLMs to explain **any Python objects**, including:

- Lists, Dictionaries
- Custom Python Classes
- Pandas Dataframes
- Numpy Arrays


## Installation

```bash
pip install explain-ai
```

## Usage

```python
from explain_ai import ExplainAI

api_key = "YOUR_GEMINI_API_KEY"

# Initialize the AI explainer
ai_explainer = ExplainAI(api_key)

# Example 1: Explain an integer
print(ai_explainer.explain_object(42))

# Example 2: Explain a list
print(ai_explainer.explain_object([1, 2, 3, 4, 5]))

# Example 3: Explain a dictionary
print(ai_explainer.explain_object({"name": "Alice", "age": 30}))

# Example 4: Explain a custom class
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

person = Person("Alice", 30)
print(ai_explainer.explain_object(person))
```

## How It Works

1. Install the package and the required dependencies (Google Gemini AI).
2. Instantiate the `ExplainAI` class with your Gemini API key (and an optional model engine, default is `gemini-flash-2`).
3. Call the `explain_object` method with a native Python object.
4. The package converts your object into a text description and sends it to Google Gemini, which returns a succinct explanation.

## Contributing

1. Fork the repo on GitHub.
2. Create a new branch for your feature or bugfix.
3. Commit and push your changes.
4. Submit a pull request.
