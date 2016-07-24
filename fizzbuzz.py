#fizzbuzz
for i in xrange(1,100):
	if(i % 3 == 0) and not(i%5==0):
		print('fizz')
	elif(i % 5 == 0) and not(i%3 == 0):
		print('buzz')
	elif(i%5 == 0) and (i%3 == 0):
		print('fizzbuzz')
	else:
		print str(i)