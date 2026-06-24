# 1. დაწერეთ პროგრამა, რომელიც მომხმარებელს შემოაყვანინებს წინადადებას, პირველ სიტყვას, მეორე სიტყვას და შემოყვანილ წინადადებაში
# პირველ სიტყვას ჩაანაცვლებს მეორე სიტყვით

sentence = input("Enter a sentence: ")
first_word, second_word = input("Enter a word from the sentence that you want replaced "
"and the word you want to replace it with (Separated by a space): ").split()
print(f"The new sentence is: {sentence.replace(first_word, second_word)}")
print("-----------------------------------------------------------------")

# 2. დაწერეთ პროგრამა, რომელიც მომხმარებლის მიერ შემოყვანილ წინადადებაში იპოვის ყველაზე გრძელ სიტყვას და დაბეჭდავს მას.

sentence = input("Enter a sentence: ").split()
print(f"'{sorted(sentence, key=len)[-1]}' is the longest word in that sentence")
print("-----------------------------------------------------------------")

# 3. დაწერეთ პროგრამა, რომელიც მომხმარებელს შეეკითხება ორ სიტყვას შეამოწმებს არის თუ არა ერთმანეთის ანაგრამა
# ანაგრამა არის ერთ სიტყვაში ასოების გადაადგილებით მიღებული მეორე სიტყვა, მაგალითად ("listen", "silent" ), ("Triangle", "Integral")
# და ა.შ. უნდა იყოს case-insensitive, ანუ მომხმარებელი დიდი ასოებით შემოიყვანს თუ არა ტექსტს, არ უნდა ჰქონდეს მნიშვნელობა.

first_word, second_word = input("Enter your words (Separated by a space): ").lower().split()
print(f"These words are anagrams: {sorted(first_word) == sorted(second_word)}")
print("-----------------------------------------------------------------")
