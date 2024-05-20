import enum
import openai
from dotenv import dotenv_values
import argparse
from colorama import init as colorama_init
from colorama import Fore, Style

CONFIG = dotenv_values(".env")

openai.api_key = CONFIG["OPENAI_API_KEY"]

colorama_init()

def create_personality():
    parser = argparse.ArgumentParser(description="This is a conversational chatbot..")
    parser.add_argument("-p","--personality",type=str,help="provide a personality like rude and sarcastic",default="kind andf helpful")

    args = parser.parse_args()
    return args.personality

def chatbot(initial_prompt):

    messages = [{
        "role":"system",
        "content": initial_prompt
    }]
    while True:
        try:
            user_input = input(Style.BRIGHT +  Fore.RED  + "You: " + Style.RESET_ALL + Fore.RESET)
            messages.append(                    {
                        "role":"user",
                        "content": user_input
                    })
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                stream=True
            )
            response_content = ""
            print(Style.BRIGHT + Fore.CYAN + "bot: " + Style.RESET_ALL + Fore.RESET, end="")
            for resp in response: 
                if resp.choices[0].delta.content != None:
                    print(resp.choices[0].delta.content,end="",flush=True)
                    response_content += resp.choices[0].delta.content
            
            messages.append({
                "role":"assistant",
                "content": response_content
            })
            print()
        except KeyboardInterrupt:
            print("Exiting...")
            break




def main():
    chatbot(create_personality())



if __name__ == "__main__":
    main()