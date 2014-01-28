# MindSumo problem for CapitalOne
# Author: Andy Tien
# ctien4@jhu.edu

# First open file in universal parsing mode
# Read first line, which is the category line
f = open('pop.csv', 'rU')
f.readline() 

POP_MIN = 50000

topCitiesTarget = {}
topCitiesAvoid = {}
topStatesGrowth = {}

# For each line, extract the city, state, and population changes.
for line in f.readlines():
  city, state, p2010, p2011, p2012 = line.strip().split(',')

  city = city.strip('" ')
  state = state.strip('" ')
  
  # We effectively don't need to worry about 2011
  # Since we are only interested in growth from 2010 - 2012
  p2010 = float(p2010) 
  p2012 = float(p2012)

  # Consider this city as a top five city
  # % change between 2012 with 50,000 min

  if p2010 >= POP_MIN:
    # compute % growth
    growth = (p2012 - p2010)/(p2010) * 100
   
    # Add our growth value to the lists
    topCitiesTarget[growth] = city
    topCitiesAvoid[growth] = city
    
    # Assumption being made here: metropolitan area means its name has "city"
    if "city" in city:
      if topStatesGrowth.has_key(state):
        topStatesGrowth[state] += growth
      else:
        topStatesGrowth[state] = growth
   
    # once more than 5, constantly remove smallest or largest
    if len(topCitiesTarget) > 5:
      del(topCitiesTarget[min(topCitiesTarget)])

    if len(topCitiesAvoid) > 5:
      del(topCitiesAvoid[max(topCitiesAvoid)])

# finished processing all lines, close file
f.close()

# Now we can process the states since we have finished parsing all states:
topStatesHelper = {}
for state in topStatesGrowth:
  topStatesHelper[topStatesGrowth[state]] = state

while len(topStatesHelper) > 5:
  del(topStatesHelper[min(topStatesHelper)])

# Print output!
print "Top Five Cities to Target:"
for growth in topCitiesTarget:
  print "{} with growth of {}%".format(topCitiesTarget[growth], growth)

print "\nTop Five Cities to AVOID:"
for growth in topCitiesAvoid:
  print "{} with growth of {}%".format(topCitiesAvoid[growth], growth)


print "\nTop Five States with Highest Cumulative Growth:"
for growth in topStatesHelper:
  print "{} with cumulative growth of {}%".format(topStatesHelper[growth], growth)
