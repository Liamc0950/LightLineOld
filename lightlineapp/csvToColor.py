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

    csv = open('lightlineapp/lee.csv', 'r')  
    for line in csv:
        print(line)
        line =  line.split(',')
        print("Hello" + line[0] + "there")
        if len(line[0]) == 1:
            pass
        if line[0] == "COLOR CODE":
            pass
        else:
            color = Color()  
            color.colorName = line[1]
            color.colorCode = line[0]
            color.colorHex = line[2]
            color.save()  

    csv.close() 

GOBOS
    csv = open('lightlineapp/roscoGobosClean.csv', 'r')  
    for line in csv:
        print(line)
        line =  line.split(',')
        if len(line[0]) == 1:
            pass
        if line[0] == "GOBO CODE":
            pass
        else:
            try:
                gobo = Gobo()  
                gobo.goboCode = line[0]
                gobo.goboName = line[1]
                gobo.imageUrl = line[2]
                gobo.save()  
            except:
                print(line[0] + "NOT ADDED" )
    csv.close() 




"""