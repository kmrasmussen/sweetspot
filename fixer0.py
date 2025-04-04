from codegen_gym import collect_problems
from codegen_gym import eval_problem
from codegen_gym import eval_candidate
import pickle
from llm_caller import get_response
from config import *
from utils import is_valid_python, extract_markdown_code
from adversary0 import adversary_wrapper, adversary0_function
from adversary1 import *

def fixer0(problem, buggy_code):
  original_description = problem.description
  original_code = problem.python_solution

  system_prompt = """
  Hi, you are an AI called FIXER that is being used to fix bugs in code. The other AI is called BUGGER.
  Below we will present a competitive programming example instructions together with a candidate solution.
  There might be a bug in the candidate solution.
  Your job is to get rid of the bug in the candidate solution.
  The bug is neither too easy nor too difficult to find.
  We will test your solution to check if it passes the tests.
  Analyze the code before making the fix.
  Note that it is not a big bug, it's just a small intended to test you.
  The code does not have several bugs.

  You have to give the code in blocks like this.
  ```python
  <your code here>
  ```
  """

  user_prompt = f"Description: \n {original_description} \n Candidate code that might contain bug: \n```python\n{buggy_code}\n\nNow, make a correct version of the code."
  #print(user_prompt)

  fixer_response = get_response(system_prompt, user_prompt, MODEL_NAME_FIXER0)
  print('fixer response:', fixer_response)

  fixer_code = extract_markdown_code(fixer_response)

  syntax_result_original = is_valid_python(original_code)
  syntax_result_buggy = is_valid_python(buggy_code)
  syntax_result_fixer =  is_valid_python(fixer_code)
  print("syntax buggy code passed? want true:", syntax_result_buggy)
  print("syntax fixer code passed? want true:", syntax_result_fixer)

  eval_result_buggy = eval_candidate(problem, buggy_code, pol=False)
  print('buggy code passed? want false: ', eval_result_buggy.all_passed)

  eval_result_fixer = eval_candidate(problem, fixer_code, pol=False)
  print('fixer code passed? want true: ', eval_result_fixer.all_passed)

  good_outcome = not eval_result_buggy.all_passed and eval_result_fixer.all_passed  
  
  return good_outcome

filename = DSET_FILENAME
with open(filename, 'rb') as f:
  problems = pickle.load(f)

problem_i = 10
problem = problems[problem_i]
print('generating buggy code')
buggy_code = adversary_wrapper(problem, adversary_function=adversary0_function)
assert buggy_code is not None
print('generated buggy code, now fixing')

fixer_worked_counter = 0
Q = 5
for i in range(Q):
  print('i', i)
  fixer_worked = fixer0(problem, buggy_code)
  if fixer_worked:
    print("HURARY!! fixer worked")
    fixer_worked_counter += 1

print('fixer worked', fixer_worked_counter, Q)
performance = fixer_worked_counter / Q
learnability = performance * (1-performance)
print('learnability', round(learnability,2))