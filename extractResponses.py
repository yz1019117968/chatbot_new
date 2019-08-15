

def getSampleQA(validateset):
    q = []
    r = []
    for dialogue in validateset:
        q.append(dialogue[0])
        r.append([dialogue[1]])
    return q,r
if __name__ == '__main__':
    getSampleQA()