
import statistics

task1 = [3, 22, 11, 9, 100, 70, 24, 12, 11, 90]

def print_task_info(tasks):
    numberOfJobs = len(tasks)
    totalBurstTime = sum(tasks)
    averageBurstTime = sum(tasks)/len(tasks)
    standardDeviation = statistics.stdev(tasks)
    minBurst = min(tasks)
    maxBurst = max(tasks)

    print(f"""Number of jobs: {numberOfJobs}\nTotal Burst Time: {totalBurstTime}\nMin Burst Time: {minBurst}\nMax Burst Time: {maxBurst}\nAverage Burst Time: {averageBurstTime:.2f}\nStandard Deviation: {standardDeviation:.2f}""")
    return


def round_robin(tasks, quantum, contextSwitchTime):

    tasksCopy = tasks[:]
    totalRuntime = 0
    totalSwitches = 0
    initial_burst = tasks[:]
    turnAroundTimes = [0] * len(tasks)
    waitTimes = [0] * len(tasks)
    responseTime = [0] *len(tasks)
    k = 0    #k is used to track if it's the first time a task has had CPU access, to calculate response time
    
    while any( task > 0 for task in tasksCopy):
        for i in range(len(tasksCopy)):
            if tasksCopy[i] > 0:
                #task has more than one quantum left
                if tasksCopy[i] - quantum > 0:
                    if k == 0:
                        responseTime[i] = totalRuntime                 
                    tasksCopy[i] -= quantum
                    totalRuntime += quantum
                    totalRuntime += contextSwitchTime
                    totalSwitches += 1
                    
                #task gets to 0 in this quantum
                else:
                    if k == 0:
                        responseTime[i] = totalRuntime
                    totalRuntime += tasksCopy[i]
                    totalRuntime += contextSwitchTime
                    tasksCopy[i] = 0
                    turnAroundTimes[i] = totalRuntime
                    totalSwitches += 1

                
        k = 1
    
    for i in range(len(tasks)):
        waitTimes[i] = turnAroundTimes[i] - initial_burst[i]


    idleTime = totalRuntime - sum(initial_burst)
    avgWait = sum(waitTimes)/len(waitTimes)
    avgTurnAround = sum(turnAroundTimes)/len(turnAroundTimes)
    avgResponse = sum(responseTime)/len(responseTime)
    print(responseTime)

    return quantum, contextSwitchTime, totalRuntime, avgTurnAround, avgWait, avgResponse, idleTime, totalSwitches


def round_robin_output(quantum, contextSwitchTime, totalRuntime, avgTurnAround, avgWait, avgResponse, idleTime, totalSwitches):
    print(f"Round Robin Scheduler\nQuantum: {quantum}\nContext Switch Time: {contextSwitchTime}\n")    
    print(f"Total runtime: {totalRuntime:.2f}\nAverage Turnaround Time: {avgTurnAround:.2f}\nAverage Wait Time: {avgWait:.2f}\nAverage Response Time: {avgResponse:.2f}\nTotal Context Switches: {totalSwitches}\nTime spent idle: {idleTime:.2f}")

def FCFS_output(quantum, contextSwitchTime, totalRuntime, avgTurnAround, avgWait, avgResponse, idleTime, totalSwitches):
    print(f"First Come First Serve Scheduler:\nContext Switch Time: {contextSwitchTime}\n")    
    print(f"Total runtime: {totalRuntime:.2f}\nAverage Turnaround Time: {avgTurnAround:.2f}\nAverage Wait Time: {avgWait:.2f}\nAverage Response Time: {avgResponse:.2f}\nTotal Context Switches: {totalSwitches}\nTime spent idle: {idleTime:.2f}")
                

def FCFS(tasks, contextSwitchTime):
    return round_robin(tasks, 10**100, contextSwitchTime)

print_task_info(task1)
print()
round_robin_output(*round_robin(task1, 1, 1))
print()
FCFS_output(*FCFS(task1, 2))