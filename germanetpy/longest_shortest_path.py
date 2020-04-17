def get_overall_longest_shortest_distance(germanet, category) -> (dict, int):
    """
    Iterate trough the synsets of a given wordcategory. For each synset, extract all possible hypernyms and compute the
    shortest possible distance to each hypernym. From these distances, also store the longest possible shortest
    distance.
    :type category: WordCategory
    :type germanet: Germanet
    :param germanet: the germanet graph
    :param category: the wordcategory
    :return: a dictionary with each synset and its longest shortest distance, the overall
    longest shortest distance
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


def get_greatest_depth(germanet, category) -> int:
    """
    Iterate trough the synsets of a given word category. For each synset check the depth and return the greatest depth
    that has been seen.
    :type category: WordCategory
    :type germanet: Germanet
    :param germanet: the germanet graph
    :param category: the wordcategory
    :return: the greatest depth for a given word category. The depth of a synset is defined by the shortest
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


def get_longest_possible_shortest_distance(germanet, wordcategory):
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
    :rtype: (int, int, tuple(Synset, Synset)
    :type wordcategory: WordCategory
    :type germanet: Germanet
    :param wordcategory: the wordcategory for which this maxlen should be computed
    :param germanet: the germanet graph
    :return: the longest possible shortest distance between two synsets of a specified wordcategory, the maximum depth
    of any synset (lenght to the root) and a Tuple with two synsets that have the longest shortest distance
    """
    sorted_dist_dic, overall_maxlen = get_overall_longest_shortest_distance(germanet=germanet, category=wordcategory)
    longest_possible_shortest_distance = 0
    synset_pair_longest_distance = (germanet.root, germanet.root)

    for synset, longest_shortest_dist in sorted_dist_dic:
        if longest_shortest_dist + overall_maxlen <= longest_possible_shortest_distance:
            continue
        for current_synset, current_shortest_dist in sorted_dist_dic:
            if current_shortest_dist + longest_shortest_dist <= longest_possible_shortest_distance:
                continue
            pathdist = current_synset.shortest_path_distance(synset)
            if pathdist > longest_possible_shortest_distance:
                longest_possible_shortest_distance = pathdist
                synset_pair_longest_distance = (synset, current_synset)
    return longest_possible_shortest_distance, overall_maxlen, synset_pair_longest_distance


def print_longest_shortest_distances(germanet, word_category):
    """Computes and prints the longest shortest distances for the given word category.
    :type word_category: WordCategory
    :type germanet: Germanet
    """
    longest_possible_shortest_distance, overall_maxlen, synset_pair_longest_distance = \
        get_longest_possible_shortest_distance(
            germanet=germanet, wordcategory=word_category)
    print(
        "retrieved the following information {}: \n"
        "longest shortest distance : {:5d} \n"
        "maximum depth : {:5d} \n, "
        "between the following synsets {}".format(
            str(word_category), longest_possible_shortest_distance,
            overall_maxlen, synset_pair_longest_distance))


def print_maximum_depths(germanet, word_category):
    """Computes and prints the maximum depth for the given word_category.
    :type word_category: WordCategory
    :type germanet: Germanet
    """
    print(
        "retrieved the following information {}: \n"
        "longest shortest distance : {:5d}".format(
            str(word_category), get_greatest_depth(germanet=germanet, category=word_category)))
