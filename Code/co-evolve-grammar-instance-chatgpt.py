import openai
import time

# Set OpenAI API key
openai.api_key = ""

# File paths
grammar_a_file = "Code\\Case_Languages\\CheckerDSL\\grammar_1_20150503_55911bf.txt"
grammar_b_file = "Code\\Case_Languages\\CheckerDSL\\grammar_2_20150727_3fa6e6d.txt"
instance_a_file = "Code\\Case_Languages\\CheckerDSL\\instance_1_20250503_55911bf.txt"

# Read the content of a file
def read_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()

# Load grammar 1, grammar 2, and instance 1
grammar_1 = read_file(grammar_a_file)
grammar_2 = read_file(grammar_b_file)
instance_1 = read_file(instance_a_file)

# Initialize the messages list for chain-of-thought prompting
messages = []

# Step 1: Send Grammar 1
messages.append({"role": "system", "content": "You are a helpful assistant."})
messages.append({
    "role": "user",
    "content": f"Here is the initial version of the grammar (Grammar 1). Please remember this for future reference:\n\n{grammar_1}"
})

# Call OpenAI API to confirm understanding
response = openai.ChatCompletion.create(model="gpt-4o", messages=messages, max_tokens=200)
# print("Response after Grammar 1:", response["choices"][0]["message"]["content"])

# Step 2: Send Grammar 2
messages.append({
    "role": "user",
    "content": f"Here is the updated version of the grammar (Grammar 2). Please remember this and analyze the differences from Grammar 1:\n\n{grammar_2}"
})

response = openai.ChatCompletion.create(model="gpt-4o", messages=messages, max_tokens=200)
# print("Response after Grammar 2:", response["choices"][0]["message"]["content"])

# Step 3: Send Instance 1
messages.append({
    "role": "user",
    "content": f"Here is an instance of Grammar 1 (Instance 1). Please remember this for future reference:\n\n{instance_1}"
})

# time.sleep(15)
response = openai.ChatCompletion.create(model="gpt-4o", messages=messages, max_tokens=1000)
print("Response after Instance 1:", response["choices"][0]["message"]["content"])

# Step 4: Add final instructions
final_prompt = """
    grammar_1 is the initial grammar of the DSL, we evolved it to get grammar_2, and instance_1 was originally a text instance that followed grammar_1. 
        Now I want you to analyze the differences between the two versions of the grammar, and based on this difference, modify instance_1 and get instance_2, which will follow grammar_2. 
        And please note the following things:
        1. When evolve the instance, please don't forget the symbol which is enclosed by single quotes.
        2. If grammar_2 add a new grammar rule or a new attribute which is optional or in an “OR” relationship (i.e., |), then please don’t instantiate it.
        3. Don’t miss or add any formats in the instance, e.g., comments, formats (white-space, indents, tabs, empty lines, etc.). 

"""
messages.append({"role": "user", "content": final_prompt})
# time.sleep(20)

# Call OpenAI API to generate Instance 2
response = openai.ChatCompletion.create(
    model="gpt-4o",
    messages=messages,
    max_tokens=1500
)
instance_2 = response["choices"][0]["message"]["content"].strip()

# # Print the result
# print("Generated Instance 2:")
# print(instance_2)

# Save the result to a file
with open("Code\\Case_Languages\\CheckerDSL\\instance_2_gen_openai_10.txt", "w", encoding="utf-8") as file:
    file.write(instance_2)

print("\nInstance 2 has been saved to 'Code\\Case_Languages\\CheckerDSL\\instance_2_gen_openai_10.txt'.")
