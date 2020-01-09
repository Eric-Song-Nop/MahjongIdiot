def ten_to_five(tiles):
#(1,2,3,4,5,6,7,8,9)
    temp = ''
    for k in tiles:
        temp += str(k)
        
    return int(temp, base=5)

def five_to_ten(five):
    ans = [0,0,0,0,0,0,0,0,0]
    count = 8
    while(five >= 1):

        ans[count] = five%5
        count -= 1
        five = five//5
    
    return tuple(ans)
