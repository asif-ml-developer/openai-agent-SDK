uv init uv_lighlllm_chainlit
cd uv_lighlllm_chainlit
code .
uv sync
uv venv
copy ".venv\Scripts\activate" paste and enter

copy these and paste in .toml file

dependencies = [
    "chainlit>=2.2.1",
    "litellm>=1.63.0",
    "python-dotenv>=1.0.1",
]


then 

uv pip install -r pyproject.toml

create .env file  + paste api key + save

create main.py file + add code + must save before run

or use uv add chainlit>=2.2.1 litellm>=1.63.0 python-dotenv>=1.0.1

uv chainlit run main.py -w

create .env file  + paste api key + save
