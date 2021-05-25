import csv
import string
import argparse

from md5 import md5
from pprint import pprint
from otp_utils import xor
from sklearn.cluster import SpectralClustering

_FILE = '../../mensajes_pregunta_3/mensajes_p3.csv'
REG_CHARS = list(string.ascii_letters) + list(string.digits) + [".", ",", " "]


def count_irregular_chars(s):
    """ Returns the number of chars not in REG_CHARS of string s"""
    return len([c for c in s if c not in REG_CHARS])


def bitstring_to_string(s):
    """ Turns a binary string (e.g. '010101001') and returns a string
    assuming 8 bits per character and ascii encoding """
    ints = []
    for i in range(0, len(s), 8):
        ints.append(int(s[i:i + 8], 2))
    return ''.join([chr(x) for x in ints])


def argmax(num_list):
    max_val = min(num_list)
    max_pos = 0
    for i in range(len(num_list)):
        if num_list[i] >= max_val:
            max_val = num_list[i]
            max_pos = i

    return max_pos


def probability_same_key(c1, c2):
    """ Computes the probability that cyphertexts c1 and c2
    were encrypted using the same key, assuming that all keys
    are independent. The probability is just the number of positions
    in which the xor is the xor between two letters, which has a result <32."""

    return len([c for c in xor(c1, c2) if ord(c) < 32]) / len(c1)


def get_my_encrypted_messages(email, studentn, filename):
    """ Get the set of encrypted messages from the csv corresponding
    to a particular student

            Parameters:
                email str: email of the student
                studentn int: student number
                filename str: path of the csv file

            Returns:
                encrypted [str]: The list of encrypted messages (as
                    binary strings) corresponding to the student
    """
    reader = csv.reader(open(filename))

    indices = [md5(email, 100 * studentn + i) for i in range(200)]
    index_set = set(indices)

    encrypted_messages = []

    for row in reader:
        if row[0] in index_set:
            string = bitstring_to_string(row[1])
            encrypted_messages.append(string)

    return encrypted_messages


def cluster_indices_by_encription_key(encrypted_messages):
    """ Group messages that were probably encrypted using the same key

            Parameters:
                encrypted_messages ([str]): list of encrypted messages

            Returns:
                clusters [[str]]: A list of lists of strings, each list
                    is a set of encrypted messages that were probably
                    encrypted using the same key
    """
    total_messages = len(encrypted_messages)

    # Compute the similarity matrix for each pair of messages
    # In parallel, compute the average number of similaritys > 0.6
    # for each message, which should be similar to the number of keys
    similarity_matrix = []
    similar_messages_count = []

    for i in range(total_messages):
        similarity_matrix.append([])
        similar_count = 0
        for j in range(total_messages):
            similarity = probability_same_key(
                encrypted_messages[i],
                encrypted_messages[j]
            )
            similarity_matrix[i].append(similarity)
            if similarity > 0.65:
                similar_count += 1
        similar_messages_count.append(similar_count)

    n_keys = round(sum(similar_messages_count) / total_messages)

    # We apply a clustering algorithm based on the similarity matrix
    spectral = SpectralClustering(
        n_clusters=n_keys,
        affinity='precomputed'
    )

    spectral.fit(similarity_matrix)
    labels = spectral.labels_.copy()

    clusters = [[] for i in range(n_keys)]
    for i in range(len(labels)):
        clusters[labels[i]].append(i)
    return clusters


def get_key(encrypted_messages):
    """ Gets the key assuming all messages were encrypted using
        the same key.

            Parameters:
                encrypted_messages ([str]): list of encrypted messages

            Returns:
                key str: The the encryption key
    """

    # For every character of every message, compute the
    # probability of that character being a space
    total_messages = len(encrypted_messages)
    msg_len = len(encrypted_messages[0])

    # Cache the xors to avoid recomputation
    xor_matrix = []
    for msg1 in encrypted_messages:
        xors = []
        for msg2 in encrypted_messages:
            xors.append(xor(msg1, msg2))
        xor_matrix.append(xors)

    # Probability that in position i of message j there is
    # a space (i < j)
    probability_of_space = []
    for i in range(msg_len):
        probability_of_space.append([0] * total_messages)
        for j in range(total_messages):
            for k in range(total_messages):
                xor_msg_ints = [ord(c) for c in xor_matrix[j][k]]
                if 64 < xor_msg_ints[i] <= 90:
                    probability_of_space[i][j] += 1 / msg_len

    # Get the most likely space for each character, and based on
    # this get the corresponding character of the key
    key = ""
    for i in range(msg_len):
        index = argmax(probability_of_space[i])
        key += xor(encrypted_messages[index][i], " ")

    return key


def break_random_otp_round(encrypted_messages):
    clusters = cluster_indices_by_encription_key(encrypted_messages)

    # We start by mapping each key to the set of encrypted messages
    encrypted_key_map = {}
    for c in clusters:
        encrypted_cluster = [encrypted_messages[i] for i in c]
        key = get_key(encrypted_cluster)
        encrypted_key_map[key] = set(encrypted_cluster)

    # Let's now see which messages are apparently wrong for the found key
    wrong_messages = {}
    for key in encrypted_key_map:
        wrong_messages[key] = set()
        for msg in encrypted_key_map[key]:
            if count_irregular_chars(xor(key, msg)) >= len(msg) / 5:
                wrong_messages[key].add(msg)
        for msg in wrong_messages[key]:
            encrypted_key_map[key].remove(msg)

    # Now let's try to add wrong messages to existing validated keys
    # and store those that could not be decrypted
    still_missing = set()
    for key1 in wrong_messages:
        to_remove = set()
        for msg in wrong_messages[key1]:
            for key in encrypted_key_map:
                if count_irregular_chars(xor(key, msg)) < len(msg) / 5:
                    encrypted_key_map[key].add(msg)
                    to_remove.add(msg)
                else:
                    still_missing.add(msg)

        wrong_messages[key1] -= to_remove

    # finally remove those keys that are most likely wrong
    for key in wrong_messages:
        if len(wrong_messages[key]) > len(encrypted_key_map[key]) / 2:
            del encrypted_key_map[key]

    return encrypted_key_map, still_missing


def break_random_otp(encrypted_messages):
    print('Applying first round')
    encrypted_map, still_missing = break_random_otp_round(encrypted_messages)
    missing_prev_round = 0
    while len(still_missing) > missing_prev_round:
        print('Still hidden messages! Going for another round')
        missing_prev_round = len(still_missing)
        new_map, still_missing = break_random_otp_round(list(still_missing))
        encrypted_map.update(new_map)

    if still_missing:
        print(f'Did my best, could not decrypt {len(still_missing)} messages')
    else:
        print('Apparently all messages decrypted :-)')

    decrypted_map = {}
    for key in encrypted_map:
        decrypted_map[key] = [xor(key, msg) for msg in encrypted_map[key]]

    return decrypted_map


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('email', type=str, help='@uc.cl')
    parser.add_argument('studentn', type=int, help='UC student number')
    args = parser.parse_args()

    encrypted_messages = get_my_encrypted_messages(
        args.email,
        args.studentn,
        _FILE
    )

    decrypted = break_random_otp(encrypted_messages)
    pprint(decrypted)
