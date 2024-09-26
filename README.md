# AI-Education-Tools
A set of tools to facilitate work in an academic environment.

**All tools assume that you have an OpenAI API key available and that its value is set in the environment variables under the variable OPENAI_VSB_API_KEY**

## Requirements

python 3.7 or higher

### Packages
pip install openai


## LaTex slide translation into english
The script tools/latex_to_en.py translates slides that start with \begin{frame} and end with \end{frame} from the original language of the slide into English. Modify this script as you like; for your own use, I recommend adjusting the TRANSLATION_PROMPT to suit your specific needs.