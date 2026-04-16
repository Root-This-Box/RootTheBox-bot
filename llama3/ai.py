import json
import aiohttp
import asyncio

async def x_inst() -> str:
    with open("llama3/x_inst.md", "r", encoding="utf-8") as f:
        return f.read()
    
async def linkedin_inst() -> str:
    with open("llama3/linkedin_inst.md", "r", encoding="utf-8") as f:
        return f.read()

async def ai_call(instructions: str, prompt: str) -> str:
    full_response = instructions + "\n\n" + prompt


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