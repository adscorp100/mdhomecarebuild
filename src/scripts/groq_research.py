#!/usr/bin/env python3
"""
Groq Research Script
A simple research tool using Groq's compound-beta-mini model.
"""

import os
import sys
from groq import Groq
from dotenv import load_dotenv

def load_api_key():
    """Load the Groq API key from environment variables."""
    # Load environment variables from .env file
    load_dotenv()
    
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("❌ Error: GROQ_API_KEY not found in environment variables.")
        print("Please add your Groq API key to the .env file:")
        print("GROQ_API_KEY=your_api_key_here")
        sys.exit(1)
    
    return api_key

def research_query(prompt, model="compound-beta-mini", temperature=1, max_tokens=1024):
    """
    Send a research query to Groq and stream the response.
    
    Args:
        prompt (str): The research question/prompt
        model (str): The Groq model to use
        temperature (float): Creativity level (0-2)
        max_tokens (int): Maximum response length
    """
    try:
        # Initialize Groq client
        client = Groq(api_key=load_api_key())
        
        print(f"🔍 Researching: {prompt}")
        print("=" * 60)
        
        # Create completion with streaming
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=temperature,
            max_completion_tokens=max_tokens,
            top_p=1,
            stream=True,
            stop=None,
        )

        # Stream the response
        response_text = ""
        for chunk in completion:
            content = chunk.choices[0].delta.content or ""
            print(content, end="", flush=True)
            response_text += content
        
        print("\n" + "=" * 60)
        return response_text
        
    except Exception as e:
        print(f"❌ Error during research: {e}")
        return None

def interactive_mode():
    """Run the script in interactive mode."""
    print("🧠 Groq Research Assistant")
    print("Type your research questions. Type 'quit' or 'exit' to stop.")
    print("-" * 60)
    
    while True:
        try:
            prompt = input("\n📝 Enter your research prompt: ").strip()
            
            if prompt.lower() in ['quit', 'exit', 'q']:
                print("👋 Goodbye!")
                break
            
            if not prompt:
                print("Please enter a research prompt.")
                continue
            
            research_query(prompt)
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except EOFError:
            print("\n👋 Goodbye!")
            break

def main():
    """Main function to handle command line arguments."""
    if len(sys.argv) > 1:
        # Single query mode
        prompt = " ".join(sys.argv[1:])
        research_query(prompt)
    else:
        # Interactive mode
        interactive_mode()

if __name__ == "__main__":
    main() 