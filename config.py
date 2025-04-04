import os
DSET_N_PROBLEMS=100
DSET_DIFFICULTY=7
DSET_FILENAME = f'codecontests_difficulty{DSET_DIFFICULTY}_nproblems{DSET_N_PROBLEMS}.pkl'
MODEL_NAME_ADVERSARY0="google/gemma-3-27b-it:free" #"qwen/qwen2.5-vl-3b-instruct:free"
MODEL_NAME_FIXER0="google/gemma-3-27b-it:free" #"openai/gpt-4o-mini"
OPENROUTER_API_KEY=os.environ.get("OPENROUTER_API_KEY")

'''
Promising cominations
adversary,fixer,performance,learnability
openai/gpt-4o-mini,google/gemini-2.0-flash-lite-001
openai/gpt-4o-mini,google/gemma-3-12b-it,0.2
google/gemma-3-12b-it,google/gemma-3-12b-it,0.8
google/gemma-3-12b-it,google/gemma-3-12b-it,0.0
google/gemma-3-12b-it,google/gemma-3-27b-it:free,1,0
'''