from time import time

def print_time(next_process: str, spec='') -> None:
    global super_time_start
    global time_start
    if spec == 'first':
        super_time_start = time()
        print(next_process + '...', end='\t')
    elif spec == 'last':
        print('%.4fs\nDone. (total: %.4fs)' % (time() - time_start, time() - super_time_start))
    else:
        print('%.4fs\n%s...' % (time() - time_start, next_process), end='\t')
    time_start = time()