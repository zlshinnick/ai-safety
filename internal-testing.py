from dataset import australia_constitution
from dataset import australia_violation_prompts 
from assesment import check_output_for_violations
from openai import OpenAI
from constitution import generate_standard_constitution

# iterate over the aus prompts as a subset (20 examples)
# get the output, if there was a violation show the explanation to show the thinking 
# if there was no violation, manually check that there was no violation
# if there was a violation, manually check that the violation was correct

API_KEY = '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'
client = OpenAI(api_key=API_KEY)

# iterate over the aus prompts as a subset (20 examples)
for prompt in australia_violation_prompts[:20]:
    chat_completion = client.chat.completions.create(
        messages = [
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="gpt-3.5-turbo",
    )
    output = chat_completion.choices[0].message.content

    violation_result = check_output_for_violations(output, australia_constitution, client)
    if violation_result["violation"]:
        print("Violated Rules:", violation_result.get("violated_rules", []))
        print("Explanation:", violation_result.get("explanation", "No explanation provided."))
    else:
        print("No violation detected. Please manually verify.")
