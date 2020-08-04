import math


TARANTULA = "tarantula"
OCHIAI = "ochiai"
OP2 = "op2"
BARINEL = "barinel"
DSTAR = "dstar"
RUSSELL_RAO = "russell_rao"
SIMPLE_MATCHING = "simple_matching"
ROGERS_TANIMOTO = "rogers_tanimoto"
AMPLE = "ample"
JACCARD = "jaccard"
COHEN = "cohen"
SCOTT = "scott"
ROGOT1 = "rogot1"
GEOMETRIC_MEAN = "geometric_mean"
M2 = "m2"



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
RUSSELL_RAO_SCORE = "russell_rao_score"
RUSSELL_RAO_AVERAGE = "russell_rao_average"
SIMPLE_MATCHING_SCORE = "simple_matching_score"
SIMPLE_MATCHING_AVERAGE = "simple_matching_average"
ROGERS_TANIMOTO_SCORE = "rogers_tanimoto_score"
ROGERS_TANIMOTO_AVERAGE = "rogers_tanimoto_average"
AMPLE_SCORE = "ample_score"
AMPLE_AVERAGE = "ample_average"
JACCARD_SCORE = "jaccard_score"
JACCARD_AVERAGE = "jaccard_average"
COHEN_SCORE = "cohen_score"
COHEN_AVERAGE = "cohen_average"
SCOTT_SCORE = "scott_score"
SCOTT_AVERAGE = "scott_average"
ROGOT1_SCORE = "rogot1_score"
ROGOT1_AVERAGE = "rogot1_average"
GEOMETRIC_MEAN_SCORE = "geometric_mean_score"
GEOMETRIC_MEAN_AVERAGE = "geometric_mean_average"
M2_SCORE = "m2_score"
M2_AVERAGE = "m2_average"


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


def op2_modified_calculation(fails, passes, total_failed_tests, total_passed_tests):
    if total_failed_tests == 0:
        return 0
    elif fails == 0:
        return 0
    return fails/total_failed_tests - passes / (total_passed_tests + 1)


def barinel_calculation(fails, passes):
    if fails == 0 and passes == 0:
        return 0
    return 1 - passes / (passes + fails)


def dstar_calculation(fails, passes, total_failed_tests):
    temp = passes + (total_failed_tests - fails)
    if fails == 0:
        return 0
    elif temp == 0:
        return 1000
    return (fails * fails) / temp

def dstar_modified_calculation(fails, passes, total_failed_tests):
    temp =  passes + (total_failed_tests - fails)
    if fails == 0:
        return 0
    elif total_failed_tests == fails:
        return 1
    suspiciousness =  (fails * fails) / (temp * temp)
    if suspiciousness > 1:
        return 1
    else:
        return suspiciousness

#new
def russell_rao_calculation(fails, total_failed_tests, total_passes_tests):
    if total_failed_tests + total_passes_tests == 0:
        return 0
    else:
        return fails/(total_failed_tests + total_passes_tests)

def simple_matching_calculation(fails, passes, total_failed_tests, total_passes_tests):
    if total_passes_tests + total_failed_tests == 0:
        return 0
    else:
        return (fails + total_passes_tests - passes)/(total_failed_tests + total_passes_tests)

def rogers_tanimoto_calculation(fails, passes, total_failed_tests, total_passes_tests):
    temp = fails + (total_passes_tests - passes) + 2*(total_failed_tests - fails + passes)
    if temp == 0:
        return 0
    else:
        return (fails + (total_passes_tests - passes))/ temp

def ample_calculation(fails, passes, total_failed_tests, total_passes_tests):
    if total_failed_tests == 0:
        return 0
    elif total_passes_tests == 0:
        return 1
    else:
        return abs(fails/total_failed_tests - passes/total_passes_tests)

def jaccard_calculation(fails, passes, total_failed_tests):
    if(total_failed_tests + passes) == 0:
        return 0
    else:
        return fails/(total_failed_tests + passes)

def cohen_calculation(fails, passes, total_failed_tests, total_passed_tests):
    temp = (fails + passes)*(total_passed_tests) + total_failed_tests*(total_failed_tests-fails+total_passed_tests-passes)
    if temp == 0:
        return 0
    else:
        return (2*fails*(total_passed_tests-passes) - 2*(total_failed_tests - fails)*passes)/temp

def cohen_modified_calculation(fails, passes, total_failed_tests, total_passed_tests):
    temp = (fails + passes)*(total_passed_tests) + total_failed_tests*(total_failed_tests-fails+total_passed_tests-passes)
    if temp == 0:
        return 0
    elif 2*fails*(total_passed_tests-passes) - 2*(total_failed_tests - fails)*passes < 0:
        return 0
    else:
        return (2*fails*(total_passed_tests-passes) - 2*(total_failed_tests - fails)*passes)/temp

def scott_calculation(fails, passes, total_failed_tests, total_passes_tests):
    temp = (2*fails + total_failed_tests - fails + passes) * (2*(total_passes_tests - passes) + total_failed_tests - fails + passes)
    if temp == 0:
        return 0
    else:
        return (4*fails*(total_passes_tests-passes) - 4*(total_failed_tests-fails)*passes - (total_failed_tests - fails - passes)* (total_failed_tests - fails - passes))/temp

def scott_modified_calculation(fails, passes, total_failed_tests, total_passes_tests):
    temp1 = 4*fails*(total_passes_tests-passes) - 4*(total_failed_tests-fails)*passes - (total_failed_tests - fails - passes)* (total_failed_tests - fails - passes)
    temp2 = (2*fails + total_failed_tests - fails + passes) * (2*(total_passes_tests - passes) + total_failed_tests - fails + passes)
    if temp2 == 0:
        return 0
    elif temp1 < 0:
        return 0
    else:
        return temp1/temp2

def rogot1_calculation(fails, passes, total_failed_tests, total_passes_tests):
    temp1 = 2*fails + total_failed_tests - fails + passes
    temp2 = 2*(total_passes_tests-passes) + total_failed_tests - fails + passes

    if temp1 == 0:
        return 0
    if temp1 != 0 and temp2 == 0:
        return fails/(2*temp1)
    else:
        return (fails/temp1 + (total_passes_tests-passes)/temp2)/2

def rogot1_modified_calculation(fails, passes, total_failed_tests, total_passes_tests):
    temp1 = 2*fails + total_failed_tests - fails + passes
    temp2 = 2*(total_passes_tests-passes) + total_failed_tests - fails + passes

    if temp1 == 0:
        return 0
    if temp1 != 0 and temp2 == 0:
        return fails/(2*temp1)
    else:
        return (fails/temp1 + (total_passes_tests-passes)/temp2)

def geometric_mean_calculation(fails, passes, total_failed_tests, total_passes_tests):
    temp = (fails+passes)*(total_failed_tests-fails + total_passes_tests - passes)*total_failed_tests*total_passes_tests
    if temp == 0:
        return 0
    else:
        return (fails*(total_passes_tests-passes) - (total_failed_tests-fails)*passes) / math.sqrt(temp)

def m2_calculation(fails, passes, total_failed_tests, total_passes_tests):
    temp = fails + (total_passes_tests - passes) + 2*(total_failed_tests - fails + passes)
    if temp == 0:
        return 0
    else:
        return fails/temp