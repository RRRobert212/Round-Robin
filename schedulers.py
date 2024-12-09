
import statistics

task2 = [[4,0],[20,2],[12,9],[11,0],[64,10000],[64,20],[60,20],[39,5]]

def print_task_info(tasks, file):
    burst_times = [task[0] for task in tasks]
    numberOfJobs = len(burst_times)
    totalBurstTime = sum(burst_times)
    averageBurstTime = sum(burst_times)/len(burst_times)
    standardDeviation = statistics.stdev(burst_times)
    minBurst = min(burst_times)
    maxBurst = max(burst_times)

    file.write(f"""Number of jobs: {numberOfJobs}\nTotal Burst Time: {totalBurstTime}\nMin Burst Time: {minBurst}\nMax Burst Time: {maxBurst}\nAverage Burst Time: {averageBurstTime:.2f}\nStandard Deviation: {standardDeviation:.2f}\n""")
    return



#core of project
def round_robin(tasks, quantum, contextSwitchTime):

    sorted_tasks = sorted(tasks, key = lambda x: x[1])

    burst_times = [task[0] for task in sorted_tasks]
    arrival_times = [task[1] for task in sorted_tasks]

    totalRuntime = 0
    totalSwitches = 0
    initial_burst = burst_times[:]
    turnAroundTimes = [0] * len(tasks)
    waitTimes = [0] * len(tasks)
    responseTime = [0] *len(tasks)
    #time tracks time elapsed, different from runtime because if no tasks are in the ready queue, we don't increment runtime, but we do increment time
    time = 0
    k = [0] * len(tasks)    #k is used to track if it's the first time a task has had CPU access, to calculate response time
    
    while any( task > 0 for task in burst_times):
        count = 0
        for i in range(len(burst_times)):
            if (time >= arrival_times[i] and burst_times[i] > 0):

                #in the edge case where only 1 task remains, I have to not add context switch between quantums
                non_zero_count = sum(1 for x in burst_times if x != 0)
                if non_zero_count == 1:
                     #task has more than one quantum left
                    if burst_times[i] - quantum > 0:             
                        burst_times[i] -= quantum
                        totalRuntime += quantum
                        time += quantum
                        
                    #task gets to 0 in this quantum
                    else:
                        totalRuntime += burst_times[i]
                        time += burst_times[i]
                        burst_times[i] = 0
                        turnAroundTimes[i] = time - arrival_times[i]
                else:
                    #if it's a tasks's first time on CPU, calculate response time
                    if k[i] == 0:
                        responseTime[i] = time - arrival_times[i]
                        k[i] = 1

                    #task has more than one quantum left
                    if burst_times[i] - quantum > 0:             
                        burst_times[i] -= quantum
                        totalRuntime += quantum
                        totalRuntime += contextSwitchTime
                        time += quantum
                        time += contextSwitchTime
                        totalSwitches += 1
                        
                    #task gets to 0 in this quantum
                    else:
                        totalRuntime += burst_times[i]
                        time += burst_times[i]
                        burst_times[i] = 0
                        turnAroundTimes[i] = time - arrival_times[i]
                        totalRuntime += contextSwitchTime
                        time += contextSwitchTime
                        totalSwitches += 1

            #if none of the tasks are ready to execute, add 1 to time and repeat
            
            else: count += 1
            if count == len(tasks):
                time += 1

    for i in range(len(tasks)):
        waitTimes[i] = turnAroundTimes[i] - initial_burst[i]

    #fixes an issue with final response time not getting calculated for FCFS
    for i in range(len(tasks)):
        if responseTime[i] == 0:
            responseTime[i] = waitTimes[i]
    



    avgWait = sum(waitTimes)/len(waitTimes)
    avgTurnAround = sum(turnAroundTimes)/len(turnAroundTimes)
    avgResponse = sum(responseTime)/len(responseTime)

    return quantum, contextSwitchTime, totalRuntime, avgTurnAround, avgWait, avgResponse, totalSwitches

#FCFS is just round robin with a long quantum
def FCFS(tasks, contextSwitchTime):
    return round_robin(tasks, 10**100, contextSwitchTime)


def SJF_NonPremptive(tasks, contextSwitchTime):
    # Sort tasks by arrival time
    sorted_tasks = sorted(tasks, key=lambda x: x[1])

    initial_bursts = [task[0] for task in sorted_tasks]
    burst_times = [task[0] for task in sorted_tasks]  
    arrival_times = [task[1] for task in sorted_tasks] 
    turnAroundTimes = [0] * len(tasks) 
    waitTimes = [0] * len(tasks)       
    responseTimes = [0] * len(tasks)   
    totalRuntime = 0
    totalSwitches = 0
    time = 0
    ready_queue = []
    completed = []

    #need to prevent context switch on first task (RR does this effectively by not counting final context switch)
    first_task = True


    while (len(completed) < len(tasks)):
        for i in range(len(burst_times)):
            if (arrival_times[i] <= time and burst_times[i] > 0 and i not in ready_queue):
                ready_queue.append(i)

        ready_queue.sort(key = lambda k: burst_times[k])
        if len(ready_queue) > 0:
            index = ready_queue.pop(0)

            if not first_task:
                totalSwitches += 1
                time += contextSwitchTime
                totalRuntime += contextSwitchTime
            else: first_task = False

            if responseTimes[index] == 0:
                responseTimes[index] = time - arrival_times[index]

            totalRuntime += burst_times[index]
            time += burst_times[index]
            burst_times[index] = 0

            turnAroundTimes[index] = time - arrival_times[index]
            waitTimes[index] = turnAroundTimes[index] - initial_bursts[index]
            completed.append(True)


        time += 1


    avgTurnAround = sum(turnAroundTimes) / len(turnAroundTimes)
    avgWait = sum(waitTimes) / len(waitTimes)
    avgResponse = sum(responseTimes) / len(responseTimes)


    return contextSwitchTime, totalRuntime, avgTurnAround, avgWait, avgResponse, totalSwitches




#output functions, change to write to file?
def round_robin_output(quantum, contextSwitchTime, totalRuntime, avgTurnAround, avgWait, avgResponse, totalSwitches, file):
    file.write(f"Round Robin Scheduler:\nQuantum: {quantum}\nContext Switch Time: {contextSwitchTime}\n")    
    file.write(f"Total runtime: {totalRuntime:.2f}\nAverage Turnaround Time: {avgTurnAround:.2f}\nAverage Wait Time: {avgWait:.2f}\nAverage Response Time: {avgResponse:.2f}\nTotal Context Switches: {totalSwitches}\n")

def FCFS_output(quantum, contextSwitchTime, totalRuntime, avgTurnAround, avgWait, avgResponse, totalSwitches, file):
    file.write(f"First Come First Serve Scheduler:\nContext Switch Time: {contextSwitchTime}\n")    
    file.write(f"Total runtime: {totalRuntime:.2f}\nAverage Turnaround Time: {avgTurnAround:.2f}\nAverage Wait Time: {avgWait:.2f}\nAverage Response Time: {avgResponse:.2f}\nTotal Context Switches: {totalSwitches}\n")

def SJF_output(contextSwitchTime, totalRuntime, avgTurnAround, avgWait, avgResponse, totalSwitches, file):
    file.write(f"Shortest Job First Scheduler:\nContext Switch Time: {contextSwitchTime}\n")    
    file.write(f"Total runtime: {totalRuntime:.2f}\nAverage Turnaround Time: {avgTurnAround:.2f}\nAverage Wait Time: {avgWait:.2f}\nAverage Response Time: {avgResponse:.2f}\nTotal Context Switches: {totalSwitches}\n")
