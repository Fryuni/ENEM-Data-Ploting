def setTgts(values, year, end=False):
    if input('Usar última configuração? [Y/n]--> ').lower() != 'n':
        from pickle import load
        with open('.previous.conf', 'rb') as fl:
            tgts = load(fl)
        print(tgts)
    else:
        line = ''
        names = {}
        tgts = []
        with open('INPUTS/INPUT_ SPSS_MICRODADOS_ENEM_'+str(year)+'.sps', 'rb') as fl:
            while line!=b'VARIABLE LABELS\r\n':
                line = fl.readline()
            for line in fl:
                line = ''.join([chr(x) for x in line])
                s = line.split('\t') if '\t' in line else line.split(' ')
                s = [s[0], ' '.join(s[1:])]
                if s[0]=='.\r\n':
                    break
                names[s[0]]=s[1].strip('"\n\r')
        print("Gostaria de classificar por essa divisão?\n")
        for val in values:
            try:
                if input('\033[F'+(' '*100)+'\r'+names[val]+' [y/N]--> ').lower() == 'y':
                    tgts.append(val)
            except KeyError:
                pass
        with open('.previous.conf', 'wb') as fl:
            from pickle import dump
            dump(tgts, fl, 3)
    if end:
        print(', '.join(tgts))
    return tgts

def ranking(options, rank, save):
    if len(rank)>0:
        if not rank[0] in save:
            save[rank[0]] = {}
    elif len(rank) == 0:
        for av in options:
            sep = av.split(',')
            prova = sep[0]
            nota = 100*round(float(sep[1])/100)
            ID = sep[2]
            if not '-'.join((prova,ID)) in save:
                save['-'.join((prova,ID))] = {q:{opt:{nota:0 for nota in range(100,1001,100)} for opt in 'ABCDE.*'} for q in range(1, 46)}
            for q in range(1,46):
                save['-'.join((prova,ID))][q][options[av][q-1]][nota] += 1
        return
    if len(rank)>1:
        if not rank[1] in save[rank[0]]:
            save[rank[0]][rank[1]] = {}
    elif len(rank) == 1:
        for av in options:
            sep = av.split(',')
            prova = sep[0]
            nota = 100*round(float(sep[1])/100)
            ID = sep[2]
            if not '-'.join((prova,ID)) in save[rank[0]]:
                save[rank[0]]['-'.join((prova,ID))] = {q:{opt:{nota:0 for nota in range(100,1001,100)} for opt in 'ABCDE.*'} for q in range(1, 46)}
            for q in range(1,46):
                save[rank[0]]['-'.join((prova,ID))][q][options[av][q-1]][nota] += 1
        return
    if len(rank)>2:
        if not rank[2] in save[rank[0]][rank[1]]:
            save[rank[0]][rank[1]][rank[2]] = {}
        for av in options:
            sep = av.split(',')
            prova = sep[0]
            nota = 100*round(float(sep[1])/100)
            ID = sep[2]
            if not '-'.join((prova,ID)) in save[rank[0]][rank[1]][rank[2]]:
                save[rank[0]][rank[1]][rank[2]]['-'.join((prova,ID))] = {q:{opt:{nota:0 for nota in range(100,1001,100)} for opt in 'ABCDE.*'} for q in range(1, 46)}
            for q in range(1,46):
                save[rank[0]][rank[1]][rank[2]]['-'.join((prova,ID))][q][options[av][q-1]][nota] += 1
        return
    elif len(rank) == 2:
        for av in options:
            sep = av.split(',')
            prova = sep[0]
            nota = 100*round(float(sep[1])/100)
            ID = sep[2]
            if not '-'.join((prova,ID)) in save[rank[0]][rank[1]]:
                save[rank[0]][rank[1]]['-'.join((prova,ID))] = {q:{opt:{nota:0 for nota in range(100,1001,100)} for opt in 'ABCDE.*'} for q in range(1, 46)}
            for q in range(1,46):
                save[rank[0]][rank[1]]['-'.join((prova,ID))][q][options[av][q-1]][nota] += 1
        return

def choice(line, tgts, save, sem):
    sem.acquire()
    rank = [line[a] for a in tgts]
    options = {','.join((a[-2:],line['NOTA_'+a[-2:]],line['ID_PROVA_'+a[-2:]])):line[a] for a in line if a[:-2] == 'TX_RESPOSTAS_' and line['IN_PRESENCA_'+a[-2:]] == '1'}
    ranking(options, rank, save)
    sem.release()
