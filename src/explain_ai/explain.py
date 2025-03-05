from typing import Any
import inspect
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import SystemMessage, HumanMessage


class ExplainAI:
    """
    A class that uses LangChain with Google Gemini Flash 2.0 (or another specified model)
    to explain native Python objects.
    """

    def __init__(self, api_key: str, model_name: str = "gemini-2.0-flash"):
        """
        Initialize the ExplainAI object with an API key and model name.

        :param api_key: API key for Google Gemini AI.
        :param model_name: The model name to use (default: "gemini-2.0-flash").
        """
        self.api_key = api_key
        self.model_name = model_name
        self.llm = ChatGoogleGenerativeAI(
            model=self.model_name, google_api_key=self.api_key)

    def _object_to_text(self, obj: Any) -> str:
        """
        Convert a Python object to a detailed string representation suitable for sending to an LLM.

        :param obj: Any native Python object.
        :return: String representation of the object.
        """
        info = []
        info.append(f"Type: {type(obj).__name__}")

        if isinstance(obj, (int, float, bool, str)):
            info.append(f"Value: {repr(obj)}")

        if isinstance(obj, list):
            info.append(f"List with {len(obj)} elements: {obj[:5]}..." if len(
                obj) > 5 else f"List: {obj}")

        if isinstance(obj, dict):
            keys_sample = list(obj.keys())[:5]
            info.append(
                f"Dictionary with {len(obj)} keys. Sample keys: {keys_sample}")

        if hasattr(obj, "__dict__"):
            info.append(
                f"Instance of {obj.__class__.__name__} with attributes: {vars(obj)}")

        info.append(f"Module: {getattr(obj, '__module__', 'Unknown')}")
        info.append(f"Class: {getattr(obj, '__class__', 'Unknown')}")
        info.append(
            f"Base Classes: {getattr(obj.__class__, '__bases__', 'Unknown')}")
        info.append(
            f"Has __dict__ attribute: {'Yes' if hasattr(obj, '__dict__') else 'No'}")
        info.append(
            f"Has __doc__: {'Yes' if hasattr(obj, '__doc__') else 'No'}")

        methods_and_attrs = dir(obj)
        info.append(f"Available Attributes & Methods: {methods_and_attrs[:10]}..." if len(
            methods_and_attrs) > 10 else f"Available Attributes & Methods: {methods_and_attrs}")

        docstring = inspect.getdoc(obj)
        if docstring:
            # Limit to first 200 chars
            info.append(f"Docstring: {docstring[:200]}...")
        print(info)
        return "\n".join(info)

    def explain(self, obj: Any) -> str:
        """
        Generate an explanation of the given object using LangChain with Gemini Flash 2.0.

        :param obj: Any native Python object.
        :return: Explanation of the object.
        """
        obj_text = self._object_to_text(obj)

        messages = [
            SystemMessage(
                content='''

                You are an AI that explains anything interesting about the Python object given to you.
                Give back only intereresting and informative information about the object
                Do not talk about the functions it has but rather the interesting information about the object. Discuss it's content.
                If feasible try to visualize it's content.
                '''),
            HumanMessage(
                content=f"Explain the following Python object:\n\n{obj_text}\n\n")
        ]

        response = self.llm(messages)

        return response.content.strip() if response and response.content else "Failed to generate an explanation."
