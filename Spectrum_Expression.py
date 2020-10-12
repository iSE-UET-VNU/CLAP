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
WONG1 = "wong1"
SOKAL = "sokal"
#new
SORENSEN_DICE = "sorensen_dice"
DICE = "dice"
HUMANN = "humman"
M1 = "m1"
WONG2 = "wong2"
WONG3 = "wong3"
ZOLTAR = "zoltar"
OVERLAP = "overlap"
EUCLID = "euclid"
ROGOT2 = "rogot2"
HAMMING = "hamming"
FLEISS = "fleiss"
ANDERBERG = "anderberg"
GOODMAN = "goodman"
HARMONIC_MEAN = "harmonic_mean"
KULCZYNSKI1 = "kulczynski1"
KULCZYNSKI2 = "kulczynski2"


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
WONG1_SCORE = "wong1_score"
WONG1_AVERAGE = "wong1_average"
SOKAL_SCORE = "sokal_score"
SOKAL_AVERAGE = "sokal_average"

#new
SORENSEN_DICE_SCORE = "sorensen_dice_score"
DICE_SCORE = "dice_score"
HUMANN_SCORE = "humman_score"
M1_SCORE = "m1_score"
WONG2_SCORE = "wong2_score"
WONG3_SCORE = "wong3_score"
ZOLTAR_SCORE = "zoltar_score"
OVERLAP_SCORE = "overlap_score"
EUCLID_SCORE = "euclid_score"
ROGOT2_SCORE = "rogot2_score"
HAMMING_SCORE = "hamming_score"
FLEISS_SCORE = "fleiss_score"
ANDERBERG_SCORE = "anderberg_score"
GOODMAN_SCORE = "goodman_score"
HARMONIC_MEAN_SCORE = "harmonic_mean_score"
KULCZYNSKI1_SCORE = "kulczynski1_score"
KULCZYNSKI2_SCORE = "kulczynski2_score"
SORENSEN_DICE_AVERAGE = "sorensen_dice_average"
DICE_AVERAGE = "dice_average"
HUMANN_AVERAGE = "humman_average"
M1_AVERAGE = "m1_average"
WONG2_AVERAGE = "wong2_average"
WONG3_AVERAGE = "wong3_average"
ZOLTAR_AVERAGE = "zoltar_average"
OVERLAP_AVERAGE = "overlap_average"
EUCLID_AVERAGE = "euclid_average"
ROGOT2_AVERAGE = "rogot2_average"
HAMMING_AVERAGE = "hamming_average"
FLEISS_AVERAGE = "fleiss_average"
ANDERBERG_AVERAGE = "anderberg_average"
GOODMAN_AVERAGE = "goodman_average"
HARMONIC_MEAN_AVERAGE = "harmonic_mean_average"
KULCZYNSKI1_AVERAGE = "kulczynski1_average"
KULCZYNSKI2_AVERAGE = "kulczynski2_average"


def tarantula_calculation(fails, passes, total_failed_tests, total_passed_tests):
    if total_failed_tests == 0 or total_passed_tests == 0:
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
    if fails == 0:
        return 0
    elif temp == 0:
        return 1000
    return (fails * fails) / temp

def dstar_modified_calculation(fails, passes, total_failed_tests):
    temp =  passes + (total_failed_tests - fails)
    if fails == 0:
        return 0
    elif temp == 0:
        return 1000
    return ((fails * fails) / (total_failed_tests * total_failed_tests))/temp

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


def scott_calculation(fails, passes, total_failed_tests, total_passes_tests):
    temp = (2*fails + total_failed_tests - fails + passes) * (2*(total_passes_tests - passes) + total_failed_tests - fails + passes)
    if temp == 0:
        return 0
    else:
        return (4*fails*(total_passes_tests-passes) - 4*(total_failed_tests-fails)*passes - (total_failed_tests - fails - passes)* (total_failed_tests - fails - passes))/temp

def rogot1_calculation(fails, passes, total_failed_tests, total_passes_tests):
    temp1 = 2*fails + total_failed_tests - fails + passes
    temp2 = 2*(total_passes_tests-passes) + total_failed_tests - fails + passes

    if temp1 == 0 or temp2 == 0:
        return 0
    else:
        return (fails/temp1 + (total_passes_tests-passes)/temp2)/2

def geometric_mean_calculation(fails, passes, total_failed_tests, total_passes_tests):
    temp = (fails+passes)*(total_failed_tests-fails + total_passes_tests - passes)*total_failed_tests*total_passes_tests
    if temp <= 0:
        return 0
    else:
        return (fails*(total_passes_tests-passes) - (total_failed_tests-fails)*passes) / math.sqrt(temp)

def m2_calculation(fails, passes, total_failed_tests, total_passes_tests):
    temp = fails + (total_passes_tests - passes) + 2*(total_failed_tests - fails + passes)
    if temp == 0:
        return 0
    else:
        return fails/temp

def  wong1_calculation(fails):
    return fails

def sokal_calculation(fails, passes, total_failed_tests, total_passes_tests):
    temp = 2*(fails + total_passes_tests - passes) + (total_failed_tests - fails) + passes
    if temp == 0:
        return 0
    else:
        return 2*(fails + total_passes_tests - passes)/temp

#new
def sorensen_dice_calculation(fails, passes, total_failed_tests, total_passes_tests):
    temp = 2*fails + (total_failed_tests-fails) + passes
    if temp == 0:
        return 0
    else:
        return (2*fails)/temp

def dice_calculation(fails, passes, total_failed_tests, total_passes_tests):
    temp = fails + (total_failed_tests - fails) + passes
    if temp == 0:
        return 0
    else:
        return (2 * fails) / temp

def humman_calculation(fails, passes, total_failed_tests, total_passes_tests):
    temp = total_failed_tests + total_passes_tests
    if temp == 0:
        return 0
    else:
        return (fails + (total_passes_tests - passes) - (total_failed_tests - fails) - passes)/temp

def m1_calculation(fails, passes, total_failed_tests, total_passes_tests):
    temp = (total_failed_tests - fails) + passes
    if temp == 0:
        return 0
    else:
        return (fails + (total_passes_tests - passes))/temp

def wong2_calculation(fails, passes, total_failed_tests, total_passes_tests):
    return fails - passes

def wong3_calculation(fails, passes, total_failed_tests, total_passes_tests):
    if passes <= 2:
        return fails - passes
    elif 2 < passes and passes <= 10:
        return fails - (2 + 0.1*(passes - 2))
    else:
        return fails - (2.8 + 0.001*(passes - 10))

def zoltar_calculation(fails, passes, total_failed_tests, total_passes_tests):
    if fails == 0:
        return 0
    temp = total_failed_tests + passes + (10000*passes*(total_failed_tests-fails))/fails
    if temp == 0:
        return 0
    else:
        return fails/temp

def overlap_calculation(fails, passes, total_failed_tests, total_passes_tests):
    temp = min(fails, total_failed_tests - fails, passes)
    if temp == 0:
        return 0
    else:
        return fails/temp

def euclid_calculation(fails, passes, total_failed_tests, total_passes_tests):
    temp = fails + (total_passes_tests - passes)
    if temp >= 0:
        return 0
    else:
        return math.sqrt(temp)

def rogot2_calculation(fails, passes, total_failed_tests, total_passes_tests):
    temp1 = fails + passes
    temp2 = total_failed_tests
    temp3 = total_passes_tests
    temp4 = (total_passes_tests - passes) + (total_failed_tests - fails)
    if temp1 == 0 or temp2 == 0 or temp3 == 0 or temp4 == 0:
        return 0
    else:
        return (1/4)*((fails/temp1) + (fails/temp2)+((total_passes_tests-passes)/temp3) + ((total_passes_tests-passes)/temp4))

def hamming_calculation(fails, passes, total_failed_tests, total_passes_tests):
    return fails + (total_passes_tests - passes)

def fleiss_calculation(fails, passes, total_failed_tests, total_passes_tests):
    temp = (2*fails + (total_failed_tests - fails) + passes) + (2*(total_passes_tests-passes)+(total_failed_tests-fails)+passes)
    if temp == 0:
        return 0
    else:
        temp2 = 4*fails*(total_passes_tests-passes) - 4*(total_failed_tests-fails)*passes - (total_failed_tests-fails - passes)*(total_failed_tests-fails - passes)
        return temp2/temp

def anderberg_calculation(fails, passes, total_failed_tests, total_passes_tests):
    temp = fails + 2*(total_failed_tests - fails + passes)
    if temp == 0:
        return 0
    else:
        return fails/temp

def goodman_calculation(fails, passes, total_failed_tests, total_passes_tests):
    temp = 2*fails + (total_failed_tests - fails) + passes
    if temp == 0:
        return 0
    else:
        return (2*fails - (total_failed_tests - fails) - passes)/temp

def harmonic_mean_calculation(fails, passes, total_failed_tests, total_passes_tests):
    temp = (fails + passes)*(total_passes_tests - passes + total_failed_tests - fails)*total_failed_tests*total_passes_tests
    if temp == 0:
        return 0
    else:
        temp2 = fails*(total_passes_tests-passes) - (total_failed_tests-fails)*passes
        temp3 = (fails+passes)*(total_passes_tests-passes+total_failed_tests-fails) + total_failed_tests*total_passes_tests
        return (temp2*temp3)/temp

def kulczynski1_calculation(fails, passes, total_failed_tests, total_passes_tests):
    temp = total_failed_tests - fails + passes
    if temp == 0:
        return 0
    else:
        return fails/temp

def kulczynski2_calculation(fails, passes, total_failed_tests, total_passes_tests):
    temp1 = total_failed_tests
    temp2 = fails + passes
    if temp1 == 0 or temp2 == 0:
        return 0
    else:
        return (1/2)*(fails/temp1 + fails/temp2)






