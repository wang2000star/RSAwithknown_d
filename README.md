python 3.9.12

purpose: factor RSA when n,e,d are known  

Pricinple 1: we suppose $q<p<Lq$, acutually L always be 2;  
             $p+q>2sqrt(pq),p+q=sqrt((p-q)^2+4pq)<sqrt(pq(L+1)^2/L)$
             $\phi=pq-(p+q)+1,k=(ed-1)/\phi,$  
             $max(e,d)<phi,1<=k<min(e,d)$
             $W = e*d - 1$
             $a = (n + 1)*W + gmpy2.isqrt(4*n*W**2)$
             $A = pow(n - 1,2)$
             $L = 2$
             $b = L*(n + 1)*W + int(gmpy2.sqrt(L**3*(L+1)^2*n*W**2)/2)$
             $B = L*pow(n + 1,2) - (L+1)**2*n$
             so $1 + a//A <= k <= min{e,d,1 + b//B}$ 
             
Principle 2: Let k=ed-1=2^s*t, where k is an even number, s>=1, t>=1. Randomly select an integer g, 1<g<n-1.
             Case 1: If gcd(g,n)!=1, then p=gcd(g,n) is a factor of n.
             Case 2: If gcd(g,n)=1, for 0<=i<=s, the values of (g^t)^(2^i) mod n fall into four categories:
             111111; -111111; ***-111111; ***111111, where * represents !=1 and !=n-1.
             # For the first three categories, reselect g.
             For the fourth category, if x^2 mod n = 1, then n|(x+1)(x-1), 1<=x<=n-1, -1<=x^2-1<=n(n-2);
             If x!=1 and x!=n-1, then 2<x+1<n, 0<x-1<n-2, so 1<=gcd(x-1,n), gcd(x+1,n)<n.
             Suppose gcd(x-1,n)=1, then n|x+1, contradiction; similarly, suppose gcd(x+1,n)=1, then n|x-1, contradiction.
             The factors of n are only 1, p, q, n, so gcd(x-1,n)=p or q and gcd(x+1,n)=p or q.
