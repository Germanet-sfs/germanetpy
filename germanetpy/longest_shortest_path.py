from germanetpy.synset import WordCategory


# get the depth (maybe extra method?)
def get_overall_longest_shortest_distance(germanet, category):
    """
    Iterate trough the synsets of a given wordcategory. For each synset, extract all possible hypernyms and compute the
    shortest possible distance to each hypernym. From these distances, also store the longest possible shortest
    distance.
    :param germanet: the germanet graph
    :param category: the wordcategory
    :return: a dictionary with each synset and its longest shortest distance, the overall longest shortest distance
    """
    synsets = germanet.get_synsets_by_wordcategory(category)
    longest_shortest_distances = []
    for synset in synsets:
        distances = synset.get_distances_hypernym_dic()
        longest_shortest_dist = max(distances.values())
        longest_shortest_distances.append(longest_shortest_dist)

    overall_maxlen = max(longest_shortest_distances)
    dist_dic = dict(zip(synsets, longest_shortest_distances))
    sorted_dist_dic = sorted(dist_dic.items(), key=lambda kv: kv[1], reverse=True)
    return sorted_dist_dic, overall_maxlen


def get_greatest_depth(germanet, category):
    """
    Iterate trough the synsets of a given word category. For each synset check the depth and return the greatest depth
    that has been seen.
    :param germanet: the germanet graph
    :param category: the wordcategory
    :return: [int] the greatest depth for a given word category. The depth of a synset is defined by the shortest
    path length
    between the synset and the root node
    """
    synsets = germanet.get_synsets_by_wordcategory(category)
    max_depth = 0
    for synset in synsets:
        depth = synset.min_depth()
        if depth >= max_depth:
            max_depth = depth
    return max_depth


def get_longest_possible_shortest_distance(wordcategory, germanet):
    """
    set a maxdistcounter = 0
    for each synset:
    get the corresponding longest shortest distance.
    if this plus the overall longest shortest distance is smaller than maxdistance:
        continue with the next synset
    if it is larger:
        go trough each synset and get the corresponding longest shortest distance.
        if this plus the longest shortest distance of the synset of interest is smaller than maxdistance:
            continue
        else:
            compute the actual path distance and update the maxdistance if it is larger
    :param wordcategory: the wordcategory for which this maxlen should be computed
    :param germanet: the germanet graph
    :return: the longest possible shortest distance between two synsets of a specified wordcategory
    """
    sorted_dist_dic, overall_maxlen = get_overall_longest_shortest_distance(wordcategory, germanet)
    longest_possible_shortest_distance = 0

    for synset, longest_shortest_dist in sorted_dist_dic:
        if longest_shortest_dist + overall_maxlen <= longest_possible_shortest_distance:
            continue
        for current_synset, current_shortest_dist in sorted_dist_dic:
            if current_shortest_dist + longest_shortest_dist <= longest_possible_shortest_distance:
                continue
            pathdist = current_synset.shortest_path_distance(synset)
            if pathdist > longest_possible_shortest_distance:
                longest_possible_shortest_distance = pathdist
    return longest_possible_shortest_distance, overall_maxlen


def print_all_longest_shortest_distances(germanet):
    """Computes and prints the longest shortest distances for every word category."""
    print(
        "longest shortest distance for nouns : %2d, maximum length for nouns : %2d" %
        get_longest_possible_shortest_distance(
            germanet, WordCategory.nomen))
    print(
        "longest shortest distance for verbs : %2d, maximum length for verbs : %2d" %
        get_longest_possible_shortest_distance(
            germanet, WordCategory.verben))
    print(
        "longest shortest distance for adjectives : %2d, maximum length for adjectives : %2d" %
        get_longest_possible_shortest_distance(
            germanet, WordCategory.adj))


def print_all_maximum_depths(germanet):
    """Computes and prints the maximum depth for every word category."""
    print(
        "maximum depth for nouns : %2d" %
        get_greatest_depth(
            germanet, WordCategory.nomen))
    print(
        "maximum depth for verbs : %2d" %
        get_greatest_depth(
            germanet, WordCategory.verben))
    print(
        "maximum depth for adjectives : %2d" %
        get_greatest_depth(
            germanet, WordCategory.adj))
