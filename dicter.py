def organizer(provas, year, cod, seq):
    ret = {}
    for (prova, cont) in provas.items():
        prova, ID = prova.split('-')


def ranker(raw, lenght, year):
    import PLANILHAS.xlsImport as xls
    plans = {}
    habs = {}
    adds = {'CH':0, 'CN':45, 'LC':85, 'MT':135}
    rawPl = xls.Main('PLANILHAS/ITENS_ENEM_%s.xlsx' % str(year))
    for (mat, quest) in rawPl.items():
        plans[mat[:2]] = {}
        for q in quest:
            print(q)
            for (val, rv) in q.items():
                if 'Ordem' in val:
                    if not val[6:].upper() in plans[mat[:2]]:
                        plans[mat[:2]][val[6:].upper()] = {}
                    if 'i' in str(rv) or 'e' in str(rv):
                        rv = str(int(rv[:-1])-adds[mat[:2]])+rv[-1]
                    else:
                        rv = str(int(rv)-adds[mat[:2]])
                    plans[mat[:2]][val[6:].upper()][rv] = q['SEQ']
                elif val == 'SEQ':
                    if mat[:2]!='LC':
                        habs[str(int(rv)+adds[mat[:2]])] = {x:y for (x,y) in q.items() if 'HAB' in x}
    #plans = {x[:2]:plans[x] for x in plans}
        
    from re import findall
    imp = {x[0]:{x[a]:x[a+1]for a in range(1,11, 2)} for x in findall('/ID_PROVA_(.{2}).+\n'+'\t(\d{3})\t"(.+?)".+\n'*5, ''.join([chr(x) for x in open('INPUTS/INPUT_ SPSS_MICRODADOS_ENEM_%s.sps' % str(0), 'rb').read()]))}
    input(imp)
    input(plans)
    if lenght == 0:
        return organizer(raw)
    if lenght == 1:
        res = {}
        for a in raw:
            res[a] = organizer(raw[a], year, imp, seq)
        return res
    if lenght == 2:
        res = {}
        for a in raw:
            res[a] = {}
            for b in raw[a]:
                res[a][b] = organizer(raw[a][b], year, imp, seq)
        return res
    if lenght == 3:
        res = {}
        for a in raw:
            res[a] = {}
            for b in raw[a]:
                res[a][b] = {}
                for c in raw[a][b]:
                    res[a][b][c] = organizer(raw[a][b][c], year, imp, seq)
        return res

def Main(year):
    from pickle import load, dump
    with open('dump.txt', 'rb') as fl:
        data = load(fl)
    l = data.pop('len')
    ndata = ranker(data, l, year)
    ndata['len'] = l
    
    with open('ndump.txt', 'wb') as fl:
        dump(ndata, fl)

if __name__=='__main__':
    Main(input())
