import json
from tqdm import tqdm

def convert_json_file(input_file_path, output_file_path):
    # Load the JSON data from the file
    with open(input_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Initialize an empty dictionary to hold conversations
    conversations = {}

    print(data[0])
    # .replace("/n/n","\n\n")

    # Iterate through each message in the provided JSON data
    for message in tqdm(data, desc="Processing messages"):
        # Create a unique conversation key based on user_uid and star_uid
        conversation_key = (message["user_uid"], message["star_uid"])

        # If the conversation key does not exist, initialize it
        if conversation_key not in conversations:
            conversations[conversation_key] = {
                "user_uid": message["user_uid"],
                "star_uid": message["star_uid"],
                "conversation": []
            }

        # Keep track of the last message type in this conversation
        last_message_type = conversations[conversation_key]["conversation"][-1]["type"] if conversations[conversation_key]["conversation"] else None

        # Enforce the "human" -> "ai" sequence
        if message["type"] == "human" and last_message_type != "ai":
            # If the last message was not 'ai', it's okay to add a 'human' message
            conversations[conversation_key]["conversation"].append({"type": "human", "content": message["content"]})
        elif message["type"] == "ai" and last_message_type == "human":
            # If the last message was 'human', add the 'ai' message and mark this pair as complete
            conversations[conversation_key]["conversation"][-1].update({"ai": message["content"]})
            conversations[conversation_key]["conversation"][-1]["complete"] = True

    # Extract the conversations and format them into the requested list
    # Only include complete pairs of 'human' followed by 'ai'
    formatted_conversations = [{
        "user_uid": conv["user_uid"],
        "star_uid": conv["star_uid"],
        "conversation": [
            {"human": pair["content"], "ai": pair["ai"]} 
            for pair in conv["conversation"] if pair.get("complete")
        ]
    } for conv in conversations.values()]

    # Save the formatted conversations into a JSON file
    with open(output_file_path, 'w', encoding='utf-8') as outfile:
        for item in formatted_conversations:
            json_record = json.dumps(item, ensure_ascii=False)
            outfile.write(json_record + '\n')

# Sample usage:
input_file_path = 'data/avatara-chat-060224.json'
output_file_path = 'data/avatara-chat.jsonl'
convert_json_file(input_file_path, output_file_path)
