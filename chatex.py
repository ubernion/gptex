from flask import Flask, render_template, request, send_file, jsonify
import openai
import requests
import os
import tempfile
import subprocess
import shutil
import contextlib import contextmanager


OPENAI__API_KEY = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route("/generate_latex", methods=["POST"])
def generate_latex():
    # Retrieve chat input from the user
    user_input = request.form.get('user_input')

    # Call the OpenAI API to get a response from the GPT model
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
        {"role": "system", "content": "You are GPTeX (TeX as in LaTeX), an AI assistant system specifically designed to provide users with answers to any question in LaTeX format. As an expert in typesetting mathematical equations and symbols, you can interpret natural language queries and generate accurate and professional-looking mathematical expressions in response. As LatexGPT, you have been trained on an extensive database of mathematical formulas, symbols, and conventions, allowing you to recognize and interpret a wide variety of mathematical expressions. Whether users need to write a complex equation, a proof, or a mathematical model, you can provide them with clear and concise LaTeX code that accurately reflects the intended meaning of their question. You are a powerful resource for researchers, students, and professionals working in fields such as mathematics, physics, engineering, and computer science. Whether users are writing a research paper, working on a thesis, or simply need assistance with a mathematical problem, you can provide them with accurate and professional-looking LaTeX code that will save them time and effort.So whether users need to typeset a simple algebraic equation or a complex integral, as LatexGPT, you are their go-to AI assistant system for all their mathematical typesetting needs. You need to surround thes equations you output with $ symbols, like this: $c^2 = a^2 + b^2$. Your answer will be ouputed in a article type A4 LaTeX pdf, adjust the format accordingly. Make use of the package called pgfplots or the package called smartdiagram to create graphical illustrations to each of your input. Don't hesitate to use any of those additional packages you were trained on: amsmath,amsfonts,amssymb,graphicx,geometry,hyperref,cleveref,caption,subcaption,natbib,booktabs,siunitx,tikz,pgf,listings,microtype,tabularx,multirow,multicol,enumitem,wrapfig,xcolor,titlesec,tocloft,algorithm,algorithmicx,algpseudocode,acronym,glossaries,coffee."},
            {"role": "user", "content": user_input+'You can use some of the packages you are trained on.'}], 
        temperature=0,
    )

    latex_code = response['choices'][0]['message']['content'].strip()

    latex_code = (
        r"\documentclass[a4paper]{article}"
        r"\usepackage{amsmath,amssymb,pgfplots,smartdiagram,amsfonts,fancyhdr,graphicx,geometry,hyperref,cleveref,caption,subcaption,natbib,booktabs,siunitx,tikz,pgf,listings,microtype,tabularx,multirow,multicol,enumitem,wrapfig,xcolor,titlesec,tocloft,algorithm,algorithmicx,algpseudocode,acronym,glossaries}"
        r"\begin{document}"
        f"{latex_code}"
        r"\end{document}"
    )    
    try:
        # Compile LaTeX code to PDF
        pdf_file = compile_latex(latex_code)
        print(f"PDF file path: {pdf_file}")
        return send_file(pdf_file, mimetype='application/pdf', as_attachment=True, download_name="output.pdf")
    except Exception as e:
        return jsonify({'error': str(e)})


@contextmanager
def temporary_directory():
    tmpdir = tempfile.mkdtemp()
    try:
        yield tmpdir
    finally:
        shutil.rmtree(tmpdir)

def compile_latex(latex_code):
    with tempfile.TemporaryDirectory() as tmpdir:
        tex_file = os.path.join(tmpdir, 'output.tex')
        pdf_file = os.path.join(tmpdir, 'output.pdf')

        with open(tex_file, "w") as f:
            f.write(latex_code)

        pdflatex_path = "/Library/TeX/texbin/pdflatex"  # Replace with the path you found earlier

        result = subprocess.run([pdflatex_path, '-interaction=nonstopmode', '-output-directory', tmpdir, tex_file], capture_output=True, text=True)

        log_file = os.path.join(tmpdir, 'output.log')
        with open(log_file, 'r') as f:
            log_contents = f.read()
        print("Output log contents:")
        print(log_contents)

        if result.returncode != 0:
            print("pdflatex command returned an error:")
            print(result.stdout)
            print(result.stderr)
        else:
            print("pdflatex command output:")
            print(result.stdout)

        if not os.path.exists(pdf_file):
            print(f"PDF file not found at: {pdf_file}")
            print("Temporary directory contents:")
            for file in os.listdir(tmpdir):
                print(f" - {file}")

        # Copy the file to a non-temporary location
        output_dir = os.path.join(os.getcwd(), 'output')
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        final_pdf_file = "/Users/ilanv/gptex/output/generated_output.pdf"
        shutil.copyfile(pdf_file, final_pdf_file)

    return final_pdf_file

if __name__ == '__main__':
    app.run(debug=True)
