Round Robin, Shortest Job First, and First Come First Serve Scheduler Simulator

Given a list containing tuples of burst times and arrival times, this program will simulate Round Robin, SJF, and FCFS schedulers.

To execute the program with the given example in main, just run main.py. Or, adjust the task list. and function parameters as desired.

Note that to get output from the functions, you have to run the output functions with the scheduler functions as an unpacked parameter.
E.G.: round_robin_output(*round_robin(taskList, 5, 1), file) where taskList is your array of tasks (burst times and arrival times), 5 is your quantum, and 1 is your context switch time. (leave file as 'file' if you want to output to scheduler_output.txt). Adjust the quantum and context switch time as needed.

An example of 4 task lists are given in the main function, but new task lists can be created by the user and tested. Just enter an array of tuples where array[i[0]] is burst time of task i and array[i[1]] is the arrival time of task i. Then either replace the tasks in tasks_list with this array or add it as an additional list. The schedulers will loop through every task list in the tasks_list array and provide output for all of them.

Adjusting these values gives insight into the advantages and disadvantages of each scheduler. For example, a high context switch time and a high quantum makes Round Robin very inefficient. However, a low quantum gives it a very low response time compared to other algorithms, which is a positive.

Different task lists also cause varying performance in schedulers. For example, tasklists with high burst times cause a high total runtime in Round Robin, because lots of context switches occur.

Note that if there are n tasks in a list, n-1 context switches will occur for FCFS and SJF. This means their total runtime is always equal. However, because SJF prioritizes shorter tasks, it has a smaller turnaround time.

There are potential improvements for this program. For example, the time it takes to sort the task list is not considered for SJF. This may add to total runtime. Furthermore, this version of SJF is non-preemptive, meaning once a task begins running, it will run to completion even if a shorter task is ready. Preemptive versions of SJF, also called shortest remaining time algorithms, also exist and would be interesting to investigate.