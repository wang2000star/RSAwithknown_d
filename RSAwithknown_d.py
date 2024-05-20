import gmpy2,random

#the function to check if n is a perfect square
def is_perfect_square(n):
    '''
    If n is a perfect square it returns sqrt(n),
    
    otherwise returns -1
    '''
    h = n & 0xF; #last hexadecimal "digit"
    
    if h > 9:
        return -1 # return immediately in 6 cases out of 16.

    # Take advantage of Boolean short-circuit evaluation
    if ( h != 2 and h != 3 and h != 5 and h != 6 and h != 7 and h != 8 ):
        # take square root if you must
        t = gmpy2.isqrt(n)
        if t*t == n:
            return t
        else:
            return -1
    
    return -1

#the first method to factorize n with known e and d
def factor_pqRange(n, e, d):
    """
        Pricinple: we suppose q<p<Lq, acutually L always be 2;
        p+q>2sqrt(pq),p+q=sqrt((p-q)^2+4pq)<sqrt((L+3)pq)
        phi=pq-(p+q)+1,k=(ed-1)/phi,
        max(e,d)<phi,1<=k<min(e,d)
        so 1+a//A<=k<=min{e,d,1+b//B}
    """
    W = e*d - 1
    a = (n + 1)*W + gmpy2.isqrt(4*n*W**2)
    A = pow(n - 1,2)
    L = 2
    b = (n + 1)*W + gmpy2.isqrt((L+3)*n*W**2)
    B = pow(n + 1,2) - 5*n
    kmin = 1 + a//A
    kmax = min(min(e, d) - 1, 1 + b//B)

    for k in range(kmin, kmax+1):#range is [kmin,kmax]
        if W % k == 0:
            phi = W // k
            s = n - phi + 1
            # check if the equation x^2 - s*x + n = 0
            # has integer roots
            discr = s*s - 4*n
            if(discr>=0):
                t = is_perfect_square(discr)
                if t!=-1 and (s+t)%2==0:
                    #pq=n,pq-p-q+1=phi,所以p+q=n-phi+1=s，p-q=t,所以p=(s+t)/2,q=(s-t)/2，假设p>q的情况
                    return (s+t)//2,(s-t)//2       

#the second method to factorize n with known e and d
def factor_pq(n, e, d):        
    """
        Principle: Let k=ed-1=2^s*t, where k is an even number, s>=1, t>=1. Randomly select an integer g, 1<g<n-1.
        Case 1: If gcd(g,n)!=1, then p=gcd(g,n) is a factor of n.
        Case 2: If gcd(g,n)=1, for 0<=i<=s, the values of (g^t)^(2^i) mod n fall into four categories:
        111111; -111111; ***-111111; ***111111, where * represents !=1 and !=n-1.
        # For the first three categories, reselect g.
        For the fourth category, if x^2 mod n = 1, then n|(x+1)(x-1), 1<=x<=n-1, -1<=x^2-1<=n(n-2);
        If x!=1 and x!=n-1, then 2<x+1<n, 0<x-1<n-2, so 1<=gcd(x-1,n), gcd(x+1,n)<n.
        Suppose gcd(x-1,n)=1, then n|x+1, contradiction; similarly, suppose gcd(x+1,n)=1, then n|x-1, contradiction.
        The factors of n are only 1, p, q, n, so gcd(x-1,n)=p or q and gcd(x+1,n)=p or q.
    """
    k = e*d - 1
    t=k
    while t % 2 == 0:
        t = t // 2
    while True:
        g = random.randint(2, n-2)
        gcd_gn = gmpy2.gcd(g, n)
        if gcd_gn != 1:
                p = gcd_gn
                if pow(p,2) > n:
                    return (p, n//p) 
                return (n//p, p)
        else:
            x=pow(g,t,n)
            if x==1 or x==n-1:
                continue
            else:
                while True: # Will find y=-1 or 1 within s times
                    y=pow(x,2,n)
                    if y==1:
                        p = gmpy2.gcd(x-1, n)
                        if  pow(p,2)>n:
                            return (p, n//p) 
                        return (n//p, p)
                    if y==n-1:
                        break
                    x=y                      

if __name__ == "__main__":
    n=0xd231f2c194d3971821984dec9cf1ef58d538975f189045ef8a706f6165aab4929096f61a3eb7dd8021bf3fdc41fe3b3b0e4ecc579b4b5e7e035ffcc383436c9656533949881dca67c26d0e770e4bf62a09718dbabc2b40f2938f16327e347f187485aa48b044432e82f5371c08f6e0bbde46c713859aec715e2a2ca66574f3eb
    e=0x5b5961921a49e3089262761e89629ab6dff2da1504a0e5eba1bb7b20d63c785a013fd6d9e021c01baf1b23830954d488041b92bca2fe2c92e3373dedd7e625da11275f6f18ee4aef336d0637505545f70f805902ddbacb21bb8276d34a0f6dfe37ede87dd95bb1494dbb5763639ba3984240f1178e32aa36ee3c5fcc8115dde5
    d=0x31df315ae64639876342f0ce3367a436ad9b92201a450b0d8b1465786a53a5e01bd70025
    p,q=factor_pqRange(n,e,d)
    if p*q==n:
        print("sucess!")
        print("p:",hex(p))
        print("q:",hex(q))
    else:
        print("failed")
