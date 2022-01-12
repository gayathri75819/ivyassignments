from flask import Flask, jsonify, request
  

playerData = {"X":None,"O":None}
m=[["_","_","_"],["_","_","_"],["_","_","_"]]
s=1
def check_empty(row,col):
    if m[row][col]=="_":
        return True
    else:
        return False

def winning_probability():
    if m[0][0]==m[0][1]==m[0][2]=="X" or m[0][0]==m[0][1]==m[0][2]=="O":
        return True
    elif m[1][0]==m[1][1]==m[1][2]=="X" or m[1][0]==m[1][1]==m[1][2]=="O":
        return True
    elif m[2][0]==m[2][1]==m[2][2]=="X" or m[2][0]==m[2][1]==m[2][2]=="O":
        return True
    elif m[0][0]==m[1][0]==m[2][0]=="X" or m[0][0]==m[1][0]==m[2][0]=="O":
        return True
    elif m[0][1]==m[1][1]==m[2][1]=="X" or m[0][1]==m[1][1]==m[2][1]=="O":
        return True
    elif m[0][2]==m[1][2]==m[2][2]=="X" or m[0][2]==m[1][2]==m[2][2]=="O":
        return True
    elif m[0][0]==m[1][1]==m[2][2]=="X" or m[0][0]==m[1][1]==m[2][2]=="O":
        return True
    elif m[0][2]==m[1][1]==m[2][0]=="X" or m[0][2]==m[1][1]==m[2][0]=="O":
        return True
    else:
        return False

def check_all_filled():
    for i in m:
        if "_" in i:
            return False
    return True
app = Flask(__name__)

@app.route('/setPlayer', methods = ['GET', 'POST'])
def setPlayer():
    global playerData,s
    if(request.method == 'GET'):
       data=playerData
       return jsonify({'data': data})
    if(request.method == 'POST'):
        try:
            p1 = request.form.get('p1')
            p2 = request.form.get('p2')
            playerData["X"] = p1
            playerData["O"] = p2
            return jsonify({'data': playerData})
        except:
            return jsonify({"message":"badRequest"})


@app.route('/letsPlay', methods = ['GET', 'POST'])
def letsPlay():
    msg=''
 
    global playerData,s
    if(request.method == 'POST'):
        if playerData["X"] == None or playerData["O"] ==  None:
            data = "Not have en info"
           
        else:
            row = int(request.form.get('row'))
            col = int(request.form.get('col'))
            player = request.form.get('player')
            data = [row,col,player]
            if check_all_filled():
                msg = " It is Draw"
            else:
                if s%2==1 and playerData["X"]==player:
                    if check_empty(row,col):
                        m[row][col]="X"
                        s=s+1
                        msg = "Data is now filled"
                        if winning_probability():
                            msg=playerData["X"]+" is the winner"
                    else:
                        msg="Take another position it is filled"

                elif s%2==0 and playerData["O"]==player:
                    if check_empty(row,col):
                        m[row][col]="O"
                        s=s+1
                        msg = "Data is now filled"
                        if winning_probability():
                            msg=playerData["O"]+" is the winner"
                    else:
                        msg="Take another position it is filled"
                else:
                    msg = "Same playe can't enter twice"
                data=m
            
        return jsonify({'data': data,'msg':msg})

@app.route('/resetData', methods = ['GET', 'POST'])
def resetData():
    global m
    if(request.method == 'GET'):
        playerData = {"X":None,"O":None}
        m=[["","",""],["","",""],["","","_"]]
        return jsonify({'data': playerData})
  
if __name__ == '__main__':
  
    app.run(debug = True)