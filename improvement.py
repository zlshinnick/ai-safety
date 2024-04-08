def recursive_improve(client, constitution, model_output, max_attempts=5):
    attempts = 0
    while attempts < max_attempts:
        request_data = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {
                    "role": "system",
                    "content": "Given the following constitution and an output based on a user prompt, identify any violations in the output. Rewrite the output to comply with the constitution while avoiding any violations. If there are no violations, state that the output is compliant."
                },
                {
                    "role": "user",
                    "content": f"Constitution:\n{constitution}"
                },
                {
                    "role": "user",
                    "content": f"Output:\n{model_output}"
                },
                {
                    "role": "user",
                    "content": "Rewrite the output to comply with the constitution while avoiding any violations. If the output violates any rules, revise it to ensure compliance without directly or indirectly breaching the constitution. If there are no violations, keep the response the same but append the phrase 'no violation' at the end."
                }
            ]
        }
        response = client.chat.completions.create(**request_data)
        response_content = response.choices[0].message.content

        if "no violations" in response_content.lower():
            return model_output
        else:
            # Update the model_output with the corrected output
            model_output = response_content

        attempts += 1

    # If the loop exits without finding a compliant output, return the last attempt
    # This is temporary we would need to change this.
    return model_output