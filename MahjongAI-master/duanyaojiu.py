from collections.abc import Iterable
from functools import cmp_to_key

def getValue(tiles):
    """
    >>> tiles = (1,1,0,0,2,0,0,0,0) # 1w,2w,5w,5w
    >>> getValue(tiles)
    ...
    """
    assert len(tiles) == 9
    assert isinstance(tiles, Iterable)
    assert sum(tiles) <= 14

    # consider jiang (including tuples)
    results_1 = set()
    for i in range(9):
        if tiles[i] >= 2:
            newtiles = tuple(tiles[j] if j!=i else tiles[j]-2 for j in range(9))
            results_1.update(eliminateTriple(newtiles))

    # not consider jiang (only triples)
    results_2 = eliminateTriple(tiles)

    return results_1, results_2
            

def eliminateTriple(tiles):
    if len(tiles) == 0:
        return []

    results = set([tiles])

    # 3 same tiles check    
    for i in range(9):
        if tiles[i] >= 3:
            newtiles = tuple(tiles[j] if j!=i else tiles[j]-3 for j in range(9))
            results.update(eliminateTriple(newtiles))
    
    # 3 consecutive tiles
    for i in range(9-3):
        if tiles[i] and tiles[i+1] and tiles[i+2]:
            newtiles = tuple(tiles[j]-1 if j in (i, i+1, i+2) else tiles[j] for j in range(9))
            results.update(eliminateTriple(newtiles))

    # 2 same tiles and pick another
    for i in range(9):
        if tiles[i] == 2:
            newtiles = tuple(tiles[j] if j!=i else tiles[j]-2 for j in range(9))
            cur_res = eliminateTriple(newtiles)
            for res in cur_res:
                results.add(
                    tuple(res[j] if j!= i else res[j]-1 for j in range(9))
                )
    
    # 2 consecutive tiles and pick one
    for i in range(0,1):
        if tiles[i] and tiles[i+1]:
            newtiles = tuple(tiles[j]-1 if j in (i, i+1) else tiles[j] for j in range(9))
            cur_res = eliminateTriple(newtiles)
            for res in cur_res:
                results.add(
                    tuple(res[j] if j!= i+2 else res[j]-1 for j in range(9))
                )
    for i in range(1,9-2):
        if tiles[i] and tiles[i+1]:
            newtiles = tuple(tiles[j]-1 if j in (i, i+1) else tiles[j] for j in range(9))
            cur_res = eliminateTriple(newtiles)
            for res in cur_res:
                results.add(
                    tuple(res[j] if j!= i+2 else res[j]-1 for j in range(9))
                )
            for res in cur_res:
                results.add(
                    tuple(res[j] if j!= i-1 else res[j]-1 for j in range(9))
                )
    for i in range(7,7+1):
        if tiles[i] and tiles[i+1]:
            newtiles = tuple(tiles[j]-1 if j in (i, i+1) else tiles[j] for j in range(9))
            cur_res = eliminateTriple(newtiles)
            for res in cur_res:
                results.add(
                    tuple(res[j] if j!= i-1 else res[j]-1 for j in range(9))
                )

    # eliminate this:
    if len(results) > 5:
        results.remove(tiles)

    return results

def need_to_change(man_tiles, pin_tiles, suo_tiles):
    man_tiles, pin_tiles, suo_tiles = tuple(man_tiles), tuple(pin_tiles), tuple(suo_tiles)
    results = set()

    res_man2, res_man3 = getValue(man_tiles)
    res_pin2, res_pin3 = getValue(pin_tiles)
    res_suo2, res_suo3 = getValue(suo_tiles)

    for i in res_man2:
        for j in res_pin3:
            for k in res_suo3:
                if sum(i) + sum(j) + sum(k) == 0:
                    results.add((i,j,k))
    
    for i in res_man3:
        for j in res_pin2:
            for k in res_suo3:
                if sum(i) + sum(j) + sum(k) == 0:
                    results.add((i,j,k))

    for i in res_man3:
        for j in res_pin3:
            for k in res_suo2:
                if sum(i) + sum(j) + sum(k) == 0:
                    results.add((i,j,k))
    
    for i in res_man3:
        for j in res_pin3:
            for k in res_suo3:
                if sum(i) + sum(j) + sum(k) == 0:
                    results.add((i,j,k))
    
    # check num needed
    min_needed = 999
    for i,j,k in results:
        min_needed = min(min_needed, num_needed_to_change(i,j,k))
    
    return sorted(results,key=cmp_to_key(lambda a, b: num_needed_to_change(a) - num_needed_to_change(b))), min_needed

def num_needed_to_change(res_man, res_pin = None, res_suo = None):
    if res_pin == None and res_suo == None:
        res_man, res_pin, res_suo = res_man
    
    num_needed = 0
    for num in res_man:
        num_needed += abs(num)
    for num in res_pin:
        num_needed += abs(num)
    for num in res_suo:
        num_needed += abs(num)
    return num_needed

def duanYaoJiu(tiles136):
    for i in tiles136:
        assert not i//4 in (0, 8, 9, 17, 18, 26) and i//4 < 27
    
    tiles = [0] * 27
    for i in tiles136:
        tiles[i//4] += 1
    return need_to_change(tiles[:9], tiles[9:18], tiles[18:])

def test1():
    tiles = (1,1,0,0,2,0,0,0,0) # 1w,2w,5w,5w
    tiles = (1,1,1,1,1,0,0,0,0)
    print(getValue(tiles))

def test2():
    """
    result:
    ((0, 0, -1, 0, 0, 0, 0, 0, 0), (0, 0, 1, 0, 0, 1, 0, 0, 0), (0, 0, 0, 0, 0, -1, 0, 0, 0))
    ((0, 0, 0, 0, 0, -1, 0, 0, 0), (0, 0, 1, 0, 0, 1, 0, 0, 0), (0, 0, 0, 0, 0, -1, 0, 0, 0))
    ((0, 0, 0, 0, 0, -1, 0, 0, 0), (0, 0, 1, 0, 0, 1, 0, 0, 0), (0, 0, 0, 0, 0, 0, 0, -1, 0))
    ((0, 0, -1, 0, 0, 0, 0, 0, 0), (0, 0, 1, 0, 0, 1, 0, 0, 0), (0, 0, 0, 0, 0, 0, 0, -1, 0))
    ((0, 0, 0, 0, 1, -1, 0, -1, 0), (0, 0, 1, 0, 0, 1, 0, 0, 0), (0, 0, 0, 0, 0, -1, 0, 0, 0))
    ((0, 0, 0, 1, -1, 0, 0, -1, 0), (0, 0, 1, 0, 0, 1, 0, 0, 0), (0, 0, 0, 0, 0, 0, 0, -1, 0))
    ((0, 0, -1, 0, 0, 0, 0, 0, 0), (0, 0, 1, 0, 0, 1, 0, 0, 1), (0, 0, 0, 0, 0, -1, 0, -1, 0))
    ((0, 0, -1, -1, 0, 0, 1, 0, 0), (0, 0, 1, 0, 0, 1, 0, 0, 0), (0, 0, 0, 0, 0, 0, 0, -1, 0))
    ((0, 0, 0, 0, 0, -1, 0, 0, 0), (0, 0, 1, 0, 0, 1, 0, 0, 1), (0, 0, 0, 0, 0, -1, 0, -1, 0))
    ((0, 0, -1, -1, 0, 0, 1, 0, 0), (0, 0, 1, 0, 0, 1, 0, 0, 0), (0, 0, 0, 0, 0, -1, 0, 0, 0))
    4
    """
    man_tiles = (0,0,0,1,2,1,1,0,0)
    pin_tiles = (0,0,1,0,0,1,0,0,3)
    suo_tiles = (0,0,0,0,0,2,0,2,0)

    res, num = need_to_change(man_tiles, pin_tiles, suo_tiles)
    for i in res[:10]:
        print(i)
    print(num)

if __name__ == "__main__":
    test2()