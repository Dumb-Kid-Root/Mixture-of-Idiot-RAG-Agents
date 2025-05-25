import os
import time
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv() # Load environment variables from .env file

# Ensure your OPENAI_API_KEY is set as an environment variable
# Example: os.environ["OPENAI_API_KEY"] = "your_openai_api_key_here"
if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("OPENAI_API_KEY environment variable not set.")

client = OpenAI()

# --- Choose your OpenAI models ---
# You can replace these with any other suitable OpenAI models
# For example, "gpt-4", "gpt-4-turbo-preview", etc.
# Consider costs and capabilities when choosing.
reference_models = [
    "gpt-4o-mini",
    "gpt-4.5-preview-2025-02-27",
    "gpt-4o-2024-08-06",
    "gpt-4-turbo-preview", # Retaining one of the more powerful ones
]

aggregator_model = "gpt-4.5-preview" # Or "gpt-4o", "gpt-4"

aggregator_system_prompt = """You have been provided with a set of responses from various AI assistants to the latest user query.
Your task is to synthesize these responses into a single, high-quality response.
It is crucial to critically evaluate the information provided in these responses,
recognizing that some of it may be biased or incorrect.
Your response should not simply replicate the given answers but should offer a refined,
accurate, and comprehensive reply to the instruction.
Ensure your response is well-structured, coherent, and adheres to the highest standards of accuracy and reliability.

Responses from assistants:"""
layers = 1 # OpenAI models are generally strong, 1 layer might be sufficient. Adjust if needed.


def get_final_system_prompt(system_prompt, results):
    """Construct a system prompt for layers 2+ that includes the previous responses to synthesize."""
    return (
        system_prompt
        + "\n\n"
        + "\n".join([f"Assistant {i+1} response: {str(element)}" for i, element in enumerate(results)])
    )


def run_llm(model_name, user_prompt, prev_response_texts=None):
    """Run a single LLM call with an OpenAI model."""
    messages = []
    if prev_response_texts:
        messages.append({
            "role": "system",
            "content": get_final_system_prompt(aggregator_system_prompt, prev_response_texts),
        })
    else:
        # For the first layer (reference models), you might want a simpler system prompt
        # or no specific system prompt beyond the default behavior of the model.
        # For simplicity, we're not adding a distinct one here for reference models.
        pass

    messages.append({"role": "user", "content": user_prompt})

    # Simple retry logic for transient errors
    for attempt in range(3): # Retry up to 3 times
        try:
            response = client.chat.completions.create(
                model=model_name,
                messages=messages,
                temperature=0.7, # Adjusted for potentially more creative synthesis
                max_tokens=1024, # Increased token limit
            )
            print(f"Model: {model_name}, Role: {'Aggregator' if prev_response_texts else 'Reference'}")
            return response.choices[0].message.content
        except Exception as e: # Catching a broader range of exceptions
            print(f"API call to {model_name} failed (attempt {attempt + 1}): {e}")
            if attempt < 2: # If not the last attempt
                time.sleep(2 ** attempt) # Exponential backoff
            else:
                print(f"Failed to get response from {model_name} after multiple retries.")
                return f"Error: Could not get response from {model_name}." # Return an error message

    return f"Error: Could not get response from {model_name} after multiple retries."


def moa_generate(user_prompt):
    """Run the main loop of the MOA process and return the final result."""
    
    # Layer 1: Get responses from reference models
    reference_responses = [run_llm(model, user_prompt) for model in reference_models]
    
    current_results = reference_responses

    # Optional: Intermediate aggregation layers (if layers > 2)
    # For OpenAI, often 1 or 2 layers are sufficient.
    # The original code had 'layers - 1' for the loop, implying at least 2 layers for this loop to run.
    # If layers = 2, this loop runs once for aggregation before the final aggregator.
    # If layers = 1, this loop is skipped.
    for i in range(1, layers -1): # This loop is for intermediate aggregation if layers > 2
        print(f"--- Running Intermediate Aggregation Layer {i+1} ---")
        # In this setup, we could re-use reference models or a specific intermediate aggregator
        # For simplicity, let's re-use the reference models concept for intermediate refinement
        intermediate_aggregated_results = [
            run_llm(model, user_prompt, prev_response_texts=current_results) for model in reference_models
        ]
        current_results = intermediate_aggregated_results

    # Final Aggregation Layer (if layers > 0)
    if layers > 0:
        print("--- Running Final Aggregation Layer ---")
        final_response_content = run_llm(aggregator_model, user_prompt, prev_response_texts=current_results)
    else: # Should not happen if layers is reasonably set
        return "Error: MoA layer count is zero."

    return final_response_content


# Example usage:
if __name__ == "__main__":
    # Make sure OPENAI_API_KEY is set in your environment
    if not os.getenv("OPENAI_API_KEY"):
        print("Please set your OPENAI_API_KEY environment variable to run this example.")
    else:
        # user_prompt = "What are 3 fun things to do in San Francisco?"
        user_prompt = "Explain the concept of a Large Language Model in simple terms."
        print(f"User Prompt: {user_prompt}")
        final_result = moa_generate(user_prompt)
        print("\n--- Final Synthesized Response ---")
        print(final_result) 