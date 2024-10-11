from openai import OpenAI

client = OpenAI()

file_name = "data/batch_tasks_eval_3.jsonl"

batch_file = client.files.create(
  file=open(file_name, "rb"),
  purpose="batch"
)

batch_job = client.batches.create(
  input_file_id=batch_file.id,
  endpoint="/v1/chat/completions",
  completion_window="24h"
)

batch_job = client.batches.retrieve(batch_job.id)
print(batch_job)