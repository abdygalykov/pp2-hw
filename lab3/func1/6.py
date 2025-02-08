def reverse_words(sentence):
    result = ""
    word = ""
    
    # Manually determine the length of the sentence


    i = len(sentence) - 1
    while i >= 0:
        if sentence[i] != " ":
            word = sentence[i] + word  
        else:
            if word != "":
                result += word + " "  
                word = ""  
        i -= 1

    if word != "":
        result += word

    return result



sentence = "My name is dimash"
print(reverse_words(sentence))  
