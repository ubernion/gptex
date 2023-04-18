# GPTeX: LaTeX Generator Web Application

GPTeX is a Flask-based web application that leverages the GPT-4 AI model to generate LaTeX documents based on user input. It's designed to help users generate professional-looking mathematical expressions, equations, and graphical illustrations in LaTeX format, suitable for various fields, such as mathematics, physics, engineering, and computer science.

## Features

- User-friendly web interface to input queries
- GPT-4 AI model integration for generating LaTeX code
- LaTeX document generation with various useful packages preloaded
- PDF compilation and download of the generated LaTeX document

## Installation

1. Clone the repository:  

        git clone https://github.com/ubernion/gptex

2. Go to the project directory:   

        cd gptex 

3. Create a virtual environment and activate it:

        python -m venv venv
        source venv/bin/activate

4. Install the required dependencies:

        pip install Flask openai requests

5. Rename the .env.template file to .env and add your apikey in OPEN_AI_KEY=<your_key>


## Usage

1. Run the Flask web application:

        python chatex.py
        
2. Access the web application in your browser at http://127.0.0.1:5000

3. Enter your query and click "Generate LaTeX" to receive a PDF containing the generated LaTeX code. 

Their can be significant delay between your request and the pdf output, due to GPT-4 being pretty slow and also because the compilation time of the LaTeX code depends on your machine.

## License

This project is licensed under the [MIT License](LICENSE).




