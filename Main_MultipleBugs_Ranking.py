from FileManager import join_path
from ranking.MultipleBugsManager import mutiple_bugs_ranking
from ranking.Spectrum_Expression import JACCARD, SORENSEN_DICE, TARANTULA, OCHIAI, OP2, BARINEL, DSTAR, ROGERS_TANIMOTO, AMPLE, \
    SIMPLE_MATCHING, RUSSELL_RAO, COHEN, SCOTT, ROGOT1, GEOMETRIC_MEAN, M2, WONG1, SOKAL, DICE, HUMANN, OVERLAP, ZOLTAR, \
    WONG3, WONG2, M1, ROGOT2, EUCLID, HAMMING, FLEISS, ANDERBERG, KULCZYNSKI1, KULCZYNSKI2, HARMONIC_MEAN, GOODMAN


if __name__ == "__main__":
    result_folder = "multiple_bugs_"
    base_dir = "/home/huent/Documents/Trang/Mixed_Multiple_bugs/"
    system_names = ["GPL", "GPL3", "ExamDB2new", "ExamDB3new", "Email2new", "Email3new", "BankAccountTP2new", "BankAccountTP3new"]
    filtering_coverage_rate_list = [0.1]
    for system_name in system_names:
        system_dir = join_path(base_dir, system_name)
        for coverage in filtering_coverage_rate_list:
            print(system_dir)
            mutiple_bugs_ranking(result_folder, system_name, system_dir, [TARANTULA, OCHIAI, OP2, BARINEL, DSTAR,
                                                    RUSSELL_RAO, SIMPLE_MATCHING, ROGERS_TANIMOTO, AMPLE, JACCARD,
                                                    COHEN, SCOTT, ROGOT1, GEOMETRIC_MEAN, M2,
                                                    WONG1, SOKAL, SORENSEN_DICE, DICE, HUMANN,
                                                    M1, WONG2, WONG3, ZOLTAR, OVERLAP,
                                                    EUCLID, ROGOT2, HAMMING, FLEISS, ANDERBERG,
                                                    GOODMAN, HARMONIC_MEAN, KULCZYNSKI1, KULCZYNSKI2], coverage)