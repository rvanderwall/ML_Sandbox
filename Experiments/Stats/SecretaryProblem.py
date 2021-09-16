
# Secretary stopping problem
# Find the best candidate without searching all of them and
# when you cannot recall a dismissed candidate

# https://www.geeksforgeeks.org/secretary-problem-optimal-stopping-problem/
import random
import math

e = 2.71828

# To find closest integer os num
def roundNo(num):
    if num < 0 :
        return num - 0.5
    else:
        return num + 0.5

# Finds best candidate using n/e rule
def findBestCandidate(candidates):
    n = len(candidates)
    # Calculating sample size for benchmarking
    sample_size = roundNo(n / e)
    sample_size = math.sqrt(n)

    # print(f"Find best candidate using first {sample_size} candidates as benchmark, from {n} total")
    # Find best candidate in sample size
    best = 0
    for i in range(1, int(sample_size)):
        if candidates[i] > candidates[best]:
            best = i

    # Find first candidate better than benchmark
    for i in range(int(sample_size), n):
        if candidates[i] >= candidates[best]:
            best = i
            break

    if (best >= int(sample_size)):
        return best
    else:
        return -1

def findBestCandidateSearch(candidates):
    # Find best candidate
    best = 0
    for i in range(1, len(candidates)):
        if candidates[i] > candidates[best]:
            best = i

    return best

def createCandidates(n):
    candidates = [0] * n
    for i in range(n):
        candidates[i] = 1 + random.randint(1,n)
    return candidates

def printCandidates(candidates):
    n = len(candidates)
    print("Candidate : ", end="")
    for i in range(n):
        print(i+1, end=" ")

    print("\nTalents :   ", end="")
    for i in range(n):
        print(candidates[i], end = " ")

def run_sample(n):
    candidates = createCandidates(n)
    printCandidates(candidates)
    best = findBestCandidate(candidates)
    best2 = findBestCandidateSearch(candidates)

    if best > 0 :
        print(f"Best candidate is {best} with {candidates[best]}")
    else:
        print("Unable to find better candidate than benchmark")
    print(f"Actual best is {best2} with {candidates[best]}")


def run_simulation():
    num_candidates = 50
    num_trials = 10000

    total_match = 0
    diff = 0
    total_bests = 0
    for i in range(num_trials):
        candidates = createCandidates(num_candidates)
        best = findBestCandidate(candidates)
        actual_best = findBestCandidateSearch(candidates)
        found_best_val = candidates[best]
        actual_best_val = candidates[actual_best]
        if found_best_val == actual_best_val:
            total_match += 1
        diff += actual_best_val - found_best_val
        total_bests += actual_best_val

    print(f"Got the actual best {total_match} times out of {num_trials}")
    print(f"Average best values = {total_bests / num_trials}")
    print(f"Average difference = {diff / num_trials}")
