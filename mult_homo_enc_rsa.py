
#Compiled and executed on Python IDLE 3.7, code will not work for Python 2.x
import random
import sys
import math


#Euclid's algorithm for determining the greatest common divisor

def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a


#Euclid's extended algorithm for finding the multiplicative inverse of two numbers

def multiplicative_inverse(e, phi):
   d = None
   i = 1
   exit = False
   while not exit:
       temp1 = phi*i +1
       d = float(temp1/e)
       d_int = int(d)
       i += 1
       if(d_int == d):
           exit=True
   return int(d)


def generate_keypair(p, q):
    
    n = p * q

    #Phi is the totient of n
    phi = (p-1) * (q-1)

    #Choosing an integer e such that e and phi(n) are coprime
    e = random.randrange(1, phi)

    #Using Euclid's Algorithm to verify that e and phi(n) are comprime
    g = gcd(e, phi)
    while g != 1:
        e = random.randrange(1, phi)
        g = gcd(e, phi)

    #Using Extended Euclid's Algorithm to generate the private key
    d = multiplicative_inverse(e, phi)
    
    #Returning public and private keypair
    #Public key is (e, n) and private key is (d, n)
    return ((e, n), (d, n))

def encrypt(pk, plaintext):
    #Unpacking the key into it's components
    key, n = pk
    #Converting each letter in the plaintext to numbers based on the character using a^b mod m
    cipher = pow(plaintext,key,n)
    #Returning the array of bytes
    return cipher

def decrypt(pk, ciphertext):
    #Unpacking the key into its components
    key, n = pk
    #Generating the plaintext based on the ciphertext and key using a^b mod m
    plain = pow(ciphertext,key,n)
    #Returning the array of bytes as a string
    return plain


def rabinMiller(n):
     s = n-1
     t = 0
     while s&1 == 0:
         s = s//2
         t +=1
     k = 0
     while k<128:
         a = random.randrange(2,n-1)
         #a^s is computationally infeasible. Thus we need a more intelligent approach
         #v = (a**s)%n
         v = pow(a,s,n) #where values are (num,exp,mod)
         if v != 1:
             i=0
             while v != (n-1):
                 if i == t-1:
                     return False
                 else:
                     i = i+1
                     v = (v**2)%n
         k+=2
     return True

def isPrime(n):
     #lowPrimes is all primes (sans 2, which is covered by the bitwise and operator)
     #under 1000. taking n modulo each lowPrime allows us to remove a huge chunk
     #of composite numbers from our potential pool without resorting to Rabin-Miller
     lowPrimes =   [3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97
                   ,101,103,107,109,113,127,131,137,139,149,151,157,163,167,173,179
                   ,181,191,193,197,199,211,223,227,229,233,239,241,251,257,263,269
                   ,271,277,281,283,293,307,311,313,317,331,337,347,349,353,359,367
                   ,373,379,383,389,397,401,409,419,421,431,433,439,443,449,457,461
                   ,463,467,479,487,491,499,503,509,521,523,541,547,557,563,569,571
                   ,577,587,593,599,601,607,613,617,619,631,641,643,647,653,659,661
                   ,673,677,683,691,701,709,719,727,733,739,743,751,757,761,769,773
                   ,787,797,809,811,821,823,827,829,839,853,857,859,863,877,881,883
                   ,887,907,911,919,929,937,941,947,953,967,971,977,983,991,997]
     if (n >= 3):
         if (n&1 != 0):
             for p in lowPrimes:
                 if (n == p):
                    return True
                 if (n % p == 0):
                     return False
             return rabinMiller(n)
     return False

def generateLargePrime(k):
     #k is the desired bit length
     r=100*(math.log(k,2)+1) 
     r_ = r
     while r>0:
         n = random.randrange(2**(k-1),2**(k))
         r-=1
         if isPrime(n) == True:
             return n



if __name__ == '__main__':
    '''
    Detect if the script is being run directly by the user
    '''
    print ("Multiplicative Homomorphic RSA Encrypter")
    l=int(input("Enter the length of prime(in bits):"))
    p=generateLargePrime(l)
    print("First Prime number:",p)
    q=generateLargePrime(l)
    print("Second Prime Number:",q)
    print ("Generating your public/private keypairs now . . .")
    private, public = generate_keypair(p, q)
    print ("Your public key is ", public ," and your private key is ", private)
    message1 = int(input("Enter a number to encrypt with your public key: "))
    encrypted_msg1 = encrypt(public, message1)
    print("Your encrypted number is: ")
    print (encrypted_msg1)
    message2 = int(input("Enter another number to encrypt with your public key: "))
    encrypted_msg2 = encrypt(public, message2)
    print ("Your encrypted number is: ")
    print (encrypted_msg2)
    #Using Multiplicative Homomorphic property of RSA
    encrypted_answer= encrypted_msg1 * encrypted_msg2
    print("Encrypted answer is: ")
    print(encrypted_answer)
    #Verifying the homomorphic encryption scheme by decrypting the encrypted answer
    print ("Decrypting answer with private key . . .")
    print ("Your answer is:")
    print (decrypt(private, encrypted_answer))
