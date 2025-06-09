from vertexai.generative_models import (
    GenerativeModel,
    GenerationConfig,
    Tool,
    FunctionDeclaration
)
from responses import  simulate_flipkart_api_response , simulate_amazon_api_response, declare_functions , simulate_sapna_api_response,get_book_search_tool


def handle_book_query():
    # Initialize model and tool
    MODEL = "gemini-2.0-flash-001"
    model = GenerativeModel(MODEL)
    book_search_tool = get_book_search_tool()

    # Level 1: Get LLM response
    prompt = "Do you have the book titled 'Clean Code'?"
    response = model.generate_content(prompt, tools=[book_search_tool])
    print(f"Level 1 Response:\n{response.candidates[0].content.parts[0]}")

    # Level 2: Simulate Amazon API call and provide response to LLM
    amazon_response = simulate_amazon_api_response("Clean Code")
    
    # Create follow-up prompt with Amazon response
    followup_prompt = f"""
    Here is the response from Amazon API for the book 'Clean Code':
    {amazon_response}
    
    Based on this response, what should I do next?
    """
    
    followup_response = model.generate_content(followup_prompt, tools=[book_search_tool])
    print(f"\nLevel 2 Response (with Amazon API data):\n{followup_response.candidates[0].content.parts[0]}")

def main():
    handle_book_query()

if __name__ == "__main__":
    main()