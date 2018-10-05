"""
	The purpose of this application is to simply plan out my day and have it in a logically 
	stored format

	#Current version review and edit and reset and time analytics and to do list
	
"""
import csv
from collections import Counter
import matplotlib.pyplot as plt

#Instructions
#-----------------------------------------------------------------------

#Note all loops end with 'Done' as input from initial question


# First make two lists. One of times ranging from 5:00 AM to 22:00 PM
#-----------------------------------------------------------------------
#Initial Conditions portion of application
#Make a list of times
def times():
	t = []
	for i in range(5,24):
		i = str(i)
		t += [i+':00']
		t += [i+':30']
	
	return t
	
# Next list of blank spaces shown by '-'

def blanks():
	b = ['-'] *38

	return b
	

# List of Days to keep at begining of new data set
def days():
	days = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']

	return days


#Save the two lists into a csv along with heading. 
#Saves files for Monday, Tuesday, Wednesday, Thursday, Friday, Saturday and Sunday
#Depending on which file name stated
def saving(time,blank,day,filename):
	filehandle = open("{}.csv".format(filename),'w+')
	filehandle.write("{}\n".format(filename))
	for i in range(len(time)):
		filehandle.write("{},{}\n".format(time[i],blank[i]))
	filehandle.close()		

#-------------------------------------------------------------------------
# Review portion of application to just view the current files

def review(filename):
	filehandle = open("{}.csv".format(filename),'r')
	reader = csv.reader(filehandle)
	print('======================================')
	print("{: ^38s}".format(filename))
	print('======================================')
	before = ['0']
	count = 0
	for i in reader:
		
		if len(i) == 2:
			print("{:6}".format(i[0]),end="")
			print('|',end="")
			if before[count] == i[1] and before[count] != '-':
				print("{:>18}".format('|'))
			else:	
				print("{:>20}".format(i[1]))

			before += [i[1]]
			count += 1
	print('======================================')	
		
	filehandle.close()

#Selection to pick which day to review

def review_day():
	print()
	which_day = input("Review which day?: ")
	print()
	review(which_day)

#This will review the whole week
def review_week():
	print()
	week = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
	for i in week:
		review(i)

#-------------------------------------------------------------------------
#This section is for editing the days

#This will generate the lists that will need to be edited
def list_generator(filename):
	filehandle = open("{}.csv".format(filename),'r')
	reader = csv.reader(filehandle)

	times = []
	blanks = []
	for i in reader:
		if len(i) == 2:
			times += [i[0]]
			blanks += [i[1]]

	filehandle.close()		
	return times, blanks		

# This will edit the lists generated by list_generator
def edit():
	which_day = input("Review which day?: ")
	review(which_day)
	t,b = list_generator(which_day)
	num_of_entries = 10
	
	#Type Done to end the loop
	for i in range(num_of_entries):
		edit = input("Time to edit?: ")				#This will select the time to edit
		if edit == 'Done':							#If 'Done' is typed will exit loop
			break	
		else:
			#Try is if things are typed wrong it will tell you why and start the loop over here	
			try:
				how_long = eval(input("How long? (1=30min): "))
			#This Loop will change the '-' associated at the edit time with the exception of 'Done'
					
				for j in range(len(t)):
					if edit == t[j]:
						b[j] = input("Entry?: ")
						#This loop changes how many of the values are edited with the How long input
						for l in range(how_long):
							b[j+l] = b[j]
			
			except:
				print('Youve put in the wrong values try the values again')				

	saving(t,b,days(),which_day)
	review(which_day)

#----------------------------------------------------------------------------	
#restart section
#this sections resets either the week or a specific day by calling initial functions

def restart():					#This will restart the week
	t = times()
	b = blanks()
	d = days()

	for i in d:
		saving(t,b,d,i)

def restart_day(day):
	t = times()
	b = blanks()
	d = days()
	saving(t,b,d,day)		

#----------------------------------------------------------------------------
#Time analytics

#This function is used to narrow the categories in the pie plot of how you spend your time
def input_category():
	filehandle = open('categories.csv','a+')
	category = []
	clase = []
	for i in range(10):
		categor = input('Activity?: ')
		#Again loop is canceled if 'Done' is called
		if categor == 'Done':
			break
		clas = input('Class Label?: ')	
		clase += [clas]
		category += [categor]

	for i in range(len(clase)):
		filehandle.write("{},{}\n".format(clase[i],category[i]))

		
	filehandle.close()		

#This function will read the values associated with the previous function
def categories(entry):
	filehandle = open('categories.csv','r')
	reader = csv.reader(filehandle)

	clase = []
	category = []
	for i in reader:
		clase += [i[0]]
		category += [i[1]]
	

	for i in range(len(entry)):
		for j in range(len(category)):
			if entry[i] == category[j]:
				entry[i] = clase[j]
	
	return entry	

	filehandle.close()

def time_analytics():
	d = days()
	blanks = []
	for i in d:
		t,b=list_generator(i)
		blanks += b

	entries = []
	for x in blanks:
		if x != '-':
			entries += [x]

	entries=categories(entries)		

	analytics = Counter(entries)
	times = analytics.values()
	entry = analytics.keys()		
		
	return list(times),list(entry)		

#Generate a pie plot based on the information
def pie_plot(t,e):
	
	ax1 = plt.subplot()
	ax1.pie(t,labels=e,autopct='%0.1f%%',startangle=90)

	centre_circle = plt.Circle((0,0),0.80,fc='white')
	fig = plt.gcf()
	fig.gca().add_artist(centre_circle)

	ax1.axis('equal')
	plt.text(0,0,'How you spend your time',horizontalalignment='center',verticalalignment='center',weight="bold",fontsize=12)
	plt.tight_layout()
	plt.show()

#Need to save the blanks stored to keep the analytics up	

#---------------------------------------------------------------------------
#To Do List

#The Goal of this section is to save a to do list, if there is a date involved in the


def add_to_list(filename):
	filehandle = open("{}.csv".format(filename),'a+')
	l = []
	d = []
	for i in range(10):
		to_do = input("To Do?: ")
		if to_do == 'Done':
			break
		l += [to_do]
		day = input("Day?: ")
		d += [day]

	for i in range(len(l)):
		filehandle.write("{},{}\n".format(l[i],d[i]))
	filehandle.close()

			

def review_to_do(filename):
	filehandle = open("{}.csv".format(filename),'r')
	reader = csv.reader(filehandle)

	to_do=[]
	days=[]
	for i in reader:
		to_do+=[i[0]]
		days+=[i[1]]
	print('============================================================')
	print("{:^60s}".format('To Do List'))
	print('============================================================')
	for i in range(len(to_do)):
		print(to_do[i],':',end="")
		print("{}".format(days[i]))

	print()	
			
	filehandle.close()
		

#This function will generat two lists from the to_do.csv list
def out_to_do(filename):
	filehandle = open("{}.csv".format(filename),'r')
	reader = csv.reader(filehandle)

	to_do=[]
	days=[]
	for i in reader:
		to_do+=[i[0]]
		days+=[i[1]]

	return to_do, days	


def remove_to_list(filename):
	to_do,days=out_to_do(filename)
	to_do_new=[]
	days_new=[]
	remove = input("Remove?: ")
	
	for i in range(len(to_do)):
		if to_do[i]	!= remove:
			to_do_new += [to_do[i]]
			days_new += [days[i]]
		else:
			pass
	
	filehandle = open("{}.csv".format(filename),'w')
	for i in range(len(to_do_new)):
		filehandle.write("{},{}\n".format(to_do_new[i],days_new[i]))
	filehandle.close()

	return remove	

#This will repeat the remove list process only way I could find to repeat it without
#Compounding effects
def repeat_remove(filename):
	for i in range(10):
		remove = remove_to_list(filename)
		if remove == 'Done':
			break 
		

def reset_to_do(filename):
	filehandle = open('{}.csv'.format(filename),'w')
	filehandle.close()


#Sub Program outside of the main program easily recallable for later
def to_do_list():
	question_2 = eval(input("1:Add, 2:Remove, 3:Review, 4:Reset    "))
	if question_2 == 1:
		add_to_list('to_do')
		review_to_do('to_do')
		to_do_list()

	elif question_2 == 2:
		review_to_do('to_do')
		repeat_remove('to_do')
		review_to_do('to_do')
		to_do_list()

	elif question_2 == 3:
		review_to_do('to_do')
		to_do_list()

	elif question_2 == 4:
		reset_to_do('to_do')
		to_do_list()

	else:
		print("Goodbye!")	

#---------------------------------------------------------------------------
#Main Program

def main():
	print()
	print()
	print()
	print()
	print('============================================================')
	print('{:^60s}'.format('Welcome to Calendar App'))
	print('============================================================')
	try:
		print('Please Select from the Following')
		print('-------------')
		print("1:Review.    |")
		print("2:Edit.      |")
		print("3:Resets.    |")
		print("4:Analytics  |")
		print("5:To Do List |")
		print('-------------')
		print()
		question = eval(input())
	
		if question == 1:
			q = eval(input("Review a day (1) or week(2)?: "))		#NOT WORKING?
			if q == 1:					
				review_day()
				main()
			else:
				review_week()
		
				main()
		
		elif question == 2:
			
			edit()
			main()
			


		elif question == 3:
			q = eval(input("1:Restart week, 2:Restart day     "))
			if q == 1:
				restart()
				main()
			else:
				q2 = input("Which day?: ")
				restart_day(q2)
				review(q2)
				main()

		elif question == 4:
			select = eval(input('1:Time Analytics, 2:Input Categories:   '))
			if select == 1:
				t,e = time_analytics()
		
				pie_plot(t,e)

				main()	

			elif select == 2:
				input_category()	

				main()
		
		elif question == 5:
			to_do_list()
			main()
				
		else:	
			print('======================================')
			print("{:^38s}".format('Goodbye!'))
			print('======================================')

	except NameError:
		print()
		print()
		print()
		print('============================================================')
		print("{:^60s}".format('Goodbye!'))
		print('============================================================')




main()





	
