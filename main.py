import glob
import numpy as np
import statistics


class Contr():
    def __init__(self, name, skills, levels, occupied=False, days_occupied=0):
        self.name = name
        self.skills = skills
        self.levels = levels

        self.occupied = occupied
        self.days_occupied = days_occupied

    def toggle_work(self):
        self.occupied = not self.occupied


class Proj():
    def __init__(self, name, days: int, score: int, best_before: int, num_roles: int, req_skills, req_levels,
                 skill_av=[], levels_av=[]):
        self.name = name
        self.days = days
        self.score = score
        self.best_before = best_before
        self.num_roles = num_roles
        self.req_skills = req_skills
        self.req_levels = req_levels
        self.skill_av = skill_av
        self.levels_av = levels_av

    def ratio(self):
        return self.score / self.days * self.num_roles

    def level_mean(self):
        return statistics.mean(self.req_levels)


def process(file):
    with open(file, "r") as fl:
        data = fl.readlines()
        pass
    NAME = file.split(".")[0]

    contr, proj = int(data[0].replace("\n", "").split(" ")[0]), int(data[0].replace("\n", "").split(" ")[1])
    queue = data[1:]

    contr_list = []
    for i in range(contr):
        dat = queue[0].replace("\n", "").split(" ")
        name, amt = dat[0], int(dat[1])
        queue.pop(0)

        skills, levels = [], []
        for i in range(amt):
            dat = queue[0].replace("\n", "").split(" ")
            skills.append(dat[0])
            levels.append(int(dat[1]))
            queue.pop(0)
        contr_list.append(Contr(name, skills, levels))

    proj_list = []
    for i in range(proj):
        dat = queue[0].replace("\n", "").split(" ")
        name = dat[0]
        days = int(dat[1])
        score = int(dat[2])
        best_before = int(dat[3])
        num_roles = int(dat[4])
        queue.pop(0)
        req_skills, req_levels = [], []
        for i in range(num_roles):
            dat = queue[0].replace("\n", "").split(" ")
            req_skills.append(dat[0])
            req_levels.append(int(dat[1]))
            queue.pop(0)
        proj_list.append(Proj(name, days, score, best_before, num_roles, req_skills, req_levels))

    proj_list.sort(key=lambda x: x.level_mean(), reverse=True)

    sub = ""
    counter = 0
    for proj in proj_list:
        print(f"working on: {proj.name}")
        req_skills = proj.req_skills
        req_levels = proj.req_levels

        workers = []
        for iter in range(len(req_skills)):
            available_contr = filter(lambda x: not x.occupied, contr_list)
            for contributer in available_contr:
                contr_skills = contributer.skills
                contr_levels = contributer.levels
                if intersection := set(contr_skills).intersection(set(req_skills)):
                    for elem in intersection:
                        indx_req = req_skills.index(elem)
                        indx = contr_skills.index(elem)

                        if contr_levels[indx] >= req_levels[indx_req]:
                            proj.skill_av.append(contr_skills)
                            proj.levels_av.append(contr_levels)
                            contributer.toggle_work()
                            if contr_levels[indx] == req_levels[indx_req]:
                                contributer.levels[indx] += 1
                        elif elem in proj.levels_av and contr_levels[indx] <= req_levels[indx_req] <= proj.levels_av[
                            proj.levels_av.index(elem)]:
                            proj.skill_av.append(contr_skills)
                            proj.levels_av.append(contr_levels)
                            contributer.toggle_work()
                            contributer.levels[indx] += 1

                            # contributer.days_occupied = proj.days-1
                if contributer.occupied:
                    workers.append(contributer)
        workers = list(set(workers))
        if len(workers) > 0:
            sub += f"\n{proj.name}\n"
            counter += 1
        for worker in workers:
            sub += f"{worker.name} "
        unavailable_contr = filter(lambda x: x.occupied, contr_list)
        for contr in unavailable_contr:
            contr.toggle_work()

    sub = f"{counter}" + sub
    with open(f"{NAME}.out.txt", "w") as file:
        file.write(f'{sub}')
    pass


#file = "a_an_example.in.txt"
#process(file)

myFiles = glob.glob('*.in.txt')
for file in myFiles:
    process(file)
