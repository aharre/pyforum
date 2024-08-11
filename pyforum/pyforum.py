import random
import numpy as np

def prepare_forum_data(actual, feature, mode='mean', nt=1000, baseline=None, presorted=False):
    """Prepares the data for FORUM calculation.

    Args:
        actual (iterable): An array of ranked item scores to evaluate, up to length of `feature`.
        feature (iterable): All item feature scores to compare against.
        mode (str, optional): How to evaluate the baseline to compare performance against. Defaults to 'mean'.
        nt (int, optional): The number of iteraions to run when median bootstrap mode is used. Defaults to 1000.
        baseline (array, optional): The precomputed baseline to use, if desired. Defaults to None.
        presorted (bool, optional): Whether `feature` is already custom sorted. Defaults to False.

    Raises:
        ValueError: If the mode is invalid

    Returns:
        tuple: The sorted feature values, the baseline, and the length of the actual values
    """
    # Calculate the baseline
    n = len(actual)
    if n == len(feature):
        n -= 1
    if mode == 'mean': # Calculate the mean cumulative sum
        baseline = np.array([x*np.mean(feature) for x in range(1, n+1)])
    elif mode == 'median': # Bootstrap the median cumulative sum with random samples
        randoms = []
        for _ in range(nt):
            randoms.append(random.sample(feature, n))
        baseline = np.array(randoms).median(axis=1)
    elif mode == 'precomputed': # Use a precomputed baseline
        baseline = np.array(baseline[:n])
    else:
        raise ValueError('Invalid mode')

    # Sort the feature values, if needed
    if presorted:
        s_feat = np.array(feature)
    else:       
        s_feat = np.sort(feature)

    return s_feat, baseline, n

def norm_policy_deltas(actual, s_feat, baseline, n):
    """Calculates the normalized policy deltas for FORUM.

    Args:
        actual (iterable): An array of ranked item scores to evaluate, up to length of `feature`.
        s_feat (array): The sorted feature values to compare against.
        baseline (array, optional): The precomputed baseline to use, if desired. Defaults to None.
        n (int): The length of the actual values to evaluate up to.

    Returns:
        array: The normalized policy deltas for the ranked list of items
    """

    # Calculate the cumulative sums
    cs_best = np.cumsum(s_feat[::-1])[:n]
    cs_worst = np.cumsum(s_feat)[:n]
    cs_actual = np.cumsum(actual)[:n]

    # Calculate the differences from baseline
    d_best = cs_best - baseline
    d_worst = baseline - cs_worst
    d_actual = cs_actual - baseline

    # Calculate and average the ratios, +ve/-ve
    rat = np.where(d_actual>0, np.nan_to_num(d_actual/d_best), np.nan_to_num(d_actual/d_worst))
    return rat

def forum(actual, feature=None, ns=None, mode='mean', nt=1000, baseline=None, presorted=False):
    """Calculates FORUM for a ranked list of items.

    Args:
        actual (iterable): An array of ranked item scores to evaluate, up to length of `feature`.
        feature (iterable): All item feature scores to compare against. If note supplied, defaults to `actual`. Defaults to None.
        mode (str, optional): How to evaluate the baseline to compare performance against. Defaults to 'mean'.
        nt (int, optional): The number of iteraions to run when median bootstrap mode is used. Defaults to 1000.
        baseline (iterable, optional): The precomputed baseline to use, if desired. Defaults to None.
        presorted (bool, optional): Whether `feature` is already custom sorted. Defaults to False.
        ns (list, optional): The ns at which to evaluate FORUM. If not supplied, single value is calculated with `n=len(actual)`. Defaults to None.

    Raises:
        ValueError: If the mode is invalid

    Returns:
        float: FORUM for the ranked list of items
    """
    if not feature:
        feature = actual.copy()
    s_feat, baseline, n = prepare_forum_data(actual, feature, mode, nt, baseline, presorted)
    rat = norm_policy_deltas(actual, s_feat, baseline, n)
    if not ns:
        forum_score = rat.mean()
    else:
        forum_score = {n: rat[:n].mean() for n in ns}
    return forum_score

