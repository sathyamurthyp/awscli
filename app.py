from flask import Flask, render_template, request
import openai
import subprocess

app = Flask(__name__)

openai.api_key = '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'

@app.route('/', methods=['GET', 'POST'])
def home():
    response = ""
    aws_output = ""
    if request.method == 'POST':
        user_input = request.form.get('user_input')

        if 'submit' in request.form:
            user_input = "you are an aws cli expert. generate only the cli command to " + user_input
            user_input += ". The output from openai api should only contain the cli command. DO NOT output any other text other than the cli command."
            openai_response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": user_input},
                ]
            )
            response = openai_response['choices'][0]['message']['content']

        elif 'execute' in request.form:
            aws_command = request.form.get('aws_command')
            if aws_command:
                aws_output = subprocess.check_output(aws_command, shell=True).decode('utf-8')

    return render_template('index.html', response=response, aws_output=aws_output)

if __name__ == '__main__':
    app.run(debug=True)

