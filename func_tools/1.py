from vertexai.generative_models import (
    GenerativeModel,
    GenerationConfig,
    Tool,
    FunctionDeclaration
)
from responses import  simulate_flipkart_api_response , simulate_amazon_api_response, declare_functions , simulate_sapna_api_response,get_book_search_tool

def handle_book_query():
    MODEL = "gemini-2.0-flash-001"
    model = GenerativeModel(MODEL)
    book_search_tool = get_book_search_tool()
    prompt = "Do you have the book titled 'Let Us C'?"
    response = model.generate_content(prompt, tools=[book_search_tool])
    print(f"Response:\n{response.candidates[0].content.parts[0]}")


def main():
    handle_book_query()

if __name__ == "__main__":
    main()