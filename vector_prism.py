import os
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv() # Load environment variables from .env file

# Default model is "text-embedding-ada-002"
# Make sure to set your OPENAI_API_KEY environment variable.

def embedding_function():
    # Example: os.environ["OPENAI_API_KEY"] = "your_openai_api_key_here"
    # It's recommended to set this in your system's environment variables
    # or use a .env file with a library like python-dotenv.
    if not os.getenv("OPENAI_API_KEY"):
        raise ValueError("OPENAI_API_KEY environment variable not set.")
    
    embeddings = OpenAIEmbeddings()
    return embeddings

# Example usage (optional, for testing):
if __name__ == '__main__':
    # This is a basic test to ensure the function can be called
    # and an embeddings object is created.
    # For a real test, you would need to have OPENAI_API_KEY set.
    try:
        # Attempt to initialize, will fail if OPENAI_API_KEY is not set
        # but will show the structure is okay.
        if os.getenv("OPENAI_API_KEY"):
            emb_func = embedding_function()
            print("OpenAIEmbeddings object created successfully.")
            # You could add a small test embedding here if needed
            # test_embedding = emb_func.embed_query("Hello, world!")
            # print(f"Test embedding (first 5 dimensions): {test_embedding[:5]}")
        else:
            print("OPENAI_API_KEY not set. Skipping full embedding function test.")
            # Test instantiation without API call
            embeddings = OpenAIEmbeddings(api_key="test_key_just_for_instantiation")
            print("OpenAIEmbeddings can be instantiated (without making API calls).")

    except Exception as e:
        print(f"Error in embedding function test: {e}") 