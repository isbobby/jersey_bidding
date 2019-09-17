import csv


def create_userpassword_csv(data):
    """ returns (file_basename, server_path, file_size) """
    file_basename = 'userPasswordList.csv'
    server_path = ''
    w_file = open(server_path+file_basename,'w')
    
    # append column headers
    headerRow = ""
    headerRow += "Room Number,"
    headerRow += "Name,"
    headerRow += "Email,"
    headerRow += "Username,"
    headerRow += "Password,"
    w_file.write(headerRow + '\n')

    for user in data:
        currentRow = ""
        currentRow += user.roomNumber + ","
        currentRow += user.name + ","
        currentRow += user.flaskUser.email + ","
        currentRow += user.flaskUser.username + ","
        currentRow += user.flaskUser.password

        w_file.write(currentRow + '\n') ## row_as_string[1:-1] because row is a tuple

    w_file.close()

    w_file = open(server_path+file_basename,'r')
    file_size = len(w_file.read())
    return file_basename, server_path, file_size