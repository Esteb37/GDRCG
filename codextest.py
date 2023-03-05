import os
import openai


openai.api_key = os.getenv("OPENAI_API_KEY")

CONTEXT = open("context.txt", "r").read().replace("\n", "\n    ")

CONTENT = f"""{CONTEXT}

    # Executes the "[PROMPT]" command
"""


def get_undefined(text, CONTEXT):
    # Get the functions that are referenced in the text but not defined in the context

    # Find functions that are referenced in the text as self.function_name()
    text_lines = text.split("\n")
    text_lines = [
        line for line in text_lines if line.strip().startswith("self.")]
    function_names = [line.split("self.")[1].split("(")[0]
                      for line in text_lines]

    # Find functions that are defined in the context
    context_lines = CONTEXT.split("\n")
    context_lines = [
        line for line in context_lines if line.strip().startswith("def ")]
    context_function_names = [line.split("def ")[1].split(
        "(")[0] for line in context_lines]

    # Get the difference between the two
    undefined_function_names = set(function_names) - \
        set(context_function_names)

    return undefined_function_names


def get_undefined_constants(text, CONTEXT):
    # Get the constants that are referenced in the text but not defined in the context

    # Find constants that are referenced in the text as self.CONSTANT
    text_lines = text.split("\n")
    text_lines = [
        line for line in text_lines if line.strip().startswith("self.")]
    constant_names = [line.split("self.")[1].split(" ")[0]
                      for line in text_lines]

    # Find constants that are defined in the context
    context_lines = CONTEXT.split("\n")
    context_lines = [line for line in context_lines if line.endswith("=")]
    context_constant_names = [line.split(" ")[-1]
                              for line in context_lines]

    # Get the difference between the two
    undefined_constant_names = set(constant_names) - \
        set(context_constant_names)

    return undefined_constant_names


while True:
    prompt = input("Enter your prompt: ")

    full_prompt = CONTENT.replace("[PROMPT]", prompt)

    print("Generating response...")
    response = openai.Completion.create(
        engine="code-davinci-002",
        prompt=full_prompt,
        max_tokens=1000,
        temperature=0.2,
        stop=["# Executes the"]
    )

    response_text = response.choices[0].text

    # Get the actual code that was generated
    lines = response_text.split("\n")
    for i in range(len(lines)):
        if lines[i].startswith(f"# Executes the \"{prompt}\" command"):
            lines = lines[i+1:]
            break
    code = "\n".join(lines)

    print("Response:")
    print(code)

    # Complete for the functions that are undefined
    undefined_function_names = get_undefined(response_text, CONTEXT)
    for function_name in undefined_function_names:
        additional_prompt = CONTEXT + "\n\tdef " + function_name
        print("Completing for " + function_name+"... ")
        response = openai.Completion.create(
            engine="code-davinci-002",
            prompt=full_prompt,
            max_tokens=1000,
            temperature=0.2,
            stop=["# Executes the"]
        )

    # Ask for the constants that are undefined
    undefined_constant_names = get_undefined_constants(response_text, CONTEXT)
    for constant_name in undefined_constant_names:
        constant_value = input("What is the value of " + constant_name + "? ")

        # Add it to the context under "# Constants"
        context_lines = CONTEXT.split("\n")
        for i in range(len(context_lines)):
            if context_lines[i].startswith("# Constants"):
                context_lines.insert(
                    i+1, f"\t{constant_name} = {constant_value}")
                break
        CONTEXT = "\n".join(context_lines)
