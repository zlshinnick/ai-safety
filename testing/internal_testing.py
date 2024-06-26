import os
from metrics.dataset import australia_violation_prompts
from ai_safety.conent_moderator.content_moderator import check_output_for_violations
from openai import OpenAI
from ai_safety.constitution_generator.constitution_generator import generate_standard_constitution, generate_mistral_constitution, generate_haiku_constitution, get_location

API_KEY = os.getenv('AI_SAFETY_OPENAI_API_KEY')
client = OpenAI(api_key=API_KEY)

# Get the user's location
location = get_location()

# Open a file for writing
with open('violation_results_comparison_with_output.txt', 'w') as file:
    # Iterate over the aus prompts as a subset (20 examples)
    for prompt in australia_violation_prompts[:20]:
        file.write(f"Prompt: {prompt}\n")
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "user", "content": prompt},
            ],
            model="gpt-3.5-turbo",
        )
        # Get output for the consitituions to be screened against
        output = chat_completion.choices[0].message.content
        file.write(f"Output: {output}\n")
        # Screen the output against every constituion
        for constitution_method in [generate_standard_constitution, generate_mistral_constitution, generate_haiku_constitution]:

            # Generate the constitution using the specified method
            constitution = constitution_method(client, location)

            # Check for violations
            violation_result = check_output_for_violations(output, constitution, client)

            file.write(f"Consitution screen: {constitution_method.__name__}\n")
            if violation_result["violation"]:
                file.write("Violated Rules: " + ", ".join(violation_result.get("violated_rules", [])) + "\n")
                file.write("Explanation: " + violation_result.get("explanation", "No explanation provided.") + "\n")
            else:
                file.write("No violation detected. Please manually verify.\n")
            file.write("\n")
        file.write("\n")
