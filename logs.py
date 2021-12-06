from os import listdir
from os.path import isfile, join

def get_logs_data(request):
    filename = request.args.get('filename')
    my_path = "../log/"
    only_files = [f for f in listdir(my_path) if isfile(join(my_path, f))]
    data = {"log_files": only_files}
    last_lines = ""
    output_text = ""
    if filename is not None:
        if '-' in filename:
            output_text = "TIME, RSI, CURRENT PRICE, BUY PRICE, SELL PRICE\n"
            filename = filename.replace('-', '#')
        a_file = open(my_path + filename, "r")
        lines = a_file.readlines()
        last_lines = lines[-100:]
        print(last_lines)
        a_file.close()
        data["log_file_name"] = filename
    else:
        data["log_file_name"] = ""

    for line in last_lines:
        output_text = output_text + line
    data["log_file_content"] = output_text
    return data
