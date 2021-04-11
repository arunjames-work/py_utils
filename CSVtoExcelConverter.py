import pandas as pd

for i in range(4):
    pd.read_csv(r'LoadFile'+str(i+1)+'.csv').to_csv(r'Merged.csv', sep=',', header=True, index=False, index_label=None, mode='a+', encoding=None, compression='infer', quoting=None, quotechar='"',
                                                    line_terminator=None, chunksize=None, date_format=None, doublequote=True, escapechar=None, decimal='.', errors='strict', storage_options=None)

    # print(read_file)
    # read_file.to_excel(r'Converted.xlsx', index=None, header=False)
