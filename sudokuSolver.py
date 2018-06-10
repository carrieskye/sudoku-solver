#######
#
# POSITIONS
#
# Positions in a Sudoku roster are tuples consisting of the number of
# the row followed by the number of the column.
# Rows and columns are numbered starting from 0.
#
#######


def row(position):
    """ Return the row of the given position. """
    return position[0]
assert row((2, 3)) == 2




def col(position):
    """ Return the column of the given position. """
    return position[1]
assert col((2, 3)) == 3




def group(dimension, position):
    """
    Return the group to which the given position belongs in a roster
    of the given dimension.
    """
    return dimension*(position[0]//dimension) + (position[1]//dimension)
assert group(3, (2, 3)) == 1




#! The implementation of this method and the next 2 must use list comprehension.
#! All other methods may not use list comprehension
def row_positions(dimension, row):
    """
    Return the positions occupied by the given row in a roster of
    the given dimension.
    The resulting sequence contains the positions in ascending order.
  """
    row_positions = [(row,y) for y in range(dimension**2)]
    return row_positions
assert row_positions(2, 2) == [(2, 0), (2, 1), (2, 2), (2, 3)]




#! The implementation of this method must use list comprehension.
def col_positions(dimension, col):
    """
    Return the positions occupied by the given column in a roster
    of the given dimension.
    The resulting sequence contains the positions in ascending order.
  """
    col_positions = [(x, col) for x in range(dimension**2)]
    return col_positions
assert col_positions(3,7) == [(0, 7), (1, 7), (2, 7), (3, 7), (4, 7),
                              (5, 7), (6, 7), (7, 7), (8, 7)]




#! The implementation of this method must use list comprehension.
def group_positions(dimension, group):
    """
    Return the positions occupied by the given group in a roster
    of the given dimension.
    The resulting sequence contains the positions in ascending order.
  """
    first_row = (group//dimension)*dimension
    first_col = (group%dimension)*dimension
    group_positions = [(x, y) for x in xrange(first_row, first_row+dimension) for y in xrange(first_col, first_col+dimension)]
    return group_positions
assert group_positions(2, 3) == [(2, 2), (2, 3), (3, 2) ,(3, 3)]




def next_position(dimension, position):
    """
    Return the position next to the given position in a roster of the
    given dimension.
    If the given position is not at the end of a row, the position right to
    the given position is returned. Otherwise, the first position of the
    next row is returned. If that next row does not exist, None is returned.
  """
    row_nr = row(position)
    col_nr = col(position)
    if col_nr != ((dimension**2)-1):
        return (row_nr, col_nr+1)
    elif row_nr != ((dimension**2)-1):
        return (row_nr+1, 0)
    else:
        return None
assert next_position(3, (2, 3)) == (2, 4)
assert next_position(2, (2, 3)) == (3, 0)
assert next_position(3, (8, 8)) == None





#######
#
# ROSTERS: BASICS
#
# A Sudoku roster of dimension N consists of N**2 rows, N**2 columns
# and N**2 groups. The most common roster is a roster of dimension 3,
# which has 9 rows, 9 columns and 9 groups.
# Each cell of a roster can store an integer in the range from 1
# to the squared dimension of the roster.
#
#######


def make_roster(dimension=3, values=[]):
    """
    Return a new roster of the given dimension that is filled
    with the given values.
    The value at position K in the supplied sequence corresponds to
    the value at position [K/dimension**2,K%dimension**2] in the roster.
    Cells for which no value is supplied are filled with None. Values
    beyond the dimension of the roster are ignored.
  """
    roster = [[None]*dimension**2 for i in range(dimension**2)]
    row = 0
    value_number = 0
    while row <= dimension**2-1:
        # LOOP INVARIANT
        #   All the elements of all the rows handled so far
        #   have been filled with the corresponding value.
        col = 0
        while col <= dimension**2-1:
            # LOOP INVARIANT
            #   All the elements of the current row at all
            #   the columns handled so far have been filled
            #   with the corresponding value.
            if value_number < len(values):
                roster[row][col]=values[value_number]
            col += 1
            value_number += 1
        row += 1
    return roster




def make_roster_positionally(dimension=3, values=[]):
    """
    Return a new roster of the given dimension that is filled with the
    given values at the given positions.
    Each element in the sequence of values consists of a position
    and an integer number. If several of those elements involves the
    same position, the leftmost element applies.
  """
    roster = [[None]*dimension**2 for i in range(dimension**2)]
    value_number = len(values)-1
    while value_number >= 0:
        # LOOP INVARIANT
        #   All the elements of the list handled so far, that have
        #   a corresponding position in the roster that is to be
        #   filled in, have been assigned to the corresponding
        #   position in the roster and overwritten by a leftmore
        #   value in the list of values if more than one value
        #   occured for the same position.
        row = values[value_number][0][0]
        col = values[value_number][0][1]
        roster_value = values[value_number][1]
        if 0 <= row and row < dimension**2 and 0 <= col and col < dimension**2 and \
           0 < roster_value and roster_value <= dimension**2:
            roster[row][col]=values[value_number][1]
        value_number -= 1
    return roster

                                   



def dimension(roster):
    """
    Return the dimension of the given roster.
    The dimension of a roster is a positive integer number.
  """
    import math
    return int(math.sqrt(len(roster)))
roster = make_roster(2,\
            [   4,None,   3,None,\
                2,   1,None,   3,\
                1,None,None,None,\
                3,None,   2,None])
assert dimension(roster) == 2
roster = make_roster_positionally(3, [((1, 6), 1), ((2, 6), 7), ((3, 6), 2),\
         ((3, 7), 9), ((4, 8), 4), ((5, 1), 8), ((5, 2), 3), ((6, 6), 5)])
assert dimension(roster) == 3




def value_at(roster, position):
    """
    Return the value registered at the given position in the given roster.
    None is returned if no value is registered at the given position.
  """
    return roster[position[0]][position[1]]
roster = make_roster(2,\
            [   4,None,   3,None,\
                2,   1,None,   3,\
                1,None,None,None,\
                3,None,   2,None])
assert value_at(roster,(0,0))== 4
assert value_at(roster,(0,2)) == 3
assert value_at(roster,(1,3)) == 3
assert value_at(roster,(3,3)) == None
roster = make_roster_positionally(3, [((1, 6), 1), ((2, 6), 7), ((3, 6), 2),\
         ((3, 7), 9), ((4, 8), 4), ((5, 1), 8), ((5, 2), 3), ((6, 6), 5)])
assert value_at(roster, (3, 6))== 2
assert value_at(roster,(6, 6))== 5
assert value_at(roster, (0, 0)) == None
assert value_at(roster, (8, 8)) == None




def set_value_at(roster, value, position):
    """
    Set the given value at the given position in the given roster.
  """
    roster[position[0]][position[1]] = value
    pass
roster = make_roster()
set_value_at(roster, 3, (2, 4))
assert value_at(roster, (2, 4)) == 3

roster = make_roster_positionally(3, [((8,8), 1)])
set_value_at(roster, 2, (8, 8))
assert value_at(roster, (8, 8)) == 2
                                 
                                



#######
#
# ROSTERS: INSPECTION
#
#
#######


def is_filled_at(roster, pos):
    """
    Check whether a value is registered at the given position in
    the given roster.
  """
    if roster[pos[0]][pos[1]] == None:
        return False
    else:
        return True
roster = make_roster(2,\
            [   4,None,   3,None,\
                2,   1,None,   3,\
                1,None,None,None,\
                3,None,   2,None])
assert not is_filled_at(roster, (1, 2))
assert is_filled_at(roster, (3, 2))



def is_completely_filled(roster):
    """
    Check whether the given roster is completely filled.
  """
    for row in range(len(roster)):
        # LOOP INVARIANT
        #   All the elements of all the rows handled so far
        #   have been checked for elements.
        for col in range(len(roster)):
            # LOOP INVARIANT
            #   All the elements of the current row at all
            #   the columns handled so far have been checked
            #   for elements.
            if roster[row][col] == None:
                return False
    else:
        return True
roster = make_roster(2,\
            [   4,None,   3,None,\
                2,   1,None,   3,\
                1,None,None,None,\
                3,None,   2,None])
assert not is_completely_filled(roster)




def candidates_at(roster, position):
    """
    Return the set of all values that can be registered at the given position
    in the given roster, such that the roster still obeys the Sudoku rules.
    The empty set is returned if the cell at the given position is filled.
  """
    list_of_values=[]
    set_of_values=([])
    if is_filled_at(roster, position):
        return set_of_values
    dim = dimension(roster)
    row_nr = row(position)
    row_pos = row_positions(dim, row_nr)
    col_nr = col(position)
    col_pos = col_positions(dim, col_nr)
    group_nr = group(dim, position)
    group_pos = group_positions(dim, group_nr)
    for i in xrange(1, len(roster)+1):
        # LOOP INVARIANT
        #   All the possible values of the roster handled so far
        #   have been compared to all the values that have been
        #   filled in on the row, column and group of the given
        #   position. If the comparisons proved that the value
        #   didn't occur in the row, column or group yet, the
        #   value has been added to the list of candidates.
        found_i = False
        for j in range(len(roster)):
            # LOOP INVARIANT
            #   All the values at the row positions, column
            #   positions and group positions handled so far,
            #   have been compared to value i.
            if value_at(roster,row_pos[j]) == i:
                found_i = True
            elif value_at(roster, col_pos[j]) == i:
                found_i = True
            elif value_at(roster, group_pos[j]) == i:
                found_i = True
        if not found_i:
            list_of_values.extend([i])
            set_of_values = set(list_of_values)
    return set_of_values

roster = make_roster(2,\
            [   4,None,   3,None,\
                2,   1,None,   3,\
                1,None,None,None,\
                3,None,   2,None])
assert candidates_at(roster,(2,1)) == {2,4}





def row_candidates(roster, row):
    pos = (row,0)
    dim = dimension(roster)
    row_pos = row_positions(dim, row)
    row_candidates = []
    i = 0
    while i < len(roster):
        # LOOP INVARIANT
        #   All the candidates at the row positions handled
        #   so far, have been added to a list that returns
        #   these candidates with their corresponding position.
        if value_at(roster, row_pos[i]) == None:
            candidates = list(candidates_at(roster, row_pos[i]))
            for j in range(len(candidates)):
                # LOOP INVARIANT
                #   All the candidates of the current row position
                #   handled so far, have been added to the list with
                #   row candidates, along with their corresponding position.
                row_candidates.extend([[candidates[j], row_pos[i]]])
        i += 1
    return row_candidates




def col_candidates(roster, col):
    pos = (0,col)
    dim = dimension(roster)
    col_pos = col_positions(dim, col)
    col_candidates = []
    i = 0
    while i < len(roster):
        # LOOP INVARIANT
        #   All the candidates at the column positions handled
        #   so far, have been added to a list that returns
        #   these candidates with their corresponding position.
        if value_at(roster, col_pos[i]) == None:
            candidates = list(candidates_at(roster, col_pos[i]))
            for j in range(len(candidates)):
                # LOOP INVARIANT
                #   All the candidates of the current column position
                #   handled so far, have been added to the list with
                #   column candidates, along with their corresponding position.
                col_candidates.extend([[candidates[j], col_pos[i]]])
        i += 1
    return col_candidates




def group_candidates(roster, group):
    dim = dimension(roster)
    group_pos = group_positions(dim, group)
    pos = group_pos[0]
    group_candidates = []
    i = 0
    while i < len(roster):
        # LOOP INVARIANT
        #   All the candidates at the group positions handled
        #   so far, have been added to a list that returns
        #   these candidates with their corresponding position.
        if value_at(roster, group_pos[i]) == None:
            candidates = list(candidates_at(roster, group_pos[i]))
            for j in range(len(candidates)):
                # LOOP INVARIANT
                #   All the candidates of the current group position
                #   handled so far, have been added to the list with
                #   group candidates, along with their corresponding position.
                group_candidates.extend([[candidates[j], group_pos[i]]])
        i += 1
    return group_candidates




#######
#
# ROSTERS: CORRECTNESS
#
#
#######


### PROVIDE THE COMPLEXITY OF THIS METHOD.
def is_correct_sequence(seq):
    """
    Check whether the given sequence does not contain
    the same value (except for None) more than once,
    and whether it only contains (1) integer values between 1
    and the length of the given sequence and/or (2) the special value None.
  """
    for i in range(len(seq)):
        # LOOP INVARIANT
        #   All the elements of the sequence handled so far
        #   have been checked on not extending the minimum value:
        #   1, and the maximum value: the length of the sequence.
        if seq[i] != None:
            if seq[i] < 0 or seq[i] > len(seq):
                return False
    seq2 = list(seq)
    seq2.sort()
    for i in range(len(seq2)-1):
        # LOOP INVARIANT
        #   All the elements of the sorted sequence handled
        #   so far, have been checked on not being equal to
        #   the element that follows them.
        if seq2[i] != None:
            if seq2[i] == seq2[i+1]:
                return False
    else:
        return True
    
assert not is_correct_sequence((4, "abc", None, -17, None, "xyz"))
assert not is_correct_sequence((1, 2, 1))
assert is_correct_sequence((None, None, 4, 1))

# COMPLEXITY
#
# Best case scenario: T(n) = 3.
#   The first value to be checked does not lie in between 1 and the
#   length of the sequence. In that case, seq[i] is only used three
#   times. Therefor the complexity is 3.
#
# Worst case scenario: T(n) = 3n + 3(n-1) = O(n).
#   The worst case scenario in this algorithm, is when it has to
#   return True. In that case, all the values of the sequence have
#   to go through all the comparisons. For the first i-loop, seq[i]
#   is used 3 times and we go as many times through it as the
#   length of the sequence. The complexity is 2n. For the second
#   i-loop, seq[i] is also used three times. We go through the loop
#   one less time, because the last comparison will be between the
#   one but last and its next element (the last one), which is why
#   the last element is already checked after this comparison. The
#   complexity of this loop therefor equals 2(n-1). 



### PROVIDE THE COMPLEXITY OF THIS METHOD IN TERMS OF
### THE DIMENSION OF THE ROSTER.
def is_correct_roster(roster):
    """
    Check whether the given roster is correctly filled with values,
    according to the rules of Sudoku. Either no value is registered
    at a position, or the value registered there does not occur at other
    positions in the same row, the same column nor the same group.
  """
    dim = dimension(roster)
    row_seq = []
    col_seq = []
    group_seq = []
    for row in range(len(roster)):
        # LOOP INVARIANT
        #   All the values on all the row positions of all the
        #   rows handled so far, have been added to a sequence,
        #   that has for every row been checked on being a
        #   correct sequence.
        row_pos = row_positions(dim, row)
        i = 0
        for i in range(len(roster)):
            # LOOP INVARIANT
            #   All the values of the current row on all the row
            #   positions handled so far, have been added to a
            #   sequence.
            value = value_at(roster, row_pos[i])
            row_seq.extend([value])
        if is_correct_sequence(row_seq) == False:
            return False
        else:
            row_seq=[]
    for col in range(len(roster)):
        # LOOP INVARIANT
        #   All the values on all the column positions of all the
        #   columns handled so far, have been added to a sequence,
        #   that has for every column been checked on being a
        #   correct sequence.
        col_pos = col_positions(dim, col)
        i = 0
        for i in range(len(roster)):
            # LOOP INVARIANT
            #   All the values of the current column on all the column
            #   positions handled so far, have been added to a
            #   sequence.
            value = value_at(roster, col_pos[i])
            col_seq.extend([value])
        if is_correct_sequence(col_seq) == False:
            return False
        else:
            col_seq=[]
    for group in range(len(roster)):
        # LOOP INVARIANT
        #   All the values on all the group positions of all the
        #   groups handled so far, have been added to a sequence,
        #   that has for every group been checked on being a
        #   correct sequence.
        group_pos = group_positions(dim, group)
        i = 0
        for i in range(len(roster)):
            # LOOP INVARIANT
            #   All the values of the current group on all the group
            #   positions handled so far, have been added to a
            #   sequence.
            value = value_at(roster, group_pos[i])
            group_seq.extend([value])
        if is_correct_sequence(group_seq) == False:
            return False
        else:
            group_seq=[]
    else:
        return True
    
assert is_correct_roster(make_roster(2,\
            [   4,None,   3,None,\
                2,   1,None,   4,\
                1,   4,None,None,\
                3,   2,   4,   1]))
assert not is_correct_roster(make_roster(2,\
            [   4,   3,None,None,\
                2,   1,None,None,\
                1,None,None,   1,\
                3,None,None,None]))

# COMPLEXITY
#
# Best case scenario: T(n) = 3(n**2) = O(n**2).
#   All values of the first row of the roster have been added
#   to a seq who appears to be incorrect. The complexity therefor
#   equals the length of the row, which in terms of the dimension
#   of the roster equals n**2, times the complexity of the worst
#   case scenario of the correct sequence function, which is 3.
#   
#
# Worst case scenario: T(n) = 3n**2(n**2+3n+3(n-1)) = O(n**4).
#   In the worst case, the algorithm returns True, in which case
#   all the rows, columns and groups have to be checked. It will
#   go through the 3 big loops: the row-loop, the column-loop and
#   the group-loop, who all have the same complexity: n**2(n**2+3n+3(n-1).
#   n**2 is for the for-loop in each one of these big groups, and
#   3n + 3(n-1) is for the worst case of the correct sequence
#   function (which is necessary to return True). The complexity
#   of the worst case scenario therefor equals 3n**2(n**2+3n+3(n-1)).



#######
#
# ROSTERS: DISPLAY
#
#
#######

def roster_contents(roster):
    """
    Return a linearized roster (as a list), containing integer values
    when a particular position has one assigned value, and otherwise a list
    that contains the candidate values for that position.
    The linearization is done row by row.
  """
    pos = (0,0)
    dim = dimension(roster)
    roster_contents = [None]*(len(roster)**2)
    i = 0
    while pos != None:
        # LOOP INVARIANT
        #   All the values on the completed positions handled
        #   so far and the candidates on the positions handled
        #   that do not have a value yet, have been added to the
        #   list with roster contents.
        if value_at(roster, pos) != None:
            roster_contents[i] = value_at(roster,pos)
        else:
            roster_contents[i] = list(candidates_at(roster, pos))
        pos = next_position(dim, pos)
        i += 1
    return roster_contents
roster = make_roster(2,\
            [   4,None,None,None,\
                2,   1,None,   3,\
                1,None,None,None,\
                3,None,   2,None])
assert roster_contents(roster) == [4, [3], [1], [1, 2],
                                   2, 1, [4], 3,
                                   1, [2, 4], [3, 4], [4],
                                   3, [4], 2, [1, 4]]


          

#! This function can be used to easily inspect rosters
def print_roster(roster):
    """
    Print the given roster one row per line.
    Each value is printed in a field of 3 characters wide.
  """
    for row in range(0, dimension(roster) ** 2):
        # LOOP INVARIANT
        #   All the elements of all the rows handled so far
        #   have been printed on successive lines.
        for col in range(0, dimension(roster) ** 2):
            # LOOP INVARIANT
            #   All the elements of the current row at all
            #   the columns handled so far have been printed
            #   on the current line.
            if is_filled_at(roster, (row, col)):
                print '%(val)3d' % {"val": value_at(roster, (row, col))},
            else:
                print '  -',
        print





##############################################
#
# ROSTERS: NUMBER OF SOLUTIONS
#
################################################


# THIS SHOULD BE A RECURSIVE FUNCTION
def nb_solutions(roster, start_pos=(0,0)):
    """
    Return the total number of possible ways that the given roster
    can be filled completely. Each of these solutions must satisfy
    the rules of Sudoku.
  """
    if is_completely_filled(roster) and is_correct_roster(roster):
        return 1
    dim = dimension(roster)
    pos = start_pos
    number_of_solutions = 0
    while value_at(roster,pos) != None:
        # LOOP INVARIANT
        #   At all the positions handled so far, on which
        #   the value is already known, the next position
        #   has become the new position.
        pos = next_position(dim, pos)
    i = 0
    for i in xrange(1, len(roster)+1):
        # LOOP INVARIANT
        #   All the values of the roster handled so far have
        #   been checked on maken the roster incorrect while
        #   filled in on the last handled emtpy position.
        set_value_at(roster, i, pos)
        if is_correct_roster(roster):
            number_of_solutions += nb_solutions(roster, pos)
    set_value_at(roster, None, pos)
    return number_of_solutions
roster = make_roster(2,\
            [   4,None,   3,None,\
             None,None,None,None,\
             None,None,None,None,\
             None,   2,None,None])
assert nb_solutions(roster) == 3




##############################################
#
# ROSTERS: FILL INTELLIGENTLY
#
################################################

	
def get_first_naked_single(roster, start_pos=(0,0)):
    """
    Return the position and the value of the first naked single in
    the given roster starting from the given position.
    A naked single is a non-filled cell in which ony one value can be filled in
    in order for the roster to stay correct. Other values are impossible
    because they already occur in the row, the column or the group to
    which the cell belongs.
    None is returned if no naked single exists starting from
    the given position.
  """
    pos = start_pos;
    dim = dimension(roster)
    while pos != None:
        # LOOP INVARIANT
        #   The number of candidates on all the positions
        #   checked so far has been checked on being equal
        #   to 1, which would prove that at that position,
        #   there would only be one candidate (the naked single).
        candidates = list(candidates_at(roster, pos))
        if len(candidates) == 1:
            return pos, candidates[0]
        else:
            pos = next_position(dim, pos)
    return None




def search_hidden_single(dim, candidate_list):
    for j in xrange(1, dim**2):
        # LOOP INVARIANT
        #   All the values of the roster handled so far
        #   have been checked on being the first value
        #   that only occurs once in the candidate list.
        count_value_j = 0
        for k in range(len(candidate_list)):
            # LOOP INVARIANT
            #   All the values of the candidate list handled
            #   so far that equaled the current value for j
            #   have been counted and checked on being equal to 1.
            if candidate_list[k][0] == j:
                count_value_j += 1
                if count_value_j == 1:
                    pos_j = candidate_list[k][1]
        if count_value_j == 1:
            return pos_j, j
    return None




def get_first_hidden_single(roster, start_pos=(0,0)):
    """
    Return the position and the value of the first hidden single in
    the given roster starting from the given position.
    A hidden single is a non-filled cell which is forced to
    take a specific value, because that value is not yet present in
    the associated group, row, or column, and due to the placement of
    the other values, there are no alternative positions left for
    that value to take.
    None is returned if no hidden single exists starting from
    the given position.
  """
    dim = dimension(roster)
    row_nr = row(start_pos)
    col_nr = col(start_pos)
    group_nr = group(dim, start_pos)
    for i in xrange(row_nr, dim**2):
        # LOOP INVARIANT
        #   All the candidates on the row positions of the
        #   current row handled so far, have been checked on
        #   having a hidden single. 
        row_can = row_candidates(roster, i)
        hidden_single = search_hidden_single(dim, row_can)
        if hidden_single != None:
            return hidden_single
    for i in xrange(col_nr, dim**2):
        # LOOP INVARIANT
        #   All the candidates on the column positions of the
        #   current column handled so far, have been checked on
        #   having a hidden single. 
        col_can = col_candidates(roster, i)
        hidden_single = search_hidden_single(dim, col_can)
        if hidden_single != None:
            return hidden_single
    for i in range(group_nr, dim**2):
        # LOOP INVARIANT
        #   All the candidates on the group positions of the
        #   current group handled so far, have been checked on
        #   having a hidden single. 
        group_can = group_candidates(roster, i)
        hidden_single = search_hidden_single(dim, group_can)
        if hidden_single != None:
            return hidden_single
    return None
roster = make_roster(2,\
            [   4,None,None,None,\
                2,   1,None,   3,\
                1,None,None,None,\
                3,None,   2,None])
assert get_first_naked_single(roster) == ((0, 1), 3)
roster = make_roster(2,\
            [   4,   3,   1,   2,\
                2,   1,   4,   3,\
                1,None,None,None,\
                3,None,   2,None])
assert get_first_hidden_single(roster,(0,0)) == ((2, 1), 2)
assert get_first_naked_single(roster) == ((2, 2), 3)




def min_candidate(roster):
    """
    Return 
  """
    dim = dimension(roster)
    min_candidate = len(roster)+1
    pos = (0,0);
    while pos != None:
        # LOOP INVARIANT
        #   The number of candidates on the positions handled
        #   so far has been checked on being smaller than the
        #   smallest number of candidates found on a position
        #   so far.
        candidates = candidates_at(roster, pos)
        if len(candidates) < min_candidate and value_at(roster, pos) == None:
            min_candidate = len(candidates)
            min_pos = pos
        pos = next_position(dim, pos)
    return min_pos
    


# THIS SHOULD BE A RECURSIVE FUNCTION
def fill_intelligently(roster, is_visualizing = False, sudoku_gui = None):
    """
    Fill the given roster completely by exploiting naked singles and hidden
    singles as much as possible. At times that there are no hidden singles
    nor naked singles in the roster, filling proceeds with a cell with the
    least number of candidates.
    The function returns True if its was able to work out a complete fill.
    In that case, the state of the roster is changed to reflect the fill.
    If a complete fill is impossible, the function returns False and leaves the
    given roster untouched.
  """
    # when is_visualizing is True, the provided sudoku_gui will receive
    # the subsequent (recursive) roster contents which will be used
    # to visualize the algorithm step-by-step once the algorithm has finished
    if is_visualizing:
        sudoku_gui.update_roster(roster_contents(roster))
    pass

    """
    The function min_candidate(roster) returns the position at which the
    number of candidates is the least. This is the position that needs to be
    filled in first. min_can gives the list of the candidates at this position.
    If this list is empty, the roster contains a wrong value. Therefor no
    solution is found. If the length equals one, there's at least one naked
    single in the roster. In that case, the naked single must be filled in.
    If no naked single can be found (when the length of min_can is greater than
    one), the roster needs to be checked for hidden singles. If a hidden single
    can be found, the hidden single must be filled in. If not, the shortest list
    of candidates is used to fill the roster. 
  """
    if is_completely_filled(roster) and is_correct_roster(roster):
        return True
    solution_found = False
    pos_to_fill = min_candidate(roster)
    min_can = list(candidates_at(roster, pos_to_fill))
    if len(min_can) == 0:
        return False
    elif len(min_can) == 1:
        naked_single = get_first_naked_single(roster)
        pos_to_fill = naked_single[0]
        set_value_at(roster, naked_single[1], pos_to_fill)
        solution_found = fill_intelligently(roster, is_visualizing, sudoku_gui)
    else:
        hidden_single = get_first_hidden_single(roster)
        if hidden_single != None:
            pos_to_fill = hidden_single[0]
            set_value_at(roster, hidden_single[1], pos_to_fill)
            solution_found = fill_intelligently(roster, is_visualizing, sudoku_gui)
        else:
            for i in range(len(min_can)):
                # LOOP INVARIANT
                #   The candidates at the current position handled
                #   so far have been checked.
                if not solution_found:
                    set_value_at(roster, min_can[i], pos_to_fill)
                    solution_found = fill_intelligently(roster, is_visualizing, sudoku_gui)
    if not solution_found:
        set_value_at(roster, None, pos_to_fill)
    return solution_found
roster = make_roster(2,
            [1,   None,None,None,\
             None,2,   None,None,\
             None,None,3,   None,\
             None,None,None,4])
assert fill_intelligently(roster, False, None)
roster = make_roster(2,\
            [1,   None,None,None,\
             None,2,   None,None,\
             2,   None,3,   None,\
             None,None,1,   4])
assert not fill_intelligently(roster, False, None)

