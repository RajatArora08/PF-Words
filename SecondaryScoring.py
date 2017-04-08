import math
import re


def total_scoring(data):
    score_output = []

    for k, v in sorted(compute_total_scores(data).items(), key=lambda x: x[1][1], reverse=True):
        score_output.append([k, v[1]])

    return score_output


def log10_scoring(data):
    """
    Log10 of all scores and rank
    """
    total_scores = compute_total_scores(data)
    # compute log10 of all scores:
    # computed_data = {k: math.log10(v) for k, v in total_scores.items()}
    computed_data = {k: [v[0], 1 + math.log10(v[1])] for k, v in total_scores.items()}

    ranked_output = []

    for k, v in sorted(computed_data.items(), key=lambda x: x[1][1], reverse=True):
        ranked_output.append([k, v[1]])

    return ranked_output


def count_scoring(data):

    count_output = []

    for k, v in sorted(compute_total_scores(data).items(), key=lambda x: x[1][0], reverse=True):
        count_output.append([k, v[0]])

    return count_output


def highest_relevancy(data):

    output_list = []
    computed_result = sorted(compute_total_scores(data).items(), key=lambda x: x[1][1], reverse=True)

    total_score = 0
    no_of_words = len(computed_result)

    for k, v in computed_result:
        total_score += v[1]

    average = total_score / no_of_words

    for k, v in computed_result:
        if v[1] > average:
            output_list.append([k, v[1]])

    print("Average is {0}".format(average))
    return output_list


def compute_total_scores(data):
    pattern_PF_word = re.compile(r'^[0-9]*_([A-Za-z0-9_]*)')
    total_scores = {}

    for result in data:
        score = result['score']
        PF_word = re.findall(pattern_PF_word, result['id'])[0]

        if total_scores.__contains__(PF_word):
            total_scores[PF_word][0] += 1
            total_scores[PF_word][1] += score

        else:
            total_scores[PF_word] = [1, score]

    return total_scores
