import sys
sys.path.append("/home/local/VANDERBILT/liy29/sumo-0.24.0/tools/")
import traci
import subprocess
import config
import os
from intersection import Intersection
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

import main
import time



def mytest(weThreshold, nsThreshold,
           paraList, intersection_name,
           intersectionIndex):
    #errorF = open("errorf.txt", 'w')
    port = config.generator_ports()
    sumoProcess = subprocess.Popen(
        ["sumo", "-c", "Scenarios_2\dsc.sumocfg", "--tripinfo-output", "tripinfo" + str(port) + ".xml",
         "--remote-port", str(port)], stdout= config.DEVNULL, stderr = config.DEVNULL)

    traci.init(port)
    intersections = config.generator_intersectionList(intersection_name, paraList)
    ins = intersections[intersectionIndex]
    ins.setThreshold(weThreshold, nsThreshold)

    for ele in intersections:
        ele.init()

    #time1 = time.time()
    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()
        for ele in intersections:
            ele.run()
#        for ele in intersections[intersectionIndex + 1:]:
#            ele.defaultRun()

    traci.close()
    sumoProcess.wait()


    return avgSpeed(port), weThreshold, nsThreshold

def avgDuration(port):
    xmlfile = open("tripinfo" + str(port) + ".xml", 'r')
    xmlTree = ET.parse(xmlfile)
    treeRoot = xmlTree.getroot()
    totalDuration = 0
    carNumber = len(treeRoot)
    for child in treeRoot:
        totalDuration += float(child.attrib['duration'])
    res = totalDuration * 1.0 / carNumber

    xmlfile.close()
    os.remove("tripinfo" + str(port) + ".xml")

    return res


def avgSpeed(port):
    xmlfile = open("tripinfo" + str(port) + ".xml", 'r')
    xmlTree = ET.parse(xmlfile)
    treeRoot = xmlTree.getroot()
    totalSpeed = 0
    carNumber = len(treeRoot)
    for child in treeRoot:
        totalSpeed += float(child.attrib['routeLength'])/float(child.attrib['duration'])
    avgspeed = totalSpeed * 1.0 / carNumber

    xmlfile.close()
    os.remove("tripinfo" + str(port) + ".xml")

    return avgspeed

if __name__ == '__main__':
    paraList = [(0,0), (0,0), (0,0), (0,0), (0,0)]
        
    print mytest(1, 1, paraList, config.smallMap, 0)
