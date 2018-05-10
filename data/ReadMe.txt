This folder should conatin 5 files (excluding this one). These files are normally in this folder by default. 
Their names are:
	breaks.txt
	ringschedule.txt
	schooldays.txt
	satschooldays.txt
	wdayswithoutschool.txt


The files should contain the following:

	breaks.txt:
		This file is used to store the time of school holidays.
		The dates in the files must be excluded from the holiday.
			For example: The first day of the break is 09/05/2018 and the last day is 20/05/2018.
				In this case the file should contain 08/05/2018 as the first date, and 21/05/2018 as the second one.
				NOTE: The start date should be the first, and the end date should be the second
		The starting and the ending date must be separated with a single space
		The dates should be in a DD/MM/YY format. For example 09/05/2018
			NOTE: If the number of the day and/or the month has only one digit, put a zero before it. Without the zero digit it does some weird stuff (I have no clue why)
		Each break's dates have to be in a new line.
		Example:
			05/11/2017 12/11/2017
			13/01/2018 21/01/2018

	ringschedule.txt:
		This file is used to store the times when the bell should "ring".
		The start and the end time of each class should be on the same line, separated with a space.
			NOTE: The start time should be the first, and the end time should be the second.
		The hours and minutes should be separated by a ':'
		Each classes starting and ending times should be on a new line.
		Example:
			8:00 8:45
			9:00 9:45
			10:00 10:45
			10:55 11:40
	
	schooldays.txt:
		This file is used to store the days of the week, on which education is done.
		The days have to be on one line, separated by space:
		The possible values you can type in:
			Mon Tue Wed Thu Fri Sat Sun
			NOTE: This is kinf of case sensitive, so you may want to type it in each startin with upper-case letters.
		Example:
			Mon Tue Wed Thu Fri

	satschooldays.txt:
		This file is used to contain the dates of the saturdays that happen to be workdays.
			NOTE: You can store any date here, on which you want the bell to ring, but otherwise it wouldn'that
			NOTE: This can override breaks
		Each date should be on a new line.
		The formatting is the same as in breaks.txt.
		Example:
			12/05/2018
			03/03/2018

	wdayswithoutschool:
		This file is the opposite to the satschooldays.txt. It contains the dates, on which there isn't school, but normally there would be.
		Formatting is the same as satschooldays.txt