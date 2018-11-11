import numpy as np

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
    showed_up_column_counts, not_showed_up_column_counts = get_column_value_counts(df_showed_up, df_not_showed_up, column)
    plt.scatter(showed_up_column_counts.keys(), showed_up_column_counts.values, alpha=0.5)
    plt.scatter(not_showed_up_column_counts.keys(), not_showed_up_column_counts.values, alpha=0.5)
    return identify_plot(plt, column)

def build_column_bar_chart(plt, df_showed_up, df_not_showed_up, column, invert_axis=False, sort=False):
    showed_up_column_counts, not_showed_up_column_counts = get_column_value_counts(df_showed_up, df_not_showed_up, column, sort)
    
    showed_up_keys = showed_up_column_counts.keys()
    not_showed_up_keys = not_showed_up_column_counts.keys()
    showed_up_values = showed_up_column_counts.values
    not_showed_up_values = not_showed_up_column_counts.values
    
    if invert_axis:
        plt.barh(showed_up_keys, showed_up_values, alpha=0.5)
        plt.barh(not_showed_up_keys, not_showed_up_values, alpha=0.5)
        plt.gca().invert_yaxis()
    else:
        plt.bar(showed_up_keys, showed_up_values, alpha=0.5)
        plt.bar(not_showed_up_keys, not_showed_up_values, alpha=0.5)
    
    return identify_plot(plt, column, invert_axis)

def build_column_plot(plt, df_showed_up, df_not_showed_up, column):
    showed_up_column_counts, not_showed_up_column_counts = get_column_value_counts(df_showed_up, df_not_showed_up, column, sort=True)
    plt.plot(showed_up_column_counts.keys(), showed_up_column_counts.values, alpha=0.5)
    plt.plot(not_showed_up_column_counts.keys(), not_showed_up_column_counts.values, alpha=0.5)
    return identify_plot(plt, column)

def build_no_showed_up_percentage_plot(plt, df, df_not_showed_up, delimited_percentage, column, min_appointment_count=0, percentages=None):
    percentages = get_no_showed_up_percentages(df, df_not_showed_up, column, min_appointment_count) if percentages is None else percentages
    plt.plot(percentages)
    plot_delimited_line(plt, delimited_percentage, percentages)
    identify_percentage_plot(plt, column)
    return percentages

def build_no_showed_up_percentage_bar(plt, df, df_not_showed_up, delimited_percentage, column, min_appointment_count=0, percentages=None, invert_axis=False):
    percentages = get_no_showed_up_percentages(df, df_not_showed_up, column, min_appointment_count) if percentages is None else percentages
    
    if invert_axis:
        plt.barh(percentages.keys(), percentages.values)
        plt.gca().invert_yaxis()
        plt.plot(np.repeat(delimited_percentage, len(percentages.keys())), percentages.keys().tolist(), color='k')
    else:
        plt.bar(percentages.keys(), percentages.values)
        plot_delimited_line(plt, delimited_percentage, percentages)
    
    identify_percentage_plot(plt, column, invert_axis)
    return percentages

def plot_delimited_line(plt, delimited_percentage, percentages):
    plt.plot(percentages.keys().tolist(), np.repeat(delimited_percentage, len(percentages.keys())), color='k')

def get_column_value_counts(df_showed_up, df_not_showed_up, column, sort=False):
    showed_up_column_counts = df_showed_up[column].value_counts()
    not_showed_up_column_counts = df_not_showed_up[column].value_counts()

    if sort:
        showed_up_column_counts.sort_index(axis=0, inplace=True)
        not_showed_up_column_counts.sort_index(axis=0, inplace=True)

    return showed_up_column_counts, not_showed_up_column_counts

def identify_percentage_plot(plt, column, invert_axis=False):
    if invert_axis:
        plt.ylabel(column)
        plt.xlabel('Percentage')
    else:
        plt.ylabel('Percentage')
        plt.xlabel(column)
    plt.title('No showed up patients by {}'.format(column))
    return plt

def identify_plot(plt, column, invert_axis=False):
    if invert_axis:
        plt.ylabel(column)
        plt.xlabel('Appointment Quantity')
    else:
        plt.ylabel('Appointment Quantity')
        plt.xlabel(column)
    plt.legend(['Showed up', 'Not showed up'])
    return plt

def get_counts_difference(df_showed_up, df_not_showed_up, column, sort_index=False, dropna=True):
    showed_up_column_counts, not_showed_up_column_counts = get_column_value_counts(df_showed_up, df_not_showed_up, column, sort_index)
    difference = showed_up_column_counts - not_showed_up_column_counts
    return difference if not dropna else difference.dropna()

def get_no_showed_up_percentages(df, df_not_showed_up, column, min_appointment_count=0):
    return ((df_not_showed_up[column].value_counts().loc[lambda x: x > min_appointment_count] / df[column].value_counts().loc[lambda x: x > min_appointment_count]).dropna()) * 100
