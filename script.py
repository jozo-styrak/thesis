''' reads file and outputs each sentence to a new file '''
text = open('data/02162014-filtered.txt', 'r')

i = 1

for line in text.readlines():
    if len(line) > 0:
        sentence_file = open('data/sentences/' + str(i).rjust(3, '0') + '.txt', 'w')
        sentence_file.write(line.strip())
        sentence_file.close()
        i += 1
        
text.close()