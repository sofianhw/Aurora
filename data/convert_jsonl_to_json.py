import json

with open('./data/indo-alpaca-gpt4-part1.jsonl', 'r') as json_file:
    data = [json.loads(line) for line in json_file]

for json_str in json_list:
    result = json.loads(data)

with open('./data/indo_alpaca.json', 'w', encoding="utf-8") as f1:
    json.dump(result, f1, ensure_ascii=False, indent=4)