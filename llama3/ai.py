import json
import aiohttp
import asyncio
import random

async def x_inst() -> str:
    with open("llama3/x_inst.md", "r", encoding="utf-8") as f:
        return f.read()
    
async def linkedin_inst() -> str:
    with open("llama3/linkedin_inst.md", "r", encoding="utf-8") as f:
        return f.read()
    
async def discord_announcement_inst() -> str:
    with open("llama3/disc_inst.md", "r", encoding="utf-8") as f:
        return f.read()

async def daily_announcement_inst() -> str:
    with open("llama3/daily_task.md", "r", encoding="utf-8") as f:
        return f.read()
    
async def random_words(file_path: str, count: int) -> str:
    # Read all words from file
    with open(file_path, "r", encoding="utf-8") as f:
        words = [line.strip() for line in f if line.strip()]

    # Ensure we have enough unique words
    if count > len(words):
        raise ValueError("Not enough unique words in the file.")

    # Randomly pick unique words
    return "\n".join(random.sample(words, count))

async def ai_call(instructions: str, prompt: str | None=None) -> str:
    full_response = instructions + "\n\n" + prompt if prompt else instructions


    async with aiohttp.ClientSession() as session:
        async with session.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3",
                "prompt": full_response,
                "stream": True,
                "temperature": 0.7,
                "top_p": 0.9,
                "top_k": 40,
                "repeat_penalty": 1.1,
                "num_predict": 200,
                "stream": True
            }
        ) as response:
            full_response = ""
            
            async for line in response.content:
                if line:
                    data = json.loads(line.decode("utf-8"))
                    full_response += data.get("response", "")
    return full_response

async def main():
    user_input = input("Enter your prompt: ")
    instructions = await x_inst()
    answer = await ai_call(instructions, user_input)
    print("AI Response:", answer)

if __name__ == "__main__":
    asyncio.run(main())