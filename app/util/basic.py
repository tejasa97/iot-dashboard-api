def compute_stats(values):

    if len(values) == 0:
        return 'NIL'

    min_ = values[0]
    max_ = values[0]
    sum_ = 0

    for value in values:
        if value > max_:
            max_ = value
        elif value < min_:
            min_ = value
        sum_ += value
    
    # return min_, max_, round(sum_/len(values), 1)
    return {
        'min' : min_,
        'max' : max_,
        'avg' : round(sum_/len(values), 1)
    }