# **COMP10001 Contact Tracing**

The functions uses a *visit* 7-tuple: <br/>
`("Irene", "Skylabs", 3, 9, 15, 13, 45)` <br/>
Which means that Irene spent 4 hours and 30 minutes at Skylabs from 9:15am to 1:45pm on the third day of the outbreak.

The list of *visit* 7-tuples is *visits* <br/>
A sample of this is:
 ```
 visits = [('Russel', 'Nutrity', 1, 5, 0, 6, 0),
           ('Russel', 'Foodigm', 2, 9, 0, 10, 0),
           ('Russel', 'Afforage', 2, 10, 0, 11, 30),
           ('Russel', 'Nutrity', 2, 11, 45, 12, 0),
           ('Russel', 'Liberry', 3, 13, 0, 14, 15),
           ('Natalya', 'Nutrity', 1, 5, 30, 6, 45),
           ('Natalya', 'Afforage', 2, 8, 15, 10, 0),
           ('Natalya', 'Nutrity', 4, 10, 10, 11, 45),
           ('Chihiro', 'Foodigm', 2, 9, 15, 9, 30),
           ('Chihiro', 'Nutrity', 4, 9, 45, 11, 30),
           ('Chihiro', 'Liberry', 3, 12, 15, 13, 25)]
```
This list of *visits* can be uncommented on line 19-31

## **Forward Tracing:**<br/>
This function dentifies all potential contacts of a detected index case that occurred after the time that they were detected:<br/>
`forward_contact_trace(visits, 'Russel', (1, 9, 0))`<br/>
This identifies the potential contacts of Russel using *visits* if he was infected at 9:00am on the first day of the outbreak.

The expected output is:<br/>
`['Chihiro']`

The reasoning is:
* Russel became infectious at 9am on day 1 of the outbreak.
* Russel visited Foodigm between 9am and 10am on day 2 of the outbreak.
* Chihiro also visited Foodigm during this time (from 9.15am until 9.45am), during which time she could have been infected by Russel. She should be contact traced and asked to quarantine.
* Natalya was not present in the same location at the same time as Russel after he became infectious, so she doesn't need to be contact traced.

> Source: University of Melbourne COMP10001

The function can also conduct a second-order search. This identifies potential contacts from first-order contacts.<br/>
`forward_contact_trace(visits, 'Russel', (1, 9, 0), second_order=True)`

The expected output is:<br/>
`['Chihiro', 'Natalya']`

The reasoning follows the previous; however:
* After being a potential contact of Russel, Chihiro visited Nutrity between 9:45am and 11:30am on day 4 of the outbreak.
* Natalya also visited Nutrity during this time (from 10:10am until 11:45am), during which time she could have been infected by Chihiro (had she been infected). As we are now also tracing Russel's second order contacts, she should also be contact traced and asked to quarantine.

> Source: University of Melbourne COMP10001

## **Backward Tracing**<br/>
Backward contact tracing identifies the potential source of the index case's infection by looking back through their recent contact history. <br/>
`backward_contact_trace(visits, 'Natalya', (4, 13, 0), 1)`<br/>
This means Natalya was detected at 1:00pm on day 4 of the outbreak, and we want to know who she could have been infected by earlier on the same day (as window=1).
The expected output is:<br/>
`['Chihiro']`<br/>
The reasoning is as follows:

* Natalya was detected at 1pm on day 4 of the outbreak, and we want to know who she could have been infected by earlier on the same day (as window=1).
* The only location that Natalya had visited on day 4 was Nutrity, between 10:10am and 11:45am.
* Chihiro also visited Nutrity at this time (from 9:45am until 11:30am), during which time she could have infected Natalya.
* Chihiro should therefore be contact traced and investigated as a potential source of Natalya's infection.
* (Additionally, outside of the scope of this problem, if Chihiro does test positive, forward contact tracing should be used to follow up on her other potential contacts!)

> Source: University of Melbourne COMP10001

All inputs are assumed to syntatically correct.
