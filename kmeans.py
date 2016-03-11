# CMSC 12300 - Computer Science with Applications 3
# Borja Sotomayor, 2013
#

import sys
import random
import numpy
import pickle
import fibonacci
import kmeans_centeroid_selector
from mrjob.job import MRJob
from kmeans_centeroid_selector import MRKMeansChooseInitialCentroids
#from kmeans_centroid_selector import *
from kmeans_centeroid_updater import MRKMeansUpdateCentroids

def extract_centroids(job, runner):
    c = []
    for line in runner.stream_output():
        key, value = job.parse_output_line(line)
        #print "extract_centeroids"
        print key, value
        c.append(value)
        #print "c:", c
    return c

# If we were running on AWS, we would simply write the centroids
# to an S3 bucket, and then read them from the jobs.
def write_centroids_to_disk(centroids, fname):
    f = open(fname, "w+")
    #print "Inside write_centroids_to_disk:", centroids
    #print "file_name:",fname 
    pickle.dump(centroids, f)
    f.close()

def get_biggest_diff(centroids,new_centroids):
    print "Centeroids:", centroids
    print "New Centeroids:", new_centroids
    distances = [numpy.linalg.norm(numpy.array(c1) - c2) for c1,c2 in zip(centroids,new_centroids)]
    max_d = max(distances)
    return max_d

CENTROIDS_FILE="/home/srikar/Data/Map_Reduce/kmeans.centroids"

if __name__ == '__main__':
    args = sys.argv[1:]

    choose_centroids_job = MRKMeansChooseInitialCentroids(args=args)
    with choose_centroids_job.make_runner() as choose_centroids_runner:
        choose_centroids_runner.run()

        centroids = extract_centroids(choose_centroids_job, choose_centroids_runner)
        print "Initial Centeroids:", centroids
        write_centroids_to_disk(centroids, CENTROIDS_FILE)

        i = 1
        while True:
            print "Iteration #%i" % i
            update_centroids_job = MRKMeansUpdateCentroids(args=args + ['--centroids='+CENTROIDS_FILE])
            with update_centroids_job.make_runner() as update_centroids_runner:
                update_centroids_runner.run()

                new_centroids = extract_centroids(update_centroids_job, update_centroids_runner)
                print "New Centroids:", new_centroids
                write_centroids_to_disk(new_centroids, CENTROIDS_FILE)

                diff = get_biggest_diff(centroids, new_centroids)
                print "Difference:", diff
                if diff > 0.001:
                    centroids = new_centroids
                else:
                    break

                i+=1
