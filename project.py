import glob
import numpy as np
import time

class Contr():
    def __init__(self,name, skills, occupied=False, days_occupied=0):
        self.name = name
        self.skills = skills

        self.occupied = occupied
        self.days_occupied = days_occupied

    def toggle_work(self):
        self.occupied = not self.occupied

    def count_down(self):
        self.days_occupied = self.days_occupied - 1 if self.days_occupied > 0 else self.days_occupied


class Proj():
    def __init__(self, name, days:int, score:int, best_before:int, num_roles:int, req_skills):
        self.name = name
        self.days = days
        self.score = score
        self.best_before = best_before
        self.max = self.score + self.best_before
        self.num_roles = num_roles
        self.req_skills = req_skills

        self.completed_skills = [0] * len(self.req_skills)

    def ratio(self):
        return self.score/self.days*self.num_roles


def get_dat(queue):
    return queue[0].replace("\n","").split(" ")


def process(file):
    t0 = time.time()
    with open(file,"r") as fl:
        data = fl.readlines()
        pass
    NAME = file.split(".")[0]

    contr, proj = int(data[0].replace("\n","").split(" ")[0]), int(data[0].replace("\n","").split(" ")[1])
    queue = data[1:]

    contr_list = []
    for i in range(contr):
        dat = get_dat(queue)
        name, amt = dat[0], int(dat[1])
        queue.pop(0)

        skills = []
        for j in range(amt):
            dat = get_dat(queue)
            skill, level = dat[0], int(dat[1])
            skills.append((skill,level))
            queue.pop(0)
        contr_list.append(Contr(name,skills))


    proj_list = []
    for i in range(proj):
        dat =  get_dat(queue)
        name = dat[0]
        days = int(dat[1])
        score = int(dat[2])
        best_before = int(dat[3])
        num_roles = int(dat[4])
        queue.pop(0)
        req_skills = []
        for j in range(num_roles):
            dat = get_dat(queue)
            req_skills.append((dat[0],int(dat[1])))
            queue.pop(0)
        proj_list.append(Proj(name,days,score,best_before,num_roles,req_skills))

    proj_list.sort(key= lambda x: x.ratio(), reverse=True)

    complete_projects = []
    #current_day = 0
    for workday in range(50):
        #print(f"$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ DAY: {current_day}")
        for i, proj in enumerate(proj_list):
            proj_members = []
            proj.completed_skills = [0] * len(proj.req_skills)
            for j, req_skill in enumerate(proj.req_skills):
                for contributor in contr_list:
                    for skill in contributor.skills:
                        if skill[0] == req_skill[0] and skill[1] >= req_skill[1]:
                            if proj.completed_skills[j] == 0 and contributor.days_occupied == 0:
                                contributor.days_occupied += proj.days
                                proj.completed_skills[j] = 1
                                proj_members.append(contributor)
            if 0 not in proj.completed_skills:
                complete_projects.append((proj.name, proj_members))
                proj_list.pop(i)
            else:
                for member in proj_members:
                    member.days_occupied = 0
        #current_day += 1

        for contributor in contr_list:
            contributor.count_down()
    print(complete_projects)
    print(f"time used: {time.time()-t0}")

    with open(f"{NAME}.out.txt", "w") as file:
        file.write(f"{len(complete_projects)}")
        for proj in complete_projects:
            file.write(f"\n{proj[0]}\n")
            for contr in proj[1]:
                file.write(f"{contr.name} ")
        pass



#file = "b_better_start_small.in.txt"
#process(file)

""" """
myFiles = glob.glob('*.in.txt')
for file in myFiles:
    process(file)

