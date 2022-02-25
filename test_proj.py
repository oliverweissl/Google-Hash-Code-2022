import glob
import numpy as np
import time

class Contr():
    def __init__(self,name, skills, levels, occupied=False, days_occupied=0):
        self.name = name
        self.skills = skills
        self.levels = levels
        self.skill_level = []
        for index, item in enumerate(self.levels):
            self.skill_level.append((self.skills[index], self.levels[index]))

        self.occupied = occupied
        self.days_occupied = days_occupied
    def toggle_work(self):
        self.occupied = not self.occupied


class Proj():
    def __init__(self, name, days:int, score:int, best_before:int, num_roles:int, req_skills, req_levels):
        self.name = name
        self.days = days
        self.score = score
        self.best_before = best_before
        self.max = self.score + self.best_before
        self.num_roles = num_roles
        self.req_skills = req_skills
        self.req_levels = req_levels
        self.completed_skills = [0] * len(self.req_skills)

    def ratio(self):
        return self.score/self.days*self.num_roles

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
        dat = queue[0].replace("\n","").split(" ")
        name, amt = dat[0], int(dat[1])
        queue.pop(0)

        skills = []
        levels = []
        for i in range(amt):
            dat = queue[0].replace("\n","").split(" ")
            skill, level = dat[0], int(dat[1])
            skills.append(skill)
            levels.append(level)
            queue.pop(0)
        contr_list.append(Contr(name,skills,levels))

    proj_list = []
    for i in range(proj):
        dat =  queue[0].replace("\n","").split(" ")
        name = dat[0]
        days = int(dat[1])
        score = int(dat[2])
        best_before = int(dat[3])
        num_roles = int(dat[4])
        queue.pop(0)
        req_skills, req_levels = [],[]
        for i in range(num_roles):
            dat = queue[0].replace("\n","").split(" ")
            req_skills.append(dat[0])
            req_levels.append(int(dat[1]))
            queue.pop(0)
        proj_list.append(Proj(name,days,score,best_before,num_roles,req_skills,req_levels))

    proj_list.sort(key= lambda x: x.ratio(), reverse=True)


    current_day = 0
    proj_name = ""
    proj_members = []
    proj_member_obj = []

    complete_projects = []

    for workday in range(50):
        #print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ DAY: " + str(current_day))
        for proj_index, proj in enumerate(proj_list):
            proj_name = proj.name
            proj_members = []
            proj_member_obj = []
            req_skills = proj.req_skills
            req_levels = proj.req_levels
            proj.completed_skills = [0] * len(proj.req_skills)
            for index, skill in enumerate(req_skills):
                for contributor in contr_list:
                    for cindex, contr_skill in enumerate(contributor.skill_level):
                        if contr_skill[0] == skill and contr_skill[1] >= req_levels[index]:
                            if proj.completed_skills[index] == 0 and contributor.days_occupied == 0:
                                contributor.days_occupied += proj.days
                                proj.completed_skills[index] = 1
                                proj_members.append(contributor.name)
                                proj_member_obj.append(contributor)
            if 0 not in proj.completed_skills:
                complete_projects.append((proj_name, proj_members))
                proj_list.pop(proj_index)
            else:
                for member in proj_member_obj:
                    member.days_occupied -= proj.days


        current_day += 1
        for contributor in contr_list:
            if contributor.days_occupied > 0:
                contributor.days_occupied -= 1
    print(complete_projects)
    print(f"time used: {time.time()-t0}")


    with open("b_better_start_small.outtttt.txt", "w") as file:
        project_count = len(complete_projects)
        file.write(str(project_count))
        file.write("\n")
        for items in complete_projects:
            for project in items:
                if isinstance(project, list):
                    for name in project:
                        file.write(str(name))
                        file.write(" ")
                else:
                    file.write(str(project))
                file.write("\n")
        pass


file = "b_better_start_small.in.txt"
process(file)

"""
myFiles = glob.glob('*.in.txt')
for file in myFiles:
    process(file)
"""
