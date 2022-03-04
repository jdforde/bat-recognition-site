from concurrent.futures import ThreadPoolExecutor
import time

def placeholder(video_url):
    return (0, 0)

#
# Test cases to test functionality of counting algorithm. Clips are short (<45 seconds) and should each
# demonstrate something (different) that can happen in a complete video, Note that it's (num_enetered, num_exited)
#

def TestVideo(video_num, count_tuple):
    start_time = time.time()
    response = placeholder('videos/' + str(video_num) + '.mp4')
    if (response == count_tuple):
        print('SUCCESS: Test case {} passed'.format(video_num))
        print('Finished test case {} in {:.2f} seconds'.format(video_num, time.time() - start_time))
        return True
    else:
        print('FAILURE: Test case {} did not pass. Expected {} but got {}'.format(video_num, count_tuple, response))
        print('Finished test case {} in {:.2f} seconds'.format(video_num, time.time() - start_time))
        return False
    
    

def ThreadedTests():
    start_time = time.time()
    print('=========================\nRunning Test Cases:\n')

    # CORRECT_RESPONSES represents the tuples that the algorithm should get for each video. For 
    # example (0, 1) corresponds to test video 4 where 0 bats entered and 1 exited
    CORRECT_RESPONSES = [(0, 1), (0, 0), (0, 0), (0, 1), (0, 2), (1, 1), (1, 0), (0, 1)] 
    NUM_WORKERS = 4 #Might want to experiment with this

    futures = []
    with ThreadPoolExecutor(max_workers=NUM_WORKERS) as executor:
        for i in range(1, 7):
            future = executor.submit(TestVideo, i, CORRECT_RESPONSES[i-1])
            futures.append(future)
    

    print('\n\n\n=========================\nFinal Results:\n')
    failure = False
    for res in futures:
        if res.result() == False:
            print('FAILURE: some test cases did not pass')
            failure = True
            break
    
    if not failure:
        print('SUCCESS: All test cases passed!')
    
    print('Finished running all test cases in {:.2f} seconds\n\n'.format(time.time() - start_time))
        
if __name__ == '__main__':
    ThreadedTests()