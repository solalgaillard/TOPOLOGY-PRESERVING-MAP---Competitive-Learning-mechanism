#!/usr/bin/env python
# -*- coding: utf-8 -*-

#1 - Normalize vector:
def normalize_v(V):
    m = 0
    for x in V: m += x**2 #Sum of the elements powered to the 2
    m = sqrt(m) #Get vector's norm
    return [x/m for x in V] #Divide each element of vector by its norm


#2 - Find D, euclidian distance
def euclid_dis(V):
    d=0
    for i in xrange(len(V)):
        for j in xrange(len(W[i])): #Len of matrix
            d += (V[i]-W[i][j])**2 #∑(xi – mij)**2
    return sqrt(d)


#3 - Find j*, the winning attractor
def find_att(d):
    star=[0,0] #Start with the beginning, keep coordinates in a list
    for A in xrange(Units) : # scan all units
        for B in xrange(Units) :
            if distance(W[A][B], d) < distance(W[star[0]][star[1]], d) :
                star = [A,B] # closest unit
    return star

#4 - signal de sortie de j* à 1, tous les autres à 0
#Cette fonction existe parce que l'algorithme du cours demande une sortie. Je ne vois pas l'utilité de cette dernière pour notre utilisation
def provide_sortie(sortie,star):
    for x in xrange(Units):
        for y in xrange(Units):
            if x == star[0] and y == star[1]: sortie[x][y]=1
            else: sortie[x][y]=0



#5 - règle les pondérations
#Le voisinage est ici hexagonal, dis_rad mesure la proximité de voisinage.
#Par convention, chaque ligne paire de la matrice est décalée vers la droite pour faire exister cette hexagonalité
def weighting(signal, alpha, star, radius):
    left = max(star[0] - radius, 0) # left boundary
    right = min(star[0] + radius+1, Units) # right boundary
    top = max(star[1] - radius, 0) #top boundary
    bottom = min(star[1] + radius+1, Units) #bottom boundary
    for A in xrange(left, right) : # scan neighborhood left-right
        dis_A = abs(A-star[0]) #Distance left or right with attractor j*
        for B in xrange(top, bottom): # scan neighborhood top-bottom
            dis_B = abs(B-star[1]) #Distance top or bottom with attractor j*
            dis_rad = dis_A if dis_A >= dis_B else dis_B #Distance total between neighboor element in matrix and j*, take the bigger distance
            left_lim = left + dis_B/2 #left limit contingent on vertical distance
            right_lim = right - dis_B/2 #Same for right limit
            if dis_B%2 == 1: #If distance of neighbooring attractor to j* is odd
                if B%2 == 0:left_lim += 1 #If j* row is even within the matrix, shift left limit by one to the right
                else : right_lim -= 1 #else shift right limit by one to the left
            if A >= right_lim or A<left_lim: continue #Do not modify neighbooring attractors not within the limits above, this guarantees hexagonality of the weighting process
            else:
                for i in xrange(len(signal)): #For both values of signal vector
                    W[A][B] += (signal[i] - W[A][B]) * (alpha / (1 + dis_rad))#distance degree linearized


#Fonction pilote:

from math import fabs, sqrt

def distance(u, v) : return fabs(u - v)

def new_rate(lap) : return 1 - (lap / float(T))

def teach(W) :
    alpha = ALPHAo # learning rate
    radius = Ro # neighborhood
    sortie = [[0]*Units for x in xrange(Units)] #Parce que demandé par l'algorithme
    for lap in xrange(T) : #2 * (10**4)
        signal = normalize_v([randrange(1, 10)for x in xrange(2)]) #Signal aléatoire
        d = euclid_dis(signal) #Find euclidian distance
        star = find_att(d) #With it find j*
        provide_sortie(sortie, star) #Provide sortie
        weighting(signal, alpha, star, radius) #Pondération du voisinage
        alpha = ALPHAo * new_rate(lap) # new learning rate
        radius = int(Ro * new_rate(lap)) # new integral radius
    return lap



#Pour lancer l'apprentissage

print("Here, we are testing the topology map by using a 8*8 matrix, we initiate each processor's attractivity weight between .45 and .55, .2 as a learning coefficient. The entry signals are random and because we iterate 2 * (10**4), all processors' weight end up at the same place:\n")

from random import randrange
Units = 8
W = [[(randrange(450, 550) * .001) for i in xrange(Units)] for x in xrange(Units)] # 0.5 ± 5 %
M = [x[:] for x in W]

ALPHAo = .2
Ro = Units / 2 # half of the width of the network
T = 2 * (10**4)


teach(W) # training phase
for A in xrange(Units) :
    for B in xrange(Units) : print "%6i%2i\t%4.2f --> %4.2f" % (A,B, M[A][B], W[A][B])


