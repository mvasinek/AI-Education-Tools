import os
import sys
from openai import OpenAI

# Constants
API_KEY_ENV_VAR = "OPENAI_VSB_API_KEY"
MODEL_NAME = "gpt-4o"
TRANSLATION_PROMPT = (
    "Translate the following frame of my bioinformatics lectures written in LaTeX into English. "
    "Keep the LaTeX formatting, translate only the text. Do not translate or modify image paths "
    "or names specified in \\includegraphics.\n\n"
)
MAX_TOKENS = 1000
TEMPERATURE = 0.2

# Initialize OpenAI client with the API key from environment variable
client = OpenAI(api_key=os.environ[API_KEY_ENV_VAR])

def translate_frame(frame_content):
    """
    Sends a LaTeX frame content to OpenAI for translation into English.
    
    Args:
        frame_content (str): The LaTeX content to be translated.
        
    Returns:
        str: Translated LaTeX content with only the text translated into English.
    """
    prompt = TRANSLATION_PROMPT + frame_content
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=MAX_TOKENS,
        temperature=TEMPERATURE
    )
    # Clean up response from code block formatting (if any)
    return response.choices[0].message.content.replace("```latex", "").replace("```", "")

def process_latex_file(input_file, output_file):
    """
    Reads a LaTeX file, translates frames, and writes the translated content to a new file.
    
    Args:
        input_file (str): The path to the input LaTeX file.
        output_file (str): The path to the output file where the translated content will be written.
    """
    with open(input_file, "r", encoding="utf-8") as infile:
        lines = infile.readlines()

    with open(output_file, "w", encoding="utf-8") as outfile:
        i = 0
        while i < len(lines):
            line = lines[i].lstrip()
            
            if line.startswith("\\begin{frame}"):
                # Collect all lines until the end of the frame
                frame = []
                while not lines[i].lstrip().startswith("\\end{frame}"):
                    frame.append(lines[i])
                    i += 1
                frame.append(lines[i])  # Add the closing \end{frame}

                # Process the collected frame
                frame_content = "".join(frame)
                translated_frame = translate_frame(frame_content)
                print(translated_frame)  # Optional: Print the translated frame for debugging
                outfile.write(translated_frame)

            else:
                # Write non-frame content directly to the output file
                outfile.write(line)
            
            i += 1

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <input_file> <output_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    process_latex_file(input_file, output_file)
