import requests 
import json


def validMove(x, y, m_x, m_y):
    if (x >= m_x) and (y >= m_y) and (m_x >= 0) and (m_y >= 0):
        return 1
    return 0

def mazeTrace(state, trace, x, y):
    #print("maze trace")
    if (state == 'END'):
        return 1
    game_state = requests.get('http://ec2-34-216-8-43.us-west-2.compute.amazonaws.com/game?token=' + token)
    parsed_state = json.loads(game_state.text)
    i = parsed_state['current_location'][1]
    j = parsed_state['current_location'][0]
    #print(i)
    #print(j)
    trace[i][j] = 1
    #print('check up')
    if (validMove(x, y, i-1, j)):
        #print('up is valid')
        if trace[i-1][j] != 1:
            me = requests.post(url = 'http://ec2-34-216-8-43.us-west-2.compute.amazonaws.com/game?token=' + token, data = {'action': 'UP'}) 
            #print('up')
            parsed_action = json.loads(me.text)
            result = parsed_action['result']
            #print(result)
            if (result == "SUCCESS" or result == "END"):
                #print('up success or end')
                if mazeTrace(result, trace, x, y) == 1:
                    return 1
                else:
                    me = requests.post(url = 'http://ec2-34-216-8-43.us-west-2.compute.amazonaws.com/game?token=' + token, data = {'action':'DOWN'})
    #print('check down')
    if (validMove(x, y, i+1, j)):
        #print('down is valid')
        if trace[i+1][j] != 1:
            me = requests.post(url = 'http://ec2-34-216-8-43.us-west-2.compute.amazonaws.com/game?token=' + token, data = {'action':'DOWN'}) 
            #print('down')
            parsed_action = json.loads(me.text)
            result = parsed_action['result']
            #print(result)
            if (result == "SUCCESS" or result == "END"):
                #print('down success or end')
                if mazeTrace(result, trace, x, y) == 1:
                    return 1
                else:
                    me = requests.post(url = 'http://ec2-34-216-8-43.us-west-2.compute.amazonaws.com/game?token=' + token, data = {'action': 'UP'})
    #print('check left')
    if (validMove(x, y, i, j-1)):
        #print('left is valid')
        if trace[i][j-1] != 1:
            me = requests.post(url = 'http://ec2-34-216-8-43.us-west-2.compute.amazonaws.com/game?token=' + token, data = {'action': 'LEFT'}) 
            #print('left')
            parsed_action = json.loads(me.text)
            result = parsed_action['result']
            #print(result)
            if (result == "SUCCESS" or result == "END"):
                #print('left success or end')
                if mazeTrace(result, trace, x, y) == 1:
                    return 1
                else:
                    me = requests.post(url = 'http://ec2-34-216-8-43.us-west-2.compute.amazonaws.com/game?token=' + token, data = {'action': 'RIGHT'}) 
    #print('check right')
    if (validMove(x, y, i, j+1)):
        #print('right is valid')
        if trace[i][j+1] != 1:
            me = requests.post(url = 'http://ec2-34-216-8-43.us-west-2.compute.amazonaws.com/game?token=' + token, data = {'action': 'RIGHT'}) 
            #print('right')
            parsed_action = json.loads(me.text)
            result = parsed_action['result']
            #print(result)
            if (result == "SUCCESS" or result == "END"):
                #print('right success or end')
                if mazeTrace(result, trace, x, y) == 1:
                    return 1
                else:
                    me = requests.post(url = 'http://ec2-34-216-8-43.us-west-2.compute.amazonaws.com/game?token=' + token, data = {'action': 'LEFT'}) 

    
    #print('backtrace')
    return 0

data = {'uid': '404784142'}
m_url = 'http://ec2-34-216-8-43.us-west-2.compute.amazonaws.com/session'
m = requests.post(url = m_url, data = data)
parsed_text = json.loads(m.text)
token = parsed_text['token']
while(1):
    game_state = requests.get('http://ec2-34-216-8-43.us-west-2.compute.amazonaws.com/game?token=' + token)
    parsed_state = json.loads(game_state.text)
    status = parsed_state['status']

    if (status == "NONE"):
        print("Session has expired. Program Exiting...\n")
        exit(0)
    if (status == "GAME_OVER"):
        print("GAME OVER...\n")
        exit(0)
    if (status == "FINISHED"):
        print("FINISHED ALL LEVELS!!\n")
        exit(0)
    maze_size = parsed_state['maze_size']
    trace = [[0 for y in range(maze_size[0])] for x in range(maze_size[1])]
    # call maze function
    if mazeTrace("SUCCESS", trace, maze_size[1] -1, maze_size[0] -1) == 0:
        print("Maze is not possible to solve.\n")
        exit(0)
    #print(parsed_state['levels_completed'])
    

