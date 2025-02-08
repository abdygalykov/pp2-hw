def unique(lst):
    unique_elements = []

    for i in range(len(lst)):  
        flag = 0  

        for j in range(len(unique_elements)):
            if lst[i] == unique_elements[j]:
                flag = 1 
                break  
        
        if flag == 0:  
            unique_elements.append(lst[i])

    return unique_elements


print(unique([1, 2, 2, 3, 4, 4, 5]))

