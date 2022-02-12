# Problem Set 4A


def get_permutations(sequence):
    '''
    Enumerate all permutations of a given string

    sequence (string): an arbitrary string to permute. Assume that it is a
    non-empty string.  

    You MUST use recursion for this part. Non-recursive solutions will not be
    accepted.

    Returns: a list of all permutations of sequence

    Example:
    >>> get_permutations('abc')
    ['abc', 'acb', 'bac', 'bca', 'cab', 'cba']

    Note: depending on your implementation, you may return the permutations in
    a different order than what is listed here.
    '''
    if len(sequence) == 1:
        return [sequence]

    final_word = []

    for count , letter in enumerate(sequence):
        final_word +=  [letter +
                       left_letter for left_letter in get_permutations(sequence[ :count] + sequence[count+1:])]

    return final_word

if __name__ == '__main__':
#    #EXAMPLE
#    example_input = 'abc'
#    print('Input:', example_input)
#    print('Expected Output:', ['abc', 'acb', 'bac', 'bca', 'cab', 'cba'])
#    print('Actual Output:', get_permutations(example_input))
    
#    # Put three example test cases here (for your sanity, limit your inputs
#    to be three characters or fewer as you will have n! permutations for a 
#    sequence of length n)

    example_input = 'abc'
    print('Input:', example_input)
    print('Expected Output:', ['abc', 'acb', 'bac', 'bca', 'cab', 'cba'])
    print('Actual Output:', get_permutations(example_input))

    example_input = 'fire'
    print('Input:', example_input)
    print(len(get_permutations(example_input)))
    print('Actual Output:', get_permutations(example_input))

    example_input = 'cat'
    print('Input:', example_input)
    print('Expected Output:', ['cat', 'cta', 'act', 'atc', 'tca', 'tac'])
    print('Actual Output:', get_permutations(example_input))

