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
    prompt = "Do you have the book titled 'Programming'?"

    response = model.generate_content(prompt, tools=[book_search_tool])
    print(f"Level 1 Response:\n{response.candidates[0].content.parts[0]}")

    amazon_response = simulate_amazon_api_response("Programming")
    followup_prompt = f"""
    Here is the response from Amazon API for the book 'Programming':
    {amazon_response}
    
    Based on this response, what should I do next?
    """
    followup_response = model.generate_content(followup_prompt, tools=[book_search_tool])
    print(f"\nLevel 2 Response (with Amazon API data):\n{followup_response.candidates[0].content.parts[0]}")

    if amazon_response["status"] == "not_found":
        enhanced_prompt = f"""
        Here is the response from Amazon API for the book 'Programming':
        {amazon_response}
        
        Since Amazon does not have the book, what should I do next? 
        Remember: If Amazon doesn't have the book, you should tell me to check Flipkart next.
        """
        enhanced_response = model.generate_content(enhanced_prompt, tools=[book_search_tool])
        print(f"\nLevel 3 Response (Enhanced with Flipkart suggestion):\n{enhanced_response.candidates[0].content.parts[0]}")

        flipkart_response = simulate_flipkart_api_response("Programming")
        flipkart_prompt = f"""
        Here is the response from Flipkart API for the book 'Programming':
        {flipkart_response}
        
        Based on this Flipkart response, what should I do next?
        """
        flipkart_llm_response = model.generate_content(flipkart_prompt, tools=[book_search_tool])
        print(f"\nLevel 4 Response (with Flipkart API data):\n{flipkart_llm_response.candidates[0].content.parts[0]}")

        if flipkart_response["status"] == "not_found":
            sapna_suggestion_prompt = f"""
            Here are the responses from both Amazon and Flipkart APIs for the book 'Regional Coding Patterns':
            
            Amazon Response: {amazon_response}
            Flipkart Response: {flipkart_response}
            
            Since both Amazon and Flipkart do not have the book, what should I do next?
            Remember: If both Amazon and Flipkart don't have the book, you should tell me to check Sapna next.
            """
            sapna_suggestion_response = model.generate_content(sapna_suggestion_prompt, tools=[book_search_tool])
            print(f"\nLevel 5 Response (Enhanced with Sapna suggestion):\n{sapna_suggestion_response.candidates[0].content.parts[0]}")

            sapna_response = simulate_sapna_api_response("Regional Coding Patterns")
            if sapna_response["status"] == "found":
                final_prompt = f"""
                Here is the response from Sapna API for the book 'Regional Coding Patterns':
                {sapna_response}
                
                Great! Sapna has the book. What should I recommend to the user?
                Remember: If Sapna has the book, you should suggest getting it from Sapna.
                """
            else:
                final_prompt = f"""
                Here are the responses from all three stores for the book 'Regional Coding Patterns':
                
                Amazon Response: {amazon_response}
                Flipkart Response: {flipkart_response}
                Sapna Response: {sapna_response}
                
                None of the stores have the book. What alternatives should I suggest?
                Remember: If none have the book, suggest alternatives like notify when available, try used book sites, etc.
                """
            final_response = model.generate_content(final_prompt, tools=[book_search_tool])
            print(f"\nLevel 6 Response (Final recommendation with Sapna API data):\n{final_response.candidates[0].content.parts[0]}")
        else:
            print(f"\nLevel 5: Book found on Flipkart, no need to check Sapna")
            print(f"Level 6: Skipping Sapna API call as book was found on Flipkart")
    else:
        print(f"\nLevel 3: Book found on Amazon, no need to check Flipkart")
        print(f"Level 4: Skipping Flipkart API call as book was found on Amazon")
        print(f"Level 5: Skipping Sapna suggestion as book was found on Amazon")
        print(f"Level 6: Skipping Sapna API call as book was found on Amazon")


def main():
    handle_book_lookup()

if __name__ == "__main__":
    main()