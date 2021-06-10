#### Recommendations

1. How long did you spend working on the problem? What did you find to be the most
difficult part?

    ```I spend 3 hours for this solution. I was a bit rusty with python since I don't use it on a day to day basis```

2. How would you modify your data model or code to account for an eventual introduction
of new, as-of-yet unknown types of covenants, beyond just maximum default likelihood
and state restrictions?
```
I would consider chaining a series of filters and then chain them together rather than using if else.
We can a Rule class that create a rule or a rule file

def rule(variable):
    letters = ['a', 'e', 'i', 'o', 'u']
    if (variable in letters):
        return True
    else:
        return False
# using filter function
filtered = filter(fule, sequence)

This example. We can explore how to create rules and then create filters.
https://zerosteiner.github.io/rule-engine/getting_started.html  - Looks like a rule engine that can leveraged to create rules for the covenants
```

3. How would you architect your solution as a production service wherein new facilities can
be introduced at arbitrary points in time. Assume these facilities become available by the
finance team emailing your team and describing the addition with a new set of CSVs.
```
To allow arbitrary number of files to be added, we must use Spark to read files from the hadoop if there are large number of files. Optionally having Apache hive allows better manipulation of data and supports efficient compression

Spark allows better maninpulation of data that is more effective when transformation has to be done to the  data.
```
4. Your solution most likely simulates the streaming process by directly calling a method in
your code to process the loans inside of a for loop. What would a REST API look like for
this same service? Stakeholders using the API will need, at a minimum, to be able to
request a loan be assigned to a facility, and read the funding status of a loan, as well as
query the capacities remaining in facilities.
```
For the REST API 
    POST call 
        get_loan_approval(interest_rate,amount,id,default_likelihood,state)
            This should fetch facilities that are greater than and equal to the default_likelihood and states that are not banned
            and with the lowest interest rate.
        Output 
           Assignments => loan_id, facility_id, status
        
        Status of the funding should include if the facilty has transferred the funds to affirm or initiated.
        Evnetually there should be an event queue where the status of loan should be reported since funds don't get transferred immedidately  
```

5. How might you improve your assignment algorithm if you were permitted to assign loans
in batch rather than streaming? We are not looking for code here, but pseudo code or
description of a revised algorithm
```
    If the loan is batched, I would find facilities where the interest is the same, in those cases choose the amount in the facility 
that is the lowest
        
    We can consider the loans as packages and the facilities as bins that have to be filled. Each facility(bin) has a max amount(capacity of the bin).  This is a variant of bin packing problem.

What we want here is add the loan to a facility and check if are able fit all the loans in the batch, otherwise change the configuration  by moving the loan to a different facility

https://www.localsolver.com/docs/last/exampletour/binpacking.html

This looks closest to the problem we are trying to solve here.

            
```
6. Discuss your solution’s runtime complexity.
```
O(mn)
m = number of loans
n = no of covenants or no of facilities depending which ever is larger
All the covenants have to be visited to get all facilities that meet the constraints
Then for each combination of facility and bank from the previous step, we are visiting all the facilities.
If facilities is absent in a covenant, we have no other way to get all the facilties associated with the bank, then find the cheapeast interest rate
```
```