import pickle
from threading import Thread as thr

def counter():
    global count, running
    while running:
        prog = round(count/48762)
        print('Progress: [%s] %d/1458000' % ('#'*prog, count), end='\r')


def Main():
    global count
    with open('dump.txt', 'rb') as fl:
        data = pickle.load(fl)
    with open('dump.txt', 'rb') as fl:
        data2 = pickle.load(fl)
    del data2['len']
    for est in data2:
        for tp in data2[est]:
            for prova in data2[est][tp]:
                for q in data2[est][tp][prova]:
                    for nota in data2[est][tp][prova][q]:
                        for opt in data2[est][tp][prova][q][nota]:
                            try:
                                if not opt in data[est][tp][prova][q]:
                                    data[est][tp][prova][q][opt] = {}
                            except KeyError:
                                print(est, tp, prova, q, opt)
                            data[est][tp][prova][q][opt][nota] = data[est][tp][prova][q][nota].pop(opt)
                            count += 1
                                
                    if len(data[est][tp][prova][q][nota])==0:
                        del data[est][tp][prova][q][nota]
                    else:
                        print('Problem!')
                        exit()

    with open('ndump.txt', 'wb') as fl:
        pickle.dump(data, fl)

if __name__=='__main__':
    global running, count
    count = 0
    running = True
    thr(target=counter).start()
    Main()
    running = False
