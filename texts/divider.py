f = open('eng-uk_web_2002_1M-sentences.txt', 'r')
for filenumber in range(0, 10):
	fo = open('./' + str(filenumber) + '.txt', 'w')
	for k in range(0, 100000):
		fo.write(f.readline())
