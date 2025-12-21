from aikeys import geminikey
from google import genai
from google.genai import types
import requests

client = genai.Client(api_key =  geminikey)

def get_weather(city_name:str):
    url = f"https://wttr.in/{city_name}?format=%c+%t"
    return requests.get(url).text.strip()

tools = [get_weather]

fn_registry = {
    "get_weather": get_weather
}
system_prompt = """
  You are a helpful and friendly weather assistant named Dora.

Your job is to answer weather-related questions only.
If the user asks a non-weather question, politely refuse and redirect them back to weather topics.

When a user asks about the weather for a location:
- Identify the city clearly.
- Use the available weather tool to fetch data when needed.
- Do not guess weather information.
- Use the tool result to form your answer.

Respond in clear, simple language that a normal user can understand.
If information is missing or the question is unclear, ask a short follow-up question.


Example :
user: What's the weather like in Paris today?
Assistant: The current weather in Paris is sunny with a temperature of 25°C

"""
print("Hi there! I'm Dora, your friendly assistant. How can I help you today")

chat = client.chats.create(
    model = "gemini-2.5-flash",
    config = types.GenerateContentConfig(
        system_instruction = (
           system_prompt
        ),

        tools = tools,
        temperature=0.3,

    )
)

while True:
    user_input = input("\n> ")
    response = chat.send_message(user_input)

    #The New SDK stores calls in candidates[0].content.parts
    for part in response.candidates[0].content.parts:
        if part.function_call:
            fn = part.function_call
            # Run the actual Python function
            result = fn_registry[fn.name](**fn.args)
            
            # SEND BACK: Tell Gemini the result so it can talk to the user
            # We use send_message again with a special 'FunctionResponse' part
            final_response = chat.send_message(
                types.Part.from_function_response(
                    name=fn.name,
                    response={'result': result}
                )
            )
            print("\nDora:", final_response.text)
        elif part.text:
            print("\nDora:", part.text)
"""
    if response.tool_calls:
        tool_call = response.tool_calls[0]
        fn_name = tool_call.name
        fn_args = tool_call.args 
        
        if fn_name in fn_registry:
            fn_respose = fn_registry[fn_name](**fn_args)
            chat.send_tool_response(tool_call, fn_respose)
        
        else :
            chat.send_tool_response(tool_call, "Function not implemented.")
    
    print("\nDora:", response.content)"""
