import pandas as pd


def gener(df, error):
    """根据标注生成字典

    参数：
        df：通过pandas读取的excel表格，单sheet。
        error：本次sheet表中已经提取的错误。
    """

    error = error
    for _, row in df.iterrows():
        if not pd.isna(row['错误位置1']) and row['错误位置1'] not in error['错误位置']:
            error['错误位置'].append(row['错误位置1'])
        if not pd.isna(row['错误位置2']) and row['错误位置2'] not in error['错误位置']:
            error['错误位置'].append(row['错误位置2'])

        if not pd.isna(row['归纳错误类型']):
            if row['归纳错误类型'] not in error['错误类型'] and not pd.isna(row['原错误类型']):
                error['错误类型'][row['归纳错误类型']] = []

            if row['原错误类型'] not in error['错误类型'][row['归纳错误类型']]:
                if pd.isna(row['原错误类型']):
                    print('存在空值', end=',')
                else:
                    error['错误类型'][row['归纳错误类型']].append(row['原错误类型'])

    return error


def merge(errors, expert):
    """ 将人工字典合并到提取的字典中

    参数：
        errors：从excel中提取的字典
        expert：手动添加的字典
    """

    for i in expert['错误位置']:
        if i not in errors['错误位置']:
            errors['错误位置'].append(i)

    for k, v in expert['错误类型'].items():
        errors['错误类型'].setdefault(k, []).extend(v)

    return errors


def rever(d):
    """将字典的键值对反转

    参数：
        d：要反转的字典
    """

    tmp = {}
    for k, v in d.items():
        for e in v:
            tmp[e] = k

    return tmp


def recog(df, error):
    """识别excel单sheet的错误

    输入：
        df：传入的单sheet数据
        error：科目对应的错误字典

    返回：
        dataframe格式的文件
    """

    for index, row in df.iterrows():
        des = row['品管异常描述']

        for s in error['错误位置']:
            if des.find(s) != -1:
                df.loc[index, '错误位置'] = df.loc[index, '错误位置']+s+','
        df.loc[index, '错误位置'] = df.loc[index, '错误位置'].strip(',')

        for k, v in error['错误类型'].items():
            if des.find(k) != -1:
                # print(type(df.loc[index, '错误类型']))
                # print(v)
                df.loc[index, '错误类型'] = df.loc[index, '错误类型']+v+','
                df.loc[index, '原文错误'] = df.loc[index, '原文错误']+k+','
        df.loc[index, '错误类型'] = df.loc[index, '错误类型'].strip(',')
        df.loc[index, '原文错误'] = df.loc[index, '原文错误'].strip(',')

    return df
