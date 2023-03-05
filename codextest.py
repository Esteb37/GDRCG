import os
import openai
import re
import sys

openai.api_key = os.getenv("OPENAI_API_KEY")

CONTEXT = ""
with open("Robot.py", "r", encoding="utf_8") as f:
    CONTEXT = f.read().replace(
        "\n", "\n    ")

CONTENT = f"""
{CONTEXT}

        # [PROMPT]
"""


def get_undefined_functions(text: str) -> str:
    # split text by all non-alphanumeric characters
    referenced_pattern = r'self\.(\w+)\('
    referenced = re.findall(referenced_pattern, text)

    defined_pattern = r'def (\w+)\('
    defined = re.findall(defined_pattern, text)

    return set(referenced) - set(defined)


def get_undefined_constants(text: str) -> str:
    # split text by all non-alphanumeric characters
    referenced_pattern = r'self\.(\w+)'
    referenced = re.findall(referenced_pattern, text)

    defined_pattern = r'(\w+) = '
    defined = re.findall(defined_pattern, text)

    return set(referenced) - set(defined)


def get_added_text(original: str, new: str):
    # Find the chunk of text that was added
    original_lines = original.split("\n")
    new_lines = new.split("\n")

    for i in range(len(original_lines)):
        if original_lines[i] != new_lines[i]:
            return "\n".join(new_lines[i:])


def get_completion(prompt: str):
    for resp in openai.Completion.create(
        model="code-davinci-002",
        prompt=prompt,
        max_tokens=4000,
        temperature=0.0,
        echo=True,
        stop=["# Executes the "],
        frequency_penalty=0.0,
        presence_penalty=0.0,
        stream=True,
    ):
        if resp != "[DONE]":
            sys.stdout.write(resp.choices[0].text)
            sys.stdout.flush()
        else:
            result = resp

    return result.choices[0].text


def main():
    while True:
        # input("Enter your prompt: ")
        prompt = "Read the quadrature encoder values and calculate distance travelled"

        full_prompt = CONTENT.replace("[PROMPT]", prompt)

        print("Generating response...")

        new_text = get_completion(full_prompt)

        code = get_added_text(CONTEXT, new_text)

        print("Generated code:")
        print(code)

        undefined_function_names = get_undefined_functions(new_text)

        completed_functions = False

        for function_name in undefined_function_names:
            print("Completing for " + function_name+"... ")

            completed_functions = True

            additional_prompt = new_text + \
                "\n        def " + function_name+"(self"

            response = get_completion(additional_prompt)
            code = get_added_text(new_text, response)
            new_text = response

        if completed_functions:
            print("Completed context: ")
            print(new_text)

        undefined_constant_names = get_undefined_constants(new_text)

        print("Undefined constants: ")
        print(undefined_constant_names)


if __name__ == "__main__":
    main()
