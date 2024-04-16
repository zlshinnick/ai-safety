import time
from app import generate_constitution, check_violations
from openai import OpenAI
from metrics.dataset import DatasetProcessor

processor = DatasetProcessor()
processed_dataset = processor.process_dataset()

client = OpenAI(api_key='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')

times = []

# iterate through each example in the processed dataset
for example in processed_dataset:
    location = example['content'][1].split(': ')[1]
    start_time = time.time()
    generate_constitution(client, location)
    end_time = time.time()
    times.append(end_time - start_time)

average_time = sum(times) / len(times)

print(f'Average time: {average_time} seconds')