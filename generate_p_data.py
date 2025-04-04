from codegen_gym import collect_problems
import pickle

if __name__ == "__main__":
    difficulty = 7
    n_problems = 100
    # Generate a small dataset (10 samples)
    print(f"Generating CodeContests dataset with {n_problems} items where problems have difficulty level {difficulty}")
    problems_list = collect_problems(n_problems, difficulty=difficulty)
    print(problems_list[0].public_tests)
    filename = f'codecontests_difficulty{difficulty}_nproblems{n_problems}.pkl'
    with open(filename, 'wb') as f:
        pickle.dump(problems_list, f)
        print('saved as', filename)