#### Recommendations

1. How long did you spend working on the problem? What did you find to be the most
difficult part?

    ```I spend 3 hours for this solution. I was a bit rusty with python since I don't use it on a day to day basis```

2. How would you modify your data model or code to account for an eventual introduction
of new, as-of-yet unknown types of covenants, beyond just maximum default likelihood
and state restrictions?
```
public class WeatherRule {

    public boolean checkBanned(@Fact("rain") boolean rain) {
        return rain;
    }
    
    @Action
    public void takeAnUmbrella() {
        System.out.println("It rains, take an umbrella!");
    }
}
```

3. How would you architect your solution as a production service wherein new facilities can
be introduced at arbitrary points in time. Assume these facilities become available by the
finance team emailing your team and describing the addition with a new set of CSVs.

4. Your solution most likely simulates the streaming process by directly calling a method in
your code to process the loans inside of a for loop. What would a REST API look like for
this same service? Stakeholders using the API will need, at a minimum, to be able to
request a loan be assigned to a facility, and read the funding status of a loan, as well as
query the capacities remaining in facilities.


5. How might you improve your assignment algorithm if you were permitted to assign loans
in batch rather than streaming? We are not looking for code here, but pseudo code or
description of a revised algorithm