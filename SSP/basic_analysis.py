import sys, run
THRESHOLD = 10
try:
    import psyco
    psyco.full()
except:
    print "psyco not found - running without optimization"
print sys.argv
run.main("basic_analysis",sys.argv,THRESHOLD)
