from Utils.utils import find_nearest_food, DDX, isValid


def BFS(_map, start_row, start_col, end_row, end_col, N, M):
    visited = [[False for _ in range(M)] for _ in range(N)]
    trace = [[[-1, -1] for _ in range(M)] for _ in range(N)]

    lt = []
    chk = False
    visited[start_row][start_col] = True
    lt.append([start_row, start_col])
    
    while len(lt) > 0:
        [row, col] = lt.pop(0)

        if [row, col] == [end_row, end_col]:
            chk = True
            break

        for [d_r, d_c] in DDX:
            new_row, new_col = row + d_r, col + d_c
            if isValid(_map, new_row, new_col, N, M) and not visited[new_row][new_col]:
                visited[new_row][new_col] = True
                lt.append([new_row, new_col])
                trace[new_row][new_col] = [row, col]

    if not chk:
        return start_row, start_col  # Không tìm thấy đường đi

    while trace[end_row][end_col] != [-1, -1]:
        next_row, next_col = end_row, end_col
        end_row, end_col = trace[end_row][end_col]
    return next_row, next_col