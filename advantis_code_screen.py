# count the number of pairs in a list of integers that have a difference of k


def solution(k, a):  # 3, [1, 2, 4, 6, 8, 9, 12]
    #                               1
    #                                  2
    a = sorted(a)
    pointer1 = 0
    pointer2 = 0
    diff = a[pointer2] - a[pointer1]
    count = 0
    # repeat until right pointer at the end and diff is less than k
    while pointer2 < len(a) and pointer1 < len(a):
        val1 = a[pointer1]
        consecutive_val1 = count_consecutive(a, pointer1)
        val2 = a[pointer2]
        consecutive_val2 = count_consecutive(a, pointer2)
        diff = val2 - val1
        # if diff == k, add that pair, then move both pointers right assuming unique values
        if diff == k:
            count += consecutive_val1 * consecutive_val2
            pointer1 += consecutive_val1
            pointer2 += consecutive_val2
        # if diff < k, move right pointer right
        elif diff < k:
            pointer2 += 1
        # if diff > k, move left pointer right
        else:
            pointer1 += 1
    return count


def count_consecutive(list, index):
    count = 1
    while index < len(list) - 1 and list[index] == list[index + 1]:
        count += 1
        index += 1
    return count


print("solution answer:", solution(3, [1, 1, 2, 4, 4, 7]))  # answer should be 6
