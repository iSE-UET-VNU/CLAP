import math


TARANTULA = "tarantula"
OCHIAI = "ochiai"
OP2 = "op2"
BARINEL = "barinel"
DSTAR = "dstar"

TARANTULA_SCORE = "tarantula_score"
TARANTULA_AVERAGE = "tarantula_average"
OCHIAI_SCORE = "ochiai_score"
OCHIAI_AVERAGE = "ochiai_average"
OP2_SCORE = "op2_score"
OP2_AVERAGE = "op2_average"
DSTAR_SCORE = "dstar_score"
DSTAR_AVERAGE = "dstar_average"
BARINEL_SCORE = "barinel_score"
BARINEL_AVERAGE = "barinel_average"

def tarantula_calculation(fails, passes, total_failed_tests, total_passed_tests):
    if total_failed_tests == 0 and total_passed_tests == 0:
        return 0

    if fails == 0:
        return 0

    return (fails / total_failed_tests) / \
           ((fails / total_failed_tests) +
            (passes / total_passed_tests))


def ochiai_calculation(fails, passes, total_failed_tests):
    if total_failed_tests == 0:
        return 0
    if fails == 0:
        return 0
    return fails / math.sqrt(total_failed_tests * (
                fails + passes))


def op2_calculation(fails, passes, total_passed_tests):
    return fails - passes / (total_passed_tests + 1)


def barinel_calculation(fails, passes):
    if fails == 0 and passes == 0:
        return 0
    return 1 - passes / (passes + fails)


def dstar_calculation(fails, passes, total_failed_tests):
    temp = passes + (total_failed_tests - fails)
    if temp == 0:
        return 0
    return (fails * fails) / temp