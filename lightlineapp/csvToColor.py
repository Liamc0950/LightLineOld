#THIS FILE IS JUST A BACKUP OF THE CODE TO POPULATE THE COLOR MODEL

"""
    csv = open('lightlineapp/roscolux.csv', 'r')  
    for line in csv:
        print(line)
        line =  line.split(',')
        print("Hello" + str(len(line[0])) + "there")
        if len(line[0]) == 1:
            pass
        else: 
            color = Color()  
            color.colorName = line[1]
            color.colorCode = line[0]  
            color.colorHex = line[2]
            color.save()  

    csv.close() 
    
"""