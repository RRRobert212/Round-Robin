from schedulers import *

task1 = [[5,0],[6,0],[7,0],[3,0],[2,1],[2,1],[2,1],[2,3],[10,4]]
task2 = [[4,0],[20,2],[12,9],[11,0],[64,10000],[64,20],[60,20],[39,5]]
task3 = [[100,0],[100,1],[2000,20],[200,1],[300,1000],[3000,1]]
task4 = [[1,0],[9000,0],[1,1],[3,1],[5,1],[20,1],[12,1],[9,1],[10000,0]]

tasks_list = [task1, task2, task3, task4]

def main():
    with open('scheduler_output.txt', 'w') as file:
        for t in tasks_list:
            file.write("Task Info:\n")
            print_task_info(t, file)
            
            file.write("\nRound Robin\n")
            round_robin_output(*round_robin(t,4,1), file)
            
            file.write("\nFCFS\n")
            FCFS_output(*FCFS(t,1), file)
            
            file.write("\nSJF\n")
            SJF_output(*SJF_NonPremptive(t,1), file)
            
            file.write("\n" + "="*40 + "\n")

    print("Output written to 'scheduler_output.txt'")




if __name__ == '__main__': main()