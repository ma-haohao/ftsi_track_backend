from datetime import datetime,timedelta

def test():
    a=[{"test":1},{"test":2}]
    b=[]
    for item in a:
        item["test"]=3
        item["task"]=6
        b.append(item)
    print(a)
    print(b)


def main():
    test()

if __name__ == '__main__':
    main()
