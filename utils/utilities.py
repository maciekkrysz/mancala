def is_int(a):
    try:     
        i = int(a)
    except:  
        return False
    return True

def other_player(current_player):
    return (current_player - 1) * -1