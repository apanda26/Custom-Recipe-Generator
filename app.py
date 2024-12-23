from flask import Flask, render_template, request
import requests

GROQ_API_KEY = "USE OWN API KEY"  
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"


# Flask setup
app = Flask(__name__)


def get_llm_response(prompt):
    """Returns the LLM response for the given prompt using Groq API."""
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",  
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama3-8b-8192",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 100  
    }

    response = requests.post(GROQ_API_URL, headers=headers, json=payload)

    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        return f"Error: {response.status_code}, {response.text}"


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        dietary_restrictions = request.form['dietary_restrictions']
        favorite_ingredients = request.form['favorite_ingredients'].split(',')
        experience_level = request.form['experience_level']
        maximum_spice_level = int(request.form['maximum_spice_level'])
        available_spices = request.form['available_spices'].split(',')

        prompt = f"""
        Please suggest a recipe that includes the following ingredients: {favorite_ingredients}.
        The recipe should adhere to the following dietary restrictions: {dietary_restrictions}.
        The difficulty of the recipe should be: {experience_level}.
        The maximum spice level on a scale of 10 should be: {maximum_spice_level}.
        Provide detailed step-by-step instructions.
        The recipe should not include spices outside of this list: {available_spices}.
        """

        recipe = get_llm_response(prompt)
        return render_template('index.html', recipe=recipe)

    return render_template('index.html', recipe=None)


if __name__ == '__main__':
    app.run(debug=True)
