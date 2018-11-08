def invert_no_show_values(df):
    try:
        df.no_show = df.no_show.apply(lambda value: 0 if value == 'Yes' else 1)
        columns = df.columns.tolist()
        columns[-1] = 'showed_up'
        df.columns = columns
    except AttributeError:
        pass
    return df

def build_column_scatter_plot(plt, df_showed_up, df_not_showed_up, column):
    showed_up_column_counts = df_showed_up[column].value_counts()
    not_showed_up_column_counts = df_not_showed_up[column].value_counts()
    plt.scatter(showed_up_column_counts.keys(), showed_up_column_counts.values, alpha=0.5)
    plt.scatter(not_showed_up_column_counts.keys(), not_showed_up_column_counts.values, alpha=0.5)
    plt.ylabel('Appointment Quantity')
    plt.xlabel(column)
    plt.legend(['Showed up', 'Not showed up'])
    return plt
