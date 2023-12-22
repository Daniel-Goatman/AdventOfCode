import re
import json
import copy
# https://www.reddit.com/r/adventofcode/comments/18lwcw2/2023_day_19_an_equivalent_part_2_example_spoilers/


rules_and_parts = """px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}"""

"""
Wrong nums:

Too high:
313610847733818
303704098603397
264313075068896


Just not right(no hint given):
111072522154149
191761338267015



201069326405216
"""


#with open('parts_processes.txt', 'r') as f:
#    rules_and_parts = f.read()


rules, parts = rules_and_parts.split('\n\n')



processes = {} #Rule storage


rules = rules.split()
for i in range(len(rules)):
    rule = rules[i]
    name = re.match('^\w+', rule).group(0)
    #print(rule)

    checks = re.findall(r'[\w><:]+,*', re.search(r'\w+\{(.*)\}', rule).group(1))

    processes[name] = checks






def plug_vals_in_check(process_key, bounds, depth):
    #print(f'\n{depth}: {process_key}, {bounds}')
    combos = 0
    if process_key == 'A':

        prod = 1
        print(bounds)
        for bound in bounds.values():
            bound = bound[1]-bound[0]+1

            prod *= bound
        if prod < 0:

            print(f'Negative nums accepted at depth {depth} with {bounds}')

        #print(f"{prod} combos at {depth}")
        return prod
    
    elif process_key == 'R':
        return 0
    

    checks = processes[process_key]

    conditions = {}

    conditional_routes = []
    last_route = None


    for check in checks:
        if ':' in check:
            condition = check[:check.index(':')]
            
            key = re.match('\w', condition).group(0)
            operator = re.search(r'(>|<)', condition).group(0)
            val = int(re.search(r'\d+$', condition).group(0))


            success_key = re.search(r'\w+', check[check.index(':')+1:]).group(0)
            conditional_routes.append((key, success_key))

            conditions[key] = {operator:val}

        else: # Goes to another process
            last_route = check


    for key, target in conditional_routes: # Perform check on each condition
        if target == 'A' and key == 'm':
            print(f'here')
        bounds_copy = copy.deepcopy(bounds)
        val = conditions[key].get('>') 
        if val:
            
            if bounds_copy[key][1] <= val: # Skip if max boundary is smaller than val

                continue

            bounds_copy[key] = [val+1, bounds_copy[key][1]] #Get all values beyond the boundary
        else:
            val = conditions[key].get('<')
            if  bounds_copy[key][0] >= val: # Skip if min boundary is larger than val
                continue

            bounds_copy[key] = [bounds_copy[key][0], val-1] #Get all values before the boundary
           


        #need to get the bounds of these other bounds up until their conditional value 
        
        others = {c_key:c_val for c_key, c_val in list(zip(conditions.keys(), conditions.values()))[:conditional_routes.index((key, target))]}#Get all conditions up to the current condition

        should_check = True
        if len(list(others.keys())) > 0:
        

            for other_key in others.keys(): # Set the bounds for the conditions to be everything before/beyond their conditional value
                c_val = others[other_key].get('>')

                #this needs to check if all the fields in the check are within the val
                if c_val:

                    if bounds_copy[other_key][0] > c_val:
                        should_check = False
                        break
                    bounds_copy[other_key] = [bounds_copy[other_key][0], c_val]
                else:
                    c_val = others[other_key].get('<')
                    print(other_key,'<', c_val)
                    if bounds_copy[other_key][1] < c_val:
                        should_check = False
                        break
                    bounds_copy[other_key] = [c_val, bounds_copy[other_key][1]]
                    
        if should_check:
            combos += plug_vals_in_check(target, bounds_copy, depth + 1)



    # For the final value in the rule
        

    other_routes = {c_key:c_val for c_key, c_val in list(zip(conditions.keys(), conditions.values()))}
    
    check_last = True

    for other_key in other_routes.keys(): # set the bounds to exclude everything beyond/before the conditional values.
        val = other_routes[other_key].get('>')

        # this needs to set the check_last to False if all the values for a field are within the boundary

        if val:

            if bounds[key][0] > val or bounds[key][1] < val: # Skip if min boundary is beyond value or max is less than val
                check_last = False
                break

            bounds[other_key] = [bounds[other_key][0],val]
        else:
            val = other_routes[other_key].get('<')
            
            if bounds[key][1] < val or bounds[key][0] >val: # Skip if max boundary is beyond value
                check_last = False
                break

            bounds[other_key] = [val, bounds[key][1]]

    if check_last:

        combos += plug_vals_in_check(last_route, bounds, depth + 1)

    return combos

print(plug_vals_in_check('in', {'x':[1,4000],'m':[1,4000],'a':[1,4000],'s':[1,4000]}, 0))





#part 1 stuff
def do_check(part:dict, process_key):

    checks = processes[process_key]

    #print(f"checking {part} in {process_key} with {checks}")
    for check in checks:
        if ':' in check:
            condition = check[:check.index(':')]
            
            key = re.match('\w', condition).group(0)
            operator = re.search(r'(>|<)', condition).group(0)
            val = int(re.search(r'\d+$', condition).group(0))


            success_key = re.search(r'\w+', check[check.index(':')+1:]).group(0)
            
            if operator == '>':
                if part[key] > val:
                    #print(f'The thing happened with {part}, {part[key]} passed the boundary of {val}')
                    if not success_key in ['R', 'A']:
                        return do_check(part, success_key)
                    else:

                        return success_key == "A"
                    
            elif operator == '<':
                if part[key] < val:
                    #print(f'The thing happened with {part}, {part[key]} it passed the boundary of {val}')

                    if not success_key in ['R', 'A']:
                        return do_check(part, success_key)
                    else:
                        #print(f'Returning {val}')
                        return success_key == "A"
           # print(key, operator, val, success_key)

        else: #is not a check

            if check in ['A', 'R']:
                return check == 'A'
            else:
            
                return do_check(part, check)

def check_parts():
    first_check = list(processes.keys())[0]

    total = 0
    for part in parts.split():
        parts = part.replace('{', '').replace('}', '').split(',')

        x,m,a,s = [int(i[i.index('=')+1:]) for i in parts]

        xmas = {'x':x,'m':m,'a':a,'s':s}
        #print(x,m,a,s)

        res = do_check(xmas, "in")

        print(f'{xmas} returned {res}')
        if res:
            total += sum(list(xmas.values()))

    print(total)