from collections import deque

def LCS(s1, s2):
    n = len(s1)
    m = len(s2)
    array = [False] * (m + 1)
    Q = deque()
    matching_number = 0
    temporary = 0
    previous_value = 0
    end_pos = 0
    
    for i in range(n + 1):
        for j in range(temporary, m + 1):
            if i == 0 or j == 0:
                if i == 0:
                    Q.append(0)
                if j == 0:
                    Q.append(0)
            else:
                if s1[i-1] == s2[j-1]:
                    diag = Q.popleft()
                    previous_value = diag + 1
                    Q.append(previous_value)
                    
                    if previous_value > matching_number:
                        temporary = j
                        array[j] = True
                        matching_number = previous_value
                        end_pos = j
                        
                        if j == n - 1:
                            substring = s2[end_pos - matching_number:end_pos]
                            return matching_number, substring
                else:
                    diag = Q.popleft()
                    vertical_value = Q[0] if Q else 0
                    temp = max(previous_value, vertical_value)
                    previous_value = temp
                    Q.append(previous_value)
                
                if j == m:
                    if Q:
                        Q.popleft()
    
    if matching_number > 0:
        substring = s2[end_pos - matching_number:end_pos]
    else:
        substring = ""
    
    return matching_number, substring


def making_a_short_string(A, B, start, end):
    if end - start <= 4:
        substring = A[start:end+1]
        return LCS(substring, B)
    
    mid = (start + end) // 2
    left_length, left_substring = making_a_short_string(A, B, start, mid)
    right_length, right_substring = making_a_short_string(A, B, mid + 1, end)
    total_length = left_length + right_length
    combined_substring = left_substring + right_substring
    return total_length, combined_substring


def lcs_dc_dp(A, B):
    if not A or not B:
        return 0, ""
    
    n = len(A)
    length, substring = making_a_short_string(A, B, 0, n - 1)
    
    return length, substring