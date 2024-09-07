from flask import Flask, request, jsonify
import requests
 
app = Flask(__name__)
 
API_URL = "https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3-8B-Instruct"
HEADERS = {"Authorization": "Bearer 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"}
 
def query_model(input_prompt):
    response = requests.post(API_URL, headers=HEADERS, json={"inputs": input_prompt, "parameters": {"max_new_tokens": 300}})
    response_json = response.json()
    if isinstance(response_json, list) and 'generated_text' in response_json[0]:
        return response_json[0]['generated_text']
    return "No message generated"
 
@app.route('/generate_message', methods=['POST'])
def generate_message():
    data = request.json
    name = data.get('name')
    headline = data.get('headline')
    location = data.get('location')
    about = data.get('about')
    post1 = data.get('post1')
    post2 = data.get('post2')
    post3 = data.get('post3')
    url = data.get('url')
    hr_name = data.get('hr_name')
    company_name = data.get('company_name')
 
    input_prompt = f"Generate a LinkedIn invite message for {name}, a {headline} based in {location}."
 
    if about:
        input_prompt += f" Include these details:\nAbout: {about}"
 
    posts = [post1, post2, post3]
    non_empty_posts = [post for post in posts if post]
    if non_empty_posts:
        input_prompt += f"\nLatest posts: {', '.join(non_empty_posts)}."
 
    input_prompt += (
        f" Make it personal and express interest in collaboration. Provide only the message text. "
        f"Also keep the message under 300 characters. These messages will be sent by the HR named {hr_name} of {company_name} based out of india."
        f"Assume whatever message you are generating is correct. Do not ask if changes are needed. "
        f"Keep the tone professional. Keep the message in same paragraph, don't change lines even for the ending signature part."
    )
 
    message = query_model(input_prompt)
    if 'Hi' in message:
        start_index = message.find('Hi')
        end_index = message.find('Please')
        if end_index != -1:
            message = message[start_index:end_index].strip() + f"\nBest, {hr_name} ({company_name})"
        else:
            message = message[start_index:].strip() + f"\nBest, {hr_name} ({company_name})"
    else:
        message = "No message generated"
 
    return jsonify({"message": message})
 
if __name__ == '__main__':
    app.run(debug=True, port=5000)
 