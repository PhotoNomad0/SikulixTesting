action = "Running.png"
wait(action)
print 'Running'
menuRegion = Region(0,58,246,753)

def by_y(group):
    return group["match"].y

def findAllImages(region, groups, image, selected, expanded):
    print "searching for expanded: ", expanded, ", selected ", selected
    region.findAll(image)
    found = region.getLastMatches()
    while found and found.hasNext():
        match = found.next()
#        print "found expanded: ", expanded, ", selected ", selected, " : ", match
        groups.append({
                    "expanded": expanded,
                    "selected": selected,
                    "match": match
                    })
    return groups

def getGroupsFromDisplayedMenu(region):
    print "Searching for Group Headers"
    selectedGroupExpanded = Pattern("SelectedGroupExpanded.png").similar(0.83)
    selectedGroupCollapsed = Pattern("SelectedGroupCollapsed.png").similar(0.83)
    deselectedGroupCollapsed = Pattern("deselectedGroupCollapsed.png").similar(0.83)
    deselectedGroups = findAllImages(region, [], deselectedGroupCollapsed, selected = False, expanded = False)
    selectedCollapsed = findAllImages(region, [], selectedGroupCollapsed, selected = True, expanded = False)
    selectedExpanded = findAllImages(region, [], selectedGroupExpanded, selected = True, expanded = True)

    groups = deselectedGroups + selectedCollapsed + selectedExpanded
    groups = sorted(groups, key=by_y) # sort keys by y order
    
    for i in range(len(groups)):
        item = groups[i]
        print i, " expanded: ", item["expanded"], " selected: ", item["selected"], ", match: ", item["match"]

    selected = None;
    collapsed = False;

    if selectedCollapsed and len(selectedCollapsed):
        found = selectedCollapsed[0]
        print "Found selected collapsed: ", found
        selected = found
        collapsed = True
        
    elif selectedExpanded and len(selectedExpanded):
        found = selectedExpanded[0]
        print "Found selected expanded: ", found
        selected = found
        collapsed = False

    return {
            "selected": selected,
            "collapsed": collapsed,
            "groups": groups
            }
            
startY = 0
results = getGroupsFromDisplayedMenu(menuRegion)
if (results["selected"]):
    if (results["collapsed"]):
        match = results["selected"]["match"]
        print "Expanding selection ", match
        click(match)
        sleep(1)
        wait(action)
        results = getGroupsFromDisplayedMenu(menuRegion)
    else:
        print "Already expanded"

    div = results["selected"]["match"]
    startY = div.y + div.h
    print "Starting at ", startY
else:
    print "No Selection found"

            
def getCheckDivisionsFromDisplayedMenu(region):
    print "Searching for check dividers"
    unselectedDivider = Pattern("unselectedDivider.png").similar(0.74)
    beforeSelectedDivider = "beforeSelectedDivider.png"
    afterSelectedDivider = "afterSelectedDivider.png"

    checks = findAllImages(region, [], unselectedDivider, selected = False, expanded = False)
    checks = findAllImages(region, checks, beforeSelectedDivider, selected = True, expanded = False)
    checks = findAllImages(region, checks, afterSelectedDivider, selected = True, expanded = True)

    checks = sorted(checks, key=by_y) # sort keys by y order
    
    for i in range(len(checks)):
        item = checks[i]["match"]
        print i, "item: ", item

    return checks


divisions = getCheckDivisionsFromDisplayedMenu(menuRegion)
for divider in divisions:
    div = divider["match"]
    y = div.y + div.h + 5
    if y > startY:
        region = Region(30, y, 169, 24)
        text = region.text()
        print "At y=", y, " found text: " 
        uprint(text)
        click(region)
        sleep(1)
        wait(action)
    
print "done"


top = Region(35,111,170,25)
Region(37,151,37,23)
bottom = Region(33,788,42,28)
lines = 18

print "step size ", (bottom.y-top.y)/(lines - 1)
print 40 *17 + 111

checkSelected = Pattern("checkSelected.png").similar(0.80)
scrollBarRegion = Region(240,54,11,771)
