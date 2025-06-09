from vertexai.generative_models import (
    GenerativeModel,
    GenerationConfig,
    Tool,
    FunctionDeclaration
)
from responses import  simulate_flipkart_api_response , simulate_amazon_api_response, declare_functions , simulate_sapna_api_response,get_book_search_tool



def handle_book_lookup():
    MODEL = "gemini-2.0-flash-001"
    model = GenerativeModel(MODEL)
    book_search_tool = get_book_search_tool()
    prompt = "Do you have the book titled 'Let Us C'?"

    response = model.generate_content(prompt, tools=[book_search_tool])
    print(f"Level 1 Response:\n{response.candidates[0].content.parts[0]}")

    amazon_response = simulate_amazon_api_response("Let Us C")
    followup_prompt = f"""
    Here is the response from Amazon API for the book 'Let Us C':
    {amazon_response}
    
    Based on this response, what should I do next?
    """
    followup_response = model.generate_content(followup_prompt, tools=[book_search_tool])
    print(f"\nLevel 2 Response (with Amazon API data):\n{followup_response.candidates[0].content.parts[0]}")

    if amazon_response["status"] == "not_found":
        enhanced_prompt = f"""
        Here is the response from Amazon API for the book 'Let Us C':
        {amazon_response}
        
        Since Amazon does not have the book, what should I do next? 
        Remember: If Amazon doesn't have the book, you should tell me to check Flipkart next.
        """
        enhanced_response = model.generate_content(enhanced_prompt, tools=[book_search_tool])
        print(f"\nLevel 3 Response (Enhanced with Flipkart suggestion):\n{enhanced_response.candidates[0].content.parts[0]}")

        flipkart_response = simulate_flipkart_api_response("Let Us C")
        flipkart_prompt = f"""
        Here is the response from Flipkart API for the book 'Let Us C':
        {flipkart_response}
        
        Based on this Flipkart response, what should I do next?
        """
        flipkart_llm_response = model.generate_content(flipkart_prompt, tools=[book_search_tool])
        print(f"\nLevel 4 Response (with Flipkart API data):\n{flipkart_llm_response.candidates[0].content.parts[0]}")

        if flipkart_response["status"] == "not_found":
            sapna_suggestion_prompt = f"""
            Here are the responses from both Amazon and Flipkart APIs for the book 'Let Us C':
            
            Amazon Response: {amazon_response}
            Flipkart Response: {flipkart_response}
            
            Since both Amazon and Flipkart do not have the book, what should I do next?
            Remember: If both Amazon and Flipkart don't have the book, you should tell me to check Sapna next.
            """
            sapna_suggestion_response = model.generate_content(sapna_suggestion_prompt, tools=[book_search_tool])
            print(f"\nLevel 5 Response (Enhanced with Sapna suggestion):\n{sapna_suggestion_response.candidates[0].content.parts[0]}")
        else:
            print(f"\nLevel 5: Book found on Flipkart, no need to check Sapna")
    else:
        print(f"\nLevel 3: Book found on Amazon, no need to check Flipkart")
        print(f"Level 4: Skipping Flipkart API call as book was found on Amazon")
        print(f"Level 5: Skipping Sapna suggestion as book was found on Amazon")


def main():
    handle_book_lookup()

if __name__ == "__main__":
    main()