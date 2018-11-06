def invert_no_show_values(df):
    try:
        df.no_show = df.no_show.apply(lambda value: 0 if value == 'Yes' else 1)
        columns = df.columns.tolist()
        columns[-1] = 'showed_up'
        df.columns = columns
    except AttributeError:
        pass
    return df