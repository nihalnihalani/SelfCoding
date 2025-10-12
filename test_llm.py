#!/usr/bin/env python3
"""
Test LLM integration directly
"""

import os
import asyncio
from emergentintegrations.llm.chat import LlmChat, UserMessage

async def test_llm():
    try:
        # Load environment
        from dotenv import load_dotenv
        load_dotenv('/app/backend/.env')
        
        api_key = os.getenv('EMERGENT_LLM_KEY')
        print(f"API Key present: {'Yes' if api_key else 'No'}")
        
        if not api_key:
            print("❌ No API key found")
            return False
        
        print("Testing LLM connection...")
        
        chat = LlmChat(
            api_key=api_key,
            session_id="test_session",
            system_message="You are a helpful assistant."
        ).with_model("gemini", "gemini-2.5-flash")
        
        print("Sending test message...")
        response = await chat.send_message(UserMessage(text="Say 'Hello World' in JSON format"))
        
        print(f"✅ LLM Response: {response[:100]}...")
        return True
        
    except Exception as e:
        print(f"❌ LLM Error: {str(e)}")
        return False

if __name__ == "__main__":
    result = asyncio.run(test_llm())
    print(f"LLM Test {'Passed' if result else 'Failed'}")