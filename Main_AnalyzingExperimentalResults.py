import os

from xlsxwriter import Workbook

from ExperimentalResultsAnalyzer import summary_result, write_header_to_excel_file, write_result_to_excel_file, \
    SYSTEM_COL, K_WISE_COL, summary_same_bugs
from FileManager import EXPERIMENT_RESULT_FOLDER, join_path, get_experimetal_result_system_dir, \
    get_experimetal_result_k_wise

def get_detail_experiment():
    experiment_file_name = join_path(EXPERIMENT_RESULT_FOLDER, "summary.xlsx")
    wb = Workbook(experiment_file_name)
    sheet = wb.add_worksheet("sheet1")
    row = 0
    write_header_to_excel_file(row, sheet)

    row += 1

    for system_name in os.listdir(EXPERIMENT_RESULT_FOLDER):
        system_dir = get_experimetal_result_system_dir(system_name)
        sheet.write(row, SYSTEM_COL, system_name)
        if (os.path.isdir(system_dir)):
            for k_wise in os.listdir(system_dir):
                sheet.write(row, K_WISE_COL, k_wise)
                k_wise_dir = get_experimetal_result_k_wise(system_dir, k_wise)
                for file in os.listdir(k_wise_dir):
                    if file.endswith(".xlsx"):
                        result = summary_result(k_wise_dir, file)
                        row = write_result_to_excel_file(result, row, sheet)
    wb.close()

def get_experimental_result_for_same_bug():
    one_wise = "/Users/thu-trangnguyen/Documents/project/InputPreparation/experiment_results/BankAccount/1-wise/1wise-BankAccountTP_coverage0.95.xlsx"
    two_wise = "/Users/thu-trangnguyen/Documents/project/InputPreparation/experiment_results/BankAccount/2-wise/2wise-BankAccountTP_coverage0.95_1.xlsx"
    three_wise = "/Users/thu-trangnguyen/Documents/project/InputPreparation/experiment_results/BankAccount/3-wise/3wise-BankAccountTP_coverage0.95.xlsx"
    four_wise = "/Users/thu-trangnguyen/Documents/project/InputPreparation/experiment_results/BankAccount/4-wise/4wise-BankAccountTP_coverage0.95.xlsx"
    result2 = summary_same_bugs(one_wise, [four_wise, two_wise, three_wise])
    print(result2)


if __name__ == "__main__":
    get_experimental_result_for_same_bug()
    #get_detail_experiment()




