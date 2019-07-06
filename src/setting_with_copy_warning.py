import pandas as pd


def main():
    df = pd.DataFrame({'id': [1, 2, 3], 'cost': [30, 25, 20]}, index=['01', '02', '03'])

    boolean01_flag = df['id'] > 1
    boolean02_flag = df['cost'] == 20

    boolean_flag = boolean01_flag & boolean02_flag

    df['boolean_flag'] = boolean_flag

    return df

