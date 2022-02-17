import unittest

#TODO: investigate multithreading so running all the tests does not take so long, gather a few more cases

def placeholder(video_url):
    return 0

#
# Test cases to test functionality of counting algorithm. Clips are short (<45 seconds) and should each
# demonstrate something (different) that can happen in a complete video 
#

class TestCountAlgorithm(unittest.TestCase):

    #There was some playing of the bats by the door, but only 1 left
    def test_video1(self):
        self.assertEqual(placeholder('test_videos/1.mp4'), -1)
    
    #There was a lot of playing by multiple bats
    def test_video2(self):
        self.assertEqual(placeholder('test_videos/2.mp4'), 0)
    
    #A fox walks in and out of the region of interest
    def test_video3(self):
        self.assertEqual(placeholder('test_videos/3.mp4'), 0)
    
    #One bat leaves by going in and out multiple times
    def test_video4(self):
        self.assertEqual(placeholder('test_videos/4.mp4'), -1)
    
    #The two leave with some playing, in and out region of interest
    def test_video5(self):
        self.assertEqual(placeholder('test_vidoes/5.mp4'), -2)
    
    #1 enters and 1 exits, so the counter should even itself out
    def test_video6(self):
        self.assertEqual(placeholder('test_videos/6.mp4'), 0)
     
if __name__ == '__main__':
    unittest.main()