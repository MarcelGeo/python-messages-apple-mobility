# python-messages-apple-mobility
Parsing and messages emmiting for apple mobility data on page https://www.apple.com/covid19/mobility

Script will output message for last processed day and merge data in database (PostgreSQL) for future manipulation.

## Example of messages from 7.5.2020 (data are available until 5.5.2020)

walking under 25 percentile (far to normal) 35.724999999999994
['Argentina' 'France' 'India' 'Indonesia' 'Ireland' 'Italy' 'Macao'
 'Morocco' 'New Zealand' 'Philippines' 'Portugal' 'Romania' 'Singapore'
 'Spain' 'Thailand' 'Uruguay']
walking over 75 percentile (over normal trnasportation) 64.86500000000001
['Belgium' 'Canada' 'Denmark' 'Estonia' 'Finland' 'Germany' 'Latvia'
 'Lithuania' 'Netherlands' 'Norway' 'Slovakia' 'Slovenia' 'Sweden'
 'Switzerland' 'Taiwan' 'Vietnam']
walking over 100 in comparison to 13.1.2020
[]
Median value is 48.85

Driving under 25 percentile (far to normal) 44.56
['Albania' 'Argentina' 'Cambodia' 'Colombia' 'France' 'India' 'Indonesia'
 'Italy' 'Macao' 'Morocco' 'New Zealand' 'Philippines' 'Portugal'
 'Romania' 'Singapore' 'Spain']
 Driving over 75 percentile (over normal trnasportation)  75.65
['Czech Republic' 'Denmark' 'Estonia' 'Finland' 'Germany' 'Iceland'
 'Latvia' 'Lithuania' 'Norway' 'Slovakia' 'Sweden' 'Switzerland' 'Taiwan'
 'Ukraine' 'United States' 'Vietnam']
Driving over 100% in comparison to 13.1.2020
['Estonia' 'Finland' 'Sweden']
Median value is 58.5

Transit under 25 percentile (far to normal) 21.65
['Ireland' 'Italy' 'New Zealand' 'Philippines' 'Singapore' 'Spain' 'UK']
Transit over 75 percentile (over normal trnasportation)  51.205
['Estonia' 'Finland' 'Germany' 'Japan' 'Norway' 'Sweden' 'Taiwan']
Transit over 100 in comparison to 13.1.2020
[]
Median value is 29.16


## Database output

PostgreSQL database is used for data storing. This will be future functionality for reading timelines with REST API builded by python.
