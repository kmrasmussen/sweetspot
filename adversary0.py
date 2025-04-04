from codegen_gym import collect_problems
from codegen_gym import eval_problem
from codegen_gym import eval_candidate
import pickle
from llm_caller import get_response
from config import *
from utils import is_valid_python
from utils import extract_markdown_code
from adversary1 import *

def adversary0_function(problem):
  original_description = problem.description
  original_code = problem.python_solution

  system_prompt = """
  Hi, you are an AI called BUGGER that is being used to train another AI to fix bugs in code. The other AI is called FIXER.
  Below we will present a competitive programming example instructions together with a correct solution.
  Your job is to introduce a bug in the solution. The bug should neither be too easy nor too difficult to find.
  You should try to give buggy code that sometimes FIXER will find the bug and sometimes FIXER will not find the bug.
  In that way FIXER can learn from your buggy code.
  If you make it too hard to find the bug, FIXER will not learn anything.
  If you make it too easy there might not even be a bug, or the FIXER will not learn anything because it is too easy to fix.
  Do not write any comments in the code, that indicates where you made a change.
  Try to make a plan for what you are going to change.
  Beware that if you do not try hard enough, you will not break any of the tests and you will get 0 reward.
  MAKE THE TESTS FAIL.
  Introduce ONLY ONE bug.
  You have to give the code in blocks like this.
  ```python
  <your code here>
  ```
  """

  user_prompt = f"Description: \n {original_description} \n Original working code: \n```python\n{original_code}\n\nNow, make a buggy version of the code. First analyze the code and decide what bug you could introduce then make the new code."
  #print(user_prompt)

  adversary_response = get_response(system_prompt, user_prompt, MODEL_NAME_ADVERSARY0)
  print(adversary_response)

  buggy_code = extract_markdown_code(adversary_response)

  return buggy_code

def adversary_wrapper(problem, adversary_function):
  original_code = problem.python_solution
  buggy_code = adversary_function(problem)
  print('received buggy code:')
  print('BUGGY CODE START')
  print(buggy_code)
  print('BUGGY CODE END')
  if not is_valid_python(original_code):
    raise Exception('not even the original code is valid python')
  if not is_valid_python(buggy_code):
    print("BEWARE: Buggy code was not python")
    raise Exception('buggy code is not valid python')

  eval_result_original = eval_candidate(problem, original_code, pol=False)
  if not eval_result_original.all_passed:
    raise Exception("Not even original code passed its own tests")

  eval_result_buggy = eval_candidate(problem, buggy_code, pol=False)
  if eval_result_buggy.all_passed:
    print("OH NO Buggy code already passed")
    raise Exception('buggy code already passed')
  else:
    print("YAY! buggy code fails tests")
  return buggy_code
  

if __name__ == "__main__":
  filename = DSET_FILENAME
  with open(filename, 'rb') as f:
    problems = pickle.load(f)

  problem = problems[0]

  buggy_code = adversary_wrapper(problem, adversary_toy1_function)  