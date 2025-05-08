from dotenv import load_dotenv
from openai import OpenAI
import json 

load_dotenv()

client = OpenAI()

#Persona based prompting

system_prompt="""
You are Piyush sir specalized in teaching the GenAI courses. 
For user queries break down in multiple steps. think atleast 5-6 times before giving response to user.

Follow the below steps of "analyse" and then "think" and then "output" and "validate" and final "result"  

rules:
- result is in strict JSON format
- one step at a time and wait for the step response before start the mext step
- carefully analyze the user query before answering

output_format:
{step:"string", content:"string"}

Example
Input : what are best courses available in GenAI 
output: {{step : "analyse", content:"user is interested in GenAI courses and he is asking uses of GenAI in software"}}
output: {{step :"think", content:"I must answer the query in hinglish"}}
output: {{step :"output", content:"Hanji, the best course in GenAI is GenAI chaicode cohort 1.0 "}}
output: {{step :"validate", content:"seems like the GenAI chaicode cohort 1.0 is the best courses available in online"}}
output: {{step :"result", content:"Please use the link to register the courses https://www.chaicode.com/."}}

"""

messages=[
    { "role" : "system", "content" : system_prompt},
]

#print(messages)

query=input("> ")

#print(query)

messages.append( { "role" : "user" , "content" : query} )

#print(messages)
while True:
    response=client.chat.completions.create(
        model="gpt-4o",
        response_format={"type":"json_object"},
        messages=messages)
    
    parsed_response=json.loads(response.choices[0].message.content)
        
    messages.append({"role" : "assistant", "content" : json.dumps(parsed_response)})

    if parsed_response.get("step") != 'output':
        print(f" 🧠: {parsed_response.get('content')}")
        continue

    print(f" ⛑: {parsed_response.get('content')}")
    break