import argparse
import csv

import solucion as sol
import pregunta3 as p3

def is_acceptable_key(ksolution, kanswer):
  if len(ksolution) == len(kanswer):
    nsamechars = 0
    for i in range(len(ksolution)):
      if ksolution[i] == kanswer[i]:
        nsamechars += 1
    return nsamechars/len(ksolution) >= .59
  return false

def is_acceptable_messages(msolution, manswer):
  solution_set = set(msolution)
  msamemessages = 0
  for m in manswer:
    if m in solution_set:
      nsamemessages += 1
  return nsamemessages/len(msolution) >= .59

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('user', type=str, help='github username')
    args = parser.parse_args()



    encrypted_messages = sol.get_my_encrypted_messages(
        args.email,
        args.studentn,
        _FILE
    )

    solution = sol.break_random_otp(encrypted_messages)
    answer = p3.break_random_otp(encrypted_messages)

    tot_success_keys = 0
    tot_keys = len(solution)

    for k1, m1 in solution.items():
      for k2, m2 in p3.items():
        if is_acceptable_key(k1, k2) and is_acceptable_messages(m1, m2):
          tot_success_keys += 1


    points = 0

    if tot_success_keys > 0 and tot_success_keys < .49 * tot_keys:
      points = 1
    elif tot_success_keys >= .49 *tot_keys and tot_success_keys < .69 * tot_keys:
      points = 3
    elif tot_success_keys >= .69 * tot_keys:
      points = 5

    print(f"Points: {points}")




