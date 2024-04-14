from openai import OpenAI
import csv
import os

API_KEY = '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'
client = OpenAI(api_key=API_KEY)

def load_data():
    with open('smaller_violation_results_comparison.txt', 'r') as f:
        lines = f.readlines()

    prompts = lines[::6]  
    expected_responses = lines[1::6]
    haiku_explanations = lines[3::6]
    mistral_explanations = lines[5::6]

    return prompts, expected_responses, haiku_explanations, mistral_explanations

def generate_response_with_openai(prompt):
    try:
        chat_completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt.strip()}
            ]
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def evaluate_responses(expected_response, generated_response, haiku_explanation, mistral_explanation):
    haiku_score = 0
    mistral_score = 0

    if generated_response:
        correct_response = int(expected_response.strip() == generated_response.strip())
    else:
        correct_response = 0

    if "No violation detected" in haiku_explanation:
        haiku_score = 1
    if "No violation detected" in mistral_explanation:
        mistral_score = 1

    return correct_response, haiku_score, mistral_score

def save_results_to_csv(results):
    with open('results.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Prompt', 'Expected Response', 'Generated Response', 'Evaluation Result', 'Haiku Score', 'Mistral Score'])
        writer.writerows(results)

def main():
    prompts, expected_responses, haiku_explanations, mistral_explanations = load_data()
    results = []

    for prompt, expected_response, haiku_explanation, mistral_explanation in zip(prompts, expected_responses, haiku_explanations, mistral_explanations):
        generated_response = generate_response_with_openai(prompt)
        evaluation_result, haiku_score, mistral_score = evaluate_responses(expected_response, generated_response, haiku_explanation, mistral_explanation)
        results.append([prompt, expected_response, generated_response, evaluation_result, haiku_score, mistral_score])

    save_results_to_csv(results)

if __name__ == "__main__":
    main()
