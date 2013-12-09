from numpy import *
from scipy import spatial
from matplotlib import pyplot

class agent:
    def __init__(self, name, options, distTup, pos):
        self.options = options
        self.pos = pos
        self.posList = [pos]
        self.name = name 
        self.distTup = distTup[pos]
        
    def __str__(self):
        return 'agent with pos: %s named %s' % (self.pos, self.name)
        
    def bestChoice(self):
        a = array(self.options)
        maxi = where(a == max(a))[0]
        dist = self.distTup[maxi]
        a = where(dist == min(dist))[0]
        a = maxi[a]
        self.posList += [int(a[0])]
        self.pos = int(a[0])
        return a
    
class game:  
    def __init__(self, name, iterations, numPlayers, x,y,z):
        self.name = name
        self.iterations = iterations
        self.numPlayers = numPlayers
        self.x = x
        self.y = y
        self.z = z
        self.cells = x * y * z
        self.payouts = array(random.random(self.cells)).reshape(self.cells, -1) # creates a payout dictionary, can be modified
        d1,d2,d3 = mgrid[0:self.x, 0:self.y, 0:self.z] # creates 3d grid, could be more or less
        tree = spatial.KDTree(zip(d1.ravel(), d2.ravel(), d3.ravel())) # creates the super cool tree
        dok = tree.sparse_distance_matrix(tree, 100) # query the tree for distances to all other points, can limit distance, but leads to zero issue
        self.distArray = dok.toarray() # turn the dok into an array for easy usage     
        playerList = []
        for i in range(self.numPlayers):
            pos = random.randint(0, self.cells)
            playerList.append(agent('mikeMommsen', [], self.distArray, pos))
        self.players = playerList
        
    def __str__(self):
        return 'game with %d iterations, %d players, and grid (%d,%d)'\
        % (self.iterations, self.numPlayers, self.x, self.x)       
        
    def compare(self, inList):
        # returns a 1 for minimum and a zero for non min. if there is a tie then 1/(number of mins) is returned   
        minimum = min(inList)
        winners = []   
        for i in inList:
            if i == minimum: winners.append(1)
            else: winners.append(0)
        total = float(sum(winners))
        winners = map(lambda x: x/total, winners)
        return winners
    
    def playerReturn(self, players, player, distList, payouts):
        distances = distList[array(players)]
        distances = array(distances)        
        distances = distances.transpose()
        comp = array(map(self.compare, distances))
        sums = sum(comp[...,player])
        return sums
        
    def Hotelling(self, players, player, distList, payouts, cells):
        options = []
        for cell in range(cells):
            players[player] = cell
            a = self.playerReturn(players, player, distList, payouts)
            options.append(a)
        return options
            
    def asynch(self):
        players = self.players
        distList = self.distArray
        payouts = self.payouts
        for count, player in enumerate(players):
            playerPos = map(lambda x: x.pos, players)
            player.options = self.Hotelling(playerPos, count, distList, payouts, self.cells)
            print player.pos, '\t', player.bestChoice()
            
    def synch(self):
        players = self.players
        distList = self.distArray
        payouts = self.payouts
        for count, player in enumerate(players):
            playerPos = map(lambda x: x.pos, players)
            options = self.Hotelling(playerPos, count, distList, payouts, self.cells)
            print options
            player.options = options
        for player in players:
            print player.pos, '\t', player.bestChoice()
                        
    def run(self):
        i = 0
        while i < self.iterations:
            self.synch()
            print 'Just finished iteration %d \n players are doing fine' % i
            i += 1
        print 'all iteration is done - take a look at results'
        for player in self.players:
            print player.posList
            pyplot.plot(player.posList)
        pyplot.show()
 
a = game('mike', 20,3,100,1,1)

a.run()
