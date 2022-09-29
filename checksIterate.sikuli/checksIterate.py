# Use control-F12 to abort

action = "Running.png"
wait(action)
running = True

def runHotkey (event) :
    global running
    print "Hot key abort"
    running = False

Env.addHotkey(Key.F12, KeyModifier.CTRL, runHotkey)

Settings.MouseMoveDelay = 0.125

config = {
        "validateRunning": action,
        "checkSize": 40,
        "waitForValidate": 0.25,
        "menuRegion": Region(1,106,240,705),
        "scrollBarRegion": Region(241,54,8,758)
        }

print 'Running'

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

def getGroupsFromDisplayedMenu(config):
    region = config["menuRegion"]
    print "Searching for Group Headers"
    selectedGroupExpanded = Pattern("SelectedGroupExpanded.png").similar(0.83)
    selectedGroupCollapsed = Pattern("SelectedGroupCollapsed.png").similar(0.83)
    deselectedGroupCollapsed = Pattern("deselectedGroupCollapsed.png").similar(0.83)
    deselectedGroups = findAllImages(region, [], deselectedGroupCollapsed, selected = False, expanded = False)
    selectedCollapsed = findAllImages(region, [], selectedGroupCollapsed, selected = True, expanded = False)
    selectedExpanded = findAllImages(region, [], selectedGroupExpanded, selected = True, expanded = True)

    groups = deselectedGroups + selectedCollapsed + selectedExpanded
    groups = sorted(groups, key=by_y) # sort keys by y order
    
    print "found groups = ", len(groups)
    
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

def getCheckDivisionsFromDisplayedMenu(region):
    print "Searching for check dividers in region ", region
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

def verifyNotCrashed(config):
    global running
    
    if not running:
        print "Detected that user cancelled"
        return False
            
    waitForValidate = config["waitForValidate"]
    success = False
    sleep(waitForValidate)
    try:
        wait(action)
    except:
        print "App has crashed"
        success = False
    else:
        success = True
        
    return (success)

def getYforDivider(divider):
    div = divider["match"]
    y = div.y + div.h + 5
    return y

def doCheck(config, y):
    success_ = False
    region = Region(30, y, 169, 30)
    text = region.text()
    print "At y=", y, " found text: ", text
    click(region)
    success_ = verifyNotCrashed(config)
    return (success_)


def iterateGroupSegment(config, autoScrolled):
    scrollBarRegion = config["scrollBarRegion"]
    checkHeight = config["checkSize"]
    print " scrollBarRegion = ", scrollBarRegion
    region = config["menuRegion"]
    print " region = ", region
    startY = region.y + checkHeight * 0.3
    print "startY = ", startY
    sleep(0.5)
    startScrollBar = scrollBarRegion.getScreen().capture(scrollBarRegion)
    print " startScrollBar = ", startScrollBar

    if autoScrolled:
        startY = region.y + region.h/3
        print "auto scrolled, setting startY = ", startY
    
    results = getGroupsFromDisplayedMenu(config)
    if (results["selected"]):
        match = results["selected"]["match"]
        region_ = Region(30, match.y, 169, 30)
        text = region_.text()
        print "Starting at group ", text, " at ", region_
        
        if (results["collapsed"]):
            print "Expanding selection ", match
            click(match)
            success = verifyNotCrashed(config)
            if not success:
                print "crashed";
            else:
                results = getGroupsFromDisplayedMenu(config)
        else:
            print "Already expanded"
    
        div = results["selected"]["match"]
        startY = div.y + div.h
        print "Starting at ", startY
    else:
        print "No Selection found"

    scrollBarRegion = config["scrollBarRegion"]
    maxY = region.y + region.h
    print "maxY = ", maxY
    endAtGroup = None
    
    # find end point of checks
    groups = results["groups"]
    for group in groups:
        match = group["match"]
        y = match.y
        if y < startY:
            print "Skipping group y ", y
        else:
            print "Will end at group y", y
            maxY = y
            print "maxY = ", maxY
            endAtGroup = match
            region_ = Region(30, endAtGroup.y, 169, 30)
            text = region_.text()
            print "Ending at group ", text, " at ", region_
            break
    
    checkHeight = config["checkSize"]
    maxGap = checkHeight * 1.4
    divisions = getCheckDivisionsFromDisplayedMenu(region)
    lastY = 10000
    steps = []
    y = getYforDivider( divisions[0])
    steps.append(y - checkHeight)
    for divider in divisions:
        y = getYforDivider( divider)
        while (y - lastY) > maxGap:
            newY = lastY + checkHeight
            steps.append(newY)
            lastY = newY
            print "Filling in ", newY
        steps.append(y)
        lastY = y

    while y < maxY:
        newY = y + checkHeight
        steps.append(newY)
        y = newY
        
    print "steps: ", steps
    checkFailed = False
    
    for y in steps:
        centerClickY = y + checkHeight / 2
        if centerClickY > maxY:
            break;
        if centerClickY > startY:
            success = doCheck(config, y)
            if not success:
                checkFailed = True
                break;
        else:
            print "skipping over check at ", centerClickY

    if running:
        autoScrolled = False
        sleep(1)
        scrollbarUnchanged = scrollBarRegion.exists(startScrollBar.getFile(), 1)
        if not scrollbarUnchanged:
            print "Scrollbar moved"
            autoScrolled = True
        else:
            print "scrollbarUnchanged = ", scrollbarUnchanged
            if endAtGroup:
                print "Selecting next group = ", endAtGroup
                click(endAtGroup)
            else:
                scrollClickAt = Region(scrollBarRegion.x, maxY-2, scrollBarRegion.w, 2)  
                print "Scrolling down ", scrollClickAt
                click(scrollClickAt)
    
        return {
            "scrollbarUnchanged": scrollbarUnchanged,
            "checkFailed": checkFailed,
            "autoScrolled": autoScrolled,
            "endAtGroup": endAtGroup
        }
    
    return {}
        
autoScrolled = False;
checkFailed = False;
page = 0
while not checkFailed and running:
    page = page + 1
    print "Starting Group ", page
    results = iterateGroupSegment(config, autoScrolled)
    print "Group ", page, " results: ", results

    if not running:
        break
    
#    ok = popAsk("continue?")

#    if not ok:
#        print "Cancelled"
#        break

    if results["checkFailed"]:
        break

    autoScrolled = results["autoScrolled"]


# if scrolled
    
print "done"

